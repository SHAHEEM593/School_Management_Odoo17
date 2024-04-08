# -*- coding: utf-8 -*-
from datetime import datetime
from odoo import fields, models
from odoo.exceptions import UserError
import io
import json
import xlsxwriter
from odoo import models
from odoo.tools import date_utils


class ExamDetails(models.TransientModel):
    """ wizard model"""
    _name = 'exam.details'

    student_ids = fields.Many2many('students.registration')
    class_id = fields.Many2one('school.class')
    exam_id = fields.Many2one('school.exam')

    def action_exam_report(self):
        query = """SELECT ex.names,cl.name,sr.first_name FROM school_exam AS ex
                       INNER JOIN school_class AS cl ON cl.id = ex.exam_class_id
                       INNER JOIN school_exam_students_registration_rel AS srl ON srl.school_exam_id = ex.id
                       INNER JOIN students_registration AS sr ON sr.id = srl.students_registration_id
               """
        if self.student_ids:
            students = self.student_ids.ids
            stud = tuple(students)
            if len(stud) == 1:
                query += """where sr.id = %s""" % str(stud[0])
            else:
                query += """where sr.id in %s""" % str(stud)
        elif self.class_id:
            school_class = self.class_id.id
            query += """ where cl.id = %s""" % str(school_class)
        elif self.exam_id:
            school_exam = self.exam_id.id
            query += """ where ex.id = %s""" % str(school_exam)
        self.env.cr.execute(query)
        date = str(datetime.today().date())
        report = self.env.cr.dictfetchall()
        data = {'report': report, 'date': date}
        if len(data['report']) > 0:
            return self.env.ref('school_management.exam_detail_report_action').report_action(self, data)
        else:
            raise UserError('No Records')

    def action_exam_excel(self):
        query = """SELECT ex.names,cl.name,sr.first_name FROM school_exam AS ex
                               INNER JOIN school_class AS cl ON cl.id = ex.exam_class_id
                               INNER JOIN school_exam_students_registration_rel AS srl ON srl.school_exam_id = ex.id
                               INNER JOIN students_registration AS sr ON sr.id = srl.students_registration_id
                       """
        if self.student_ids:
            students = self.student_ids.ids
            stud = tuple(students)
            if len(stud) == 1:
                query += """where sr.id = %s""" % str(stud[0])
            else:
                query += """where sr.id in %s""" % str(stud)
        elif self.class_id:
            school_class = self.class_id.id
            query += """ where cl.id = %s""" % str(school_class)
        elif self.exam_id:
            school_exam = self.exam_id.id
            query += """ where ex.id = %s""" % str(school_exam)
        self.env.cr.execute(query)
        date = str(datetime.today().date())
        report = self.env.cr.dictfetchall()
        company = self.env.user.company_id.name
        company_address = self.env.user.company_id.street

        data = {'report': report, 'date': date, 'company': company, 'address': company_address}
        if len(data['report']) > 0:
            return {
                'type': 'ir.actions.report',
                'data': {'model': 'exam.details',
                         'options': json.dumps(data,
                                               default=date_utils.json_default),
                         'output_format': 'xlsx',
                         'report_name': 'Exam Details Excel Report',
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
        sheet.merge_range('A4:C5', 'Exam Details', head)
        sheet.write('A3', 'Printed On : ' + data.get('date', False), txt)
        sheet.merge_range('A1:B1',  data.get('company', False), txt)
        sheet.merge_range('A2:B2', data.get('address', False), txt)
        sheet.write('A6', 'Name:', cell_format)
        sheet.write('B6', 'Class:', cell_format)
        sheet.write('C6', 'Student:', cell_format)
        for i, product in enumerate(data['report'],
                                    start=7):
            sheet.write(f'A{i}', product['names'], txt)
            sheet.write(f'B{i}', product['name'], txt)
            sheet.write(f'C{i}', product['first_name'], txt)
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
