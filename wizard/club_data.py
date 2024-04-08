# -*- coding: utf-8 -*-
from datetime import datetime
from odoo import fields, models
from odoo.exceptions import UserError
import io
import json
import xlsxwriter
from odoo import models
from odoo.tools import date_utils


class ClubData(models.TransientModel):
    """ wizard model"""
    _name = 'club.data'

    club_id = fields.Many2one('school.club')
    students_ids = fields.Many2many('students.registration')

    def action_club_report(self):
        query = """     SELECT cd.name  FROM school_club AS cd
                        INNER JOIN school_club_students_registration_rel AS sr ON sr.school_club_id = cd.id
                        INNER JOIN students_registration AS se ON se.id = sr.students_registration_id"""

        query1 = """SELECT cd.name as club,se.first_name,se.phone,se.gender,se.dob,sc.name as namez  FROM school_club AS cd
                          INNER JOIN school_club_students_registration_rel AS sr ON sr.school_club_id = cd.id
                          INNER JOIN students_registration AS se ON se.id = sr.students_registration_id
                          INNER JOIN school_class AS sc ON sc.id = se.student_class_id"""

        query2 = """SELECT cd.name,she.names,she.start_date,she.end_date FROM school_club AS cd
                          INNER JOIN school_club_school_event_rel AS sce ON sce.school_club_id = cd.id
                          INNER JOIN school_event AS she ON she.id = sce.school_event_id"""
        club = []
        name = []
        count = 0
        if self.students_ids or self.club_id:
            if self.students_ids:
                students = self.students_ids.ids
                stud = tuple(students)
                var = self.env['school.club'].search([('students_ids', 'in', students)]).mapped('name')
                club = var
                if len(stud) == 1:
                    count = len(stud)
                    query1 += """ WHERE  se.id = %s""" % str(stud[0])
                    name.append(self.students_ids.first_name)
                else:
                    query1 += """ WHERE  se.id in %s""" % str(stud)
            if self.club_id:
                clubs = self.club_id.id
                query += """ where cd.id = %s""" % str(clubs)
                club.append(self.club_id.name)
        else:
            club = self.env['school.club'].search([]).mapped('name')
        date = str(datetime.today().date())
        self.env.cr.execute(query)
        report = self.env.cr.dictfetchall()
        self.env.cr.execute(query1)
        students = self.env.cr.dictfetchall()
        self.env.cr.execute(query2)
        events = self.env.cr.dictfetchall()
        data = {'report': report, 'date': date, 'events': events,
                'club': club, 'students': students, 'count': count, 'name': name}

        if len(data['report']) > 0:
            return self.env.ref('school_management.school_club_report_action').report_action(self, data)
        else:
            raise UserError('No Records')

    def action_club_excel(self):
        query = """     SELECT cd.name  FROM school_club AS cd
                                INNER JOIN school_club_students_registration_rel AS sr ON sr.school_club_id = cd.id
                                INNER JOIN students_registration AS se ON se.id = sr.students_registration_id"""

        query1 = """SELECT cd.name as club,se.first_name,se.phone,se.gender,se.dob,sc.name as namez  FROM school_club AS cd
                                  INNER JOIN school_club_students_registration_rel AS sr ON sr.school_club_id = cd.id
                                  INNER JOIN students_registration AS se ON se.id = sr.students_registration_id
                                  INNER JOIN school_class AS sc ON sc.id = se.student_class_id"""

        query2 = """SELECT cd.name,she.names,she.start_date,she.end_date FROM school_club AS cd
                                  INNER JOIN school_club_school_event_rel AS sce ON sce.school_club_id = cd.id
                                  INNER JOIN school_event AS she ON she.id = sce.school_event_id
                """
        club = []
        name = []
        count = 0
        if self.students_ids or self.club_id:
            if self.students_ids:
                students = self.students_ids.ids
                stud = tuple(students)
                var = self.env['school.club'].search([('students_ids', 'in', students)]).mapped('name')
                club = var
                if len(stud) == 1:
                    count = len(stud)
                    query1 += """ WHERE  se.id = %s""" % str(stud[0])
                    name.append(self.students_ids.first_name)
                else:
                    query1 += """ WHERE  se.id in %s""" % str(stud)
            if self.club_id:
                clubs = self.club_id.id
                query += """ where cd.id = %s""" % str(clubs)
                club.append(self.club_id.name)
        else:
            club = self.env['school.club'].search([]).mapped('name')
        date = str(datetime.today().date())
        self.env.cr.execute(query)
        report = self.env.cr.dictfetchall()
        self.env.cr.execute(query1)
        students = self.env.cr.dictfetchall()
        self.env.cr.execute(query2)
        events = self.env.cr.dictfetchall()
        company = self.env.user.company_id.name
        company_address = self.env.user.company_id.street

        data = {'report': report, 'date': date, 'events': events,
                'club': club, 'students': students, 'count': count, 'name': name, 'company': company,
                'address': company_address}

        if len(data['report']) > 0:
            return {
                'type': 'ir.actions.report',
                'data': {'model': 'club.data',
                         'options': json.dumps(data,
                                               default=date_utils.json_default),
                         'output_format': 'xlsx',
                         'report_name': 'Club Data Excel Report',
                         },
                'report_type': 'xlsx',
            }
        else:
            raise UserError('No Records')

    def get_xlsx_report(self, data, response):
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet()
        sheet.set_column('A:E', 18)
        cell_format = workbook.add_format(
            {'font_size': '12px', 'align': 'center', 'bg_color': '696969'})
        head = workbook.add_format(
            {'align': 'center', 'bold': True, 'font_size': '20px'})
        txt = workbook.add_format({'font_size': '10px', 'align': 'center'})
        sheet.write('A3', 'Printed On : ' + data.get('date', False), txt)
        sheet.merge_range('A1:B1', 'Company  : ' + data.get('company', False), txt)
        sheet.merge_range('A2:B2', data.get('address', False), txt)
        count = 8
        sheet.merge_range(f'A{4}:E{5}', 'Club Report', head)
        if data.get('count') != 1:
            for club in data['club']:
                i = count
                sheet.merge_range(f'A{i - 2}:E{i - 1}', club, head)
                sheet.write(f'A{i}', 'Student:', cell_format)
                sheet.write(f'B{i}', 'Phone:', cell_format)
                sheet.write(f'C{i}', 'Gender :', cell_format)
                sheet.write(f'D{i}', 'Dob :', cell_format)
                sheet.write(f'E{i}', 'Class', cell_format)
                for stud in data['students']:
                    if club == stud['club']:
                        j = i + 1
                        sheet.write(f'A{j}', stud['first_name'], txt)
                        sheet.write(f'B{j}', stud['phone'], txt)
                        sheet.write(f'C{j}', stud['gender'], txt)
                        sheet.write(f'D{j}', stud['dob'], txt)
                        sheet.write(f'E{j}', stud['namez'], txt)
                        i = i + 1
                        count = j + 5
        if data.get('count') == 1:
            i = count - 1
            for stud in data['name']:
                sheet.merge_range(f'A{i - 2}:B{i - 3}', f"Student : {stud}", txt)
                sheet.merge_range(f'A{i}:E{i}', 'Club:', cell_format)
            j = i + 1
            for club in data['club']:
                sheet.merge_range(f'A{j}:E{j}', club, txt)
                j = j + 1
                count = j + 5
        k = count + 5
        sheet.merge_range(f'A{k - 2}:F{k - 1}', 'Events Report', head)
        sheet.write(f'A{k}', 'Club:', cell_format)
        sheet.write(f'B{k}', 'Events:', cell_format)
        sheet.write(f'C{k}', 'Start Date :', cell_format)
        sheet.write(f'D{k}', 'End Date :', cell_format)
        j = k + 1
        for events in data['events']:
            sheet.write(f'A{j}', events['name'], txt)
            sheet.write(f'B{j}', events['names'], txt)
            sheet.write(f'C{j}', events['start_date'], txt)
            sheet.write(f'D{j}', events['end_date'], txt)
            j = j + 1
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
