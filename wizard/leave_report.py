# -*- coding: utf-8 -*-
from datetime import datetime
from odoo import fields, models
from dateutil.relativedelta import relativedelta, MO, SU
from odoo.exceptions import UserError, ValidationError
import io
import json
import xlsxwriter
from odoo import models
from odoo.tools import date_utils


class LeaveReport(models.TransientModel):
    """ wizard model"""
    _name = 'leave.report'

    date_type = fields.Selection([('month', 'Month'), ('week', 'Week'), ('day', 'Day'), ('custom', 'Custom')])
    custom_start_date = fields.Date(string='Start date')
    custom_end_date = fields.Date(string='End date')
    students_ids = fields.Many2many(comodel_name='students.registration',
                                    domain="[('student_class_id', '=', class_id)]")
    class_id = fields.Many2one(comodel_name='school.class')

    def action_leave_report(self):
        query = """ SELECT sr.id,scl.id,sr.first_name,l.start_date,l.end_date,l.total_days,l.reason 
                    FROM   school_leave AS l
                    RIGHT  JOIN students_registration AS sr ON sr.id = l.student_id 
                    LEFT  JOIN school_class AS scl ON scl.id = l.school_class_id WHERE TRUE """
        if self.date_type:
            if self.date_type == 'day':
                query += """AND start_date = '%s' """ % fields.Date.today()
            elif self.date_type == 'month':
                month_start_date = fields.Date.today() + relativedelta(day=1)
                month_end_date = fields.Date.today() + relativedelta(day=1, months=1)
                query += """AND l.start_date BETWEEN '%s' and '%s' """ % (month_start_date, month_end_date)
            elif self.date_type == 'week':
                week_start_date = fields.Date.today() + relativedelta(weekday=MO(-1))
                week_end_date = fields.Date.today() + relativedelta(weekday=SU)
                query += """AND l.start_date BETWEEN '%s' and '%s' """ % (week_start_date, week_end_date)
            elif self.date_type == 'custom':
                if self.custom_start_date:
                    start = self.custom_start_date
                    query += """AND start_date < '%s' """ % start
                elif self.custom_end_date:
                    end = self.custom_end_date
                    query += """AND start_date > '%s' """ % end
                elif self.custom_start_date and self.custom_end_date:
                    if self.custom_start_date > self.custom_end_date:
                        raise ValidationError("Wrong Date")
                    else:
                        start = self.custom_start_date
                        end = self.custom_end_date
                        query += """AND start_date BETWEEN '%s' and '%s' ORDER BY start_date DESC""" % (start, end)
                else:
                    query += """"""

        if self.class_id:
            school_class = self.class_id.id
            query += """ AND scl.id = %s""" % str(school_class)
        if self.students_ids:
            students = self.students_ids.ids
            stud = tuple(students)
            if len(stud) == 1:
                query += """AND sr.id = %s""" % str(stud[0])
            else:
                query += """AND sr.id in %s""" % str(stud)

        self.env.cr.execute(query)
        date = str(datetime.today().date())
        report = self.env.cr.dictfetchall()
        students = []
        for stud in report:
            var = stud['first_name']
            if var not in students:
                students.append(var)
        count = 0
        if len(students) > 1:
            count = len(students)
        data = {'report': report, 'date': date, 'count': count}
        if len(data['report']) > 0:
            return self.env.ref('school_management.leave_information_report_action').report_action(self, data)
        else:
            raise UserError('No Records')

    def action_leave_excel(self):
        query = """ SELECT sr.id,scl.id,sr.first_name,l.start_date,l.end_date,l.total_days,l.reason 
                           FROM   school_leave AS l
                           RIGHT  JOIN students_registration AS sr ON sr.id = l.student_id 
                           LEFT  JOIN school_class AS scl ON scl.id = l.school_class_id WHERE TRUE """
        if self.date_type:
            if self.date_type == 'day':
                query += """AND start_date = '%s' """ % fields.Date.today()
            elif self.date_type == 'month':
                month_start_date = fields.Date.today() + relativedelta(day=1)
                month_end_date = fields.Date.today() + relativedelta(day=1, months=1)
                query += """AND l.start_date BETWEEN '%s' and '%s' """ % (month_start_date, month_end_date)
            elif self.date_type == 'week':
                week_start_date = fields.Date.today() + relativedelta(weekday=MO(-1))
                week_end_date = fields.Date.today() + relativedelta(weekday=SU)
                query += """AND l.start_date BETWEEN '%s' and '%s' """ % (week_start_date, week_end_date)
            elif self.date_type == 'custom':
                if self.custom_start_date:
                    start = self.custom_start_date
                    query += """AND start_date < '%s' """ % start
                elif self.custom_end_date:
                    end = self.custom_end_date
                    query += """AND start_date > '%s' """ % end
                elif self.custom_start_date and self.custom_end_date:
                    if self.custom_start_date > self.custom_end_date:
                        raise ValidationError("Wrong Date")
                    else:
                        start = self.custom_start_date
                        end = self.custom_end_date
                        query += """AND start_date BETWEEN '%s' and '%s' ORDER BY start_date DESC""" % (start, end)
                else:
                    query += """"""
        if self.class_id:
            school_class = self.class_id.id
            query += """ AND scl.id = %s""" % str(school_class)
        if self.students_ids:
            students = self.students_ids.ids
            stud = tuple(students)
            if len(stud) == 1:
                query += """AND sr.id = %s""" % str(stud[0])
            else:
                query += """AND sr.id in %s""" % str(stud)
        self.env.cr.execute(query)
        date = str(datetime.today().date())
        report = self.env.cr.dictfetchall()
        students = []
        for stud in report:
            var = stud['first_name']
            if var not in students:
                students.append(var)
        count = 0
        company = self.env.user.company_id.name
        company_address = self.env.user.company_id.street
        if len(students) > 1:
            count = len(students)
        data = {'report': report, 'date': date, 'count': count, 'company': company,
                'address': company_address}
        if len(data['report']) > 0:
            return {
                'type': 'ir.actions.report',
                'data': {'model': 'leave.report',
                         'options': json.dumps(data,
                                               default=date_utils.json_default),
                         'output_format': 'xlsx',
                         'report_name': 'Leave Information Excel Report',
                         },
                'report_type': 'xlsx',
            }
        else:
            raise UserError("No Records")

    def get_xlsx_report(self, data, response):
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet()
        sheet.set_column('A:C', 18)
        cell_format = workbook.add_format(
            {'font_size': '12px', 'align': 'center', 'bg_color': '696969'})
        head = workbook.add_format(
            {'align': 'center', 'bold': True, 'font_size': '20px'})
        txt = workbook.add_format({'font_size': '10px', 'align': 'center'})
        sheet.merge_range('A4:D5', 'Leave Information', head)
        if data['count'] == 0:
            sheet.write('A6', f"Name:{data['report'][0].get('first_name')}", txt)
        sheet.write('A3', 'Printed On : ' + data.get('date', False), txt)
        sheet.merge_range('A1:B1', 'Company  : ' + data.get('company', False), txt)
        sheet.merge_range('A2:B2', data.get('address', False), txt)
        if data['count'] > 0:
            sheet.write('A7', 'Student:', cell_format)
            sheet.write('B7', 'Start Date:', cell_format)
            sheet.write('C7', 'End Date:', cell_format)
            sheet.write('D7', 'Days:', cell_format)
            sheet.write('E7', 'Reason', cell_format)
        else:
            sheet.write('A7', 'Start Date:', cell_format)
            sheet.write('B7', 'End Date:', cell_format)
            sheet.write('C7', 'Days:', cell_format)
            sheet.write('D7', 'Reason', cell_format)
        for i, students in enumerate(data['report'], start=8):
            if data['count'] > 0:
                sheet.write(f'A{i}', students['first_name'], txt)
                sheet.write(f'B{i}', students['start_date'], txt)
                sheet.write(f'C{i}', students['end_date'], txt)
                sheet.write(f'D{i}', students['total_days'], txt)
                sheet.write(f'E{i}', students['reason'], txt)
            else:
                sheet.write(f'A{i}', students['start_date'], txt)
                sheet.write(f'B{i}', students['end_date'], txt)
                sheet.write(f'C{i}', students['total_days'], txt)
                sheet.write(f'D{i}', students['reason'], txt)
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
