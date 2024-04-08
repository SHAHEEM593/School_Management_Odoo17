# -*- coding: utf-8 -*-
from datetime import datetime
from odoo import fields, models
from odoo.exceptions import UserError
import io
import json
import xlsxwriter
from odoo import models
from odoo.tools import date_utils


class StudentInformation(models.TransientModel):
    """ wizard model"""
    _name = 'student.information'

    class_id = fields.Many2one('school.class')
    department_id = fields.Many2one('school.department')

    def action_students_report(self):
        query = """SELECT sr.first_name,sr.email,sr.phone,sr.gender,sr.age,sc.name,dp.name as namex FROM students_registration AS sr
                INNER JOIN school_class AS sc ON sc.id = sr.student_class_id
                INNER JOIN school_department AS dp ON dp.id = sc.departments_id
        """
        if self.class_id:
            school_class = self.class_id.id
            query += """ where sc.id = %s""" % str(school_class)
        if self.department_id:
            school_department = self.department_id.id
            query += """ where dp.id = %s""" % str(school_department)
        self.env.cr.execute(query)
        date = str(datetime.today().date())
        report = self.env.cr.dictfetchall()
        data = {'report': report, 'date': date}
        if len(data['report']) > 0:
            return self.env.ref('school_management.student_information_report_action').report_action(self, data)
        else:
            raise UserError('No Records')

    def action_student_information_excel(self):
        query = """SELECT sr.first_name,sr.email,sr.phone,sr.gender,sr.age,sc.name,dp.name as namex FROM students_registration AS sr
                        INNER JOIN school_class AS sc ON sc.id = sr.student_class_id
                        INNER JOIN school_department AS dp ON dp.id = sc.departments_id
                """
        if self.class_id:
            school_class = self.class_id.id
            query += """ where sc.id = %s""" % str(school_class)
        if self.department_id:
            school_department = self.department_id.id
            query += """ where dp.id = %s""" % str(school_department)
        self.env.cr.execute(query)
        date = str(datetime.today().date())
        report = self.env.cr.dictfetchall()
        company = self.env.user.company_id.name
        company_address = self.env.user.company_id.street
        data = {'report': report, 'date': date, 'company': company, 'address': company_address}
        if len(data['report']) > 0:
            return {
                'type': 'ir.actions.report',
                'data': {'model': 'student.information',
                         'options': json.dumps(data,
                                               default=date_utils.json_default),
                         'output_format': 'xlsx',
                         'report_name': 'Student Information Excel Report',
                         },
                'report_type': 'xlsx',
            }
        else:
            raise UserError('No Records')

    def get_xlsx_report(self, data, response):
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet()
        sheet.set_column('A:G', 18)
        cell_format = workbook.add_format(
            {'font_size': '12px', 'align': 'center', 'bg_color': '696969'})
        head = workbook.add_format(
            {'align': 'center', 'bold': True, 'font_size': '20px'})

        txt = workbook.add_format({'font_size': '10px', 'align': 'center'})
        sheet.merge_range('A4:E5', 'Student Information', head)
        sheet.write('A3', 'Printed On : ' + data.get('date', False), txt)
        sheet.merge_range('A1:B1', data.get('company', False), txt)
        sheet.merge_range('A2:B2', data.get('address', False), txt)
        sheet.write('A6', 'Name:', cell_format)
        sheet.write('B6', 'Email :', cell_format)
        sheet.write('C6', 'Phone :', cell_format)
        sheet.write('D6', 'Gender:', cell_format)
        sheet.write('E6', 'Age', cell_format)
        sheet.write('F6', 'Class', cell_format)
        sheet.write('G6', 'Department', cell_format)
        for i, students in enumerate(data['report'], start=7):
            sheet.write(f'A{i}', students['first_name'], txt)
            sheet.write(f'B{i}', students['email'], txt)
            sheet.write(f'C{i}', students['phone'], txt)
            sheet.write(f'D{i}', students['gender'], txt)
            sheet.write(f'E{i}', students['age'], txt)
            sheet.write(f'F{i}', students['name'], txt)
            sheet.write(f'G{i}', students['namex'], txt)
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
