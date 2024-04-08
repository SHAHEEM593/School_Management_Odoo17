# -*- coding: utf-8 -*-
from datetime import datetime
from odoo import fields, models
from dateutil.relativedelta import relativedelta, MO, SU
from odoo.exceptions import ValidationError, UserError
import io
import json
import xlsxwriter
from odoo import models
from odoo.tools import date_utils


class EventDetails(models.TransientModel):
    """ wizard model"""
    _name = 'event.details'

    date_type = fields.Selection([('month', 'Month'), ('week', 'Week'), ('day', 'Day'), ('custom', 'Custom')])
    custom_start_date = fields.Date(string='Start date')
    custom_end_date = fields.Date(string='End date')
    club_id = fields.Many2one(comodel_name='school.club')

    def action_event_report(self):
        query = """SELECT sc.id,ev.names,ev.status,ev.start_date,ev.end_date,ev.total_days,rp.name FROM school_event AS ev
                       INNER JOIN res_partner AS rp ON rp.id = ev.responsible_id
                       INNER JOIN school_club AS sc ON sc.id = ev.club_id"""
        parms = (self.custom_start_date, self.custom_end_date)
        if self.date_type:
            if self.date_type == 'day':
                query += """WHERE l.start_date = '%s' """ % fields.Date.today()
            elif self.date_type == 'month':
                month_start_date = fields.Date.today() + relativedelta(day=1)
                month_end_date = fields.Date.today() + relativedelta(day=1, months=1)
                query += """ WHERE start_date BETWEEN '%s' and '%s' """ % (month_start_date, month_end_date)
            elif self.date_type == 'week':
                week_start_date = fields.Date.today() + relativedelta(weekday=MO(-1))
                week_end_date = fields.Date.today() + relativedelta(weekday=SU)
                query += """WHERE start_date BETWEEN '%s' and '%s' """ % (week_start_date, week_end_date)
                if self.date_type == 'custom':
                    if self.custom_start_date < self.custom_end_date:
                        query += """WHERE start_date BETWEEN %s and %s ORDER BY start_date DESC"""
                    else:
                        raise ValidationError("Wrong Date")
        if self.club_id:
            school_club = self.club_id.id
            query += """ where sc.id = %s""" % str(school_club)

        self.env.cr.execute(query, parms)
        date = str(datetime.today().date())
        report = self.env.cr.dictfetchall()
        data = {'report': report, 'date': date}
        if len(data['report']) > 0:
            return self.env.ref('school_management.event_detail_report_action').report_action(self, data)
        else:
            raise UserError('No Records')

    def action_event_excel(self):
        query = """SELECT sc.id,ev.names,ev.status,ev.start_date,ev.end_date,ev.total_days,rp.name 
                        FROM school_event AS ev
                       left JOIN res_partner AS rp ON rp.id = ev.responsible_id
                       left JOIN school_club AS sc ON sc.id = ev.club_id"""
        parms = (self.custom_start_date, self.custom_end_date)
        if self.date_type:
            if self.date_type == 'day':
                query += """ WHERE start_date = '%s' """ % fields.Date.today()
            elif self.date_type == 'month':
                month_start_date = fields.Date.today() + relativedelta(day=1)
                month_end_date = fields.Date.today() + relativedelta(day=1, months=1)
                query += """ WHERE start_date BETWEEN '%s' and '%s' """ % (month_start_date, month_end_date)
            elif self.date_type == 'week':
                week_start_date = fields.Date.today() + relativedelta(weekday=MO(-1))
                week_end_date = fields.Date.today() + relativedelta(weekday=SU)
                query += """ WHERE start_date BETWEEN '%s' and '%s' """ % (week_start_date, week_end_date)
                if self.date_type == 'custom':
                    if self.custom_start_date < self.custom_end_date:
                        query += """ WHERE start_date BETWEEN %s and %s ORDER BY start_date DESC"""
                    else:
                        raise ValidationError("Wrong Date")
        if self.club_id:
            school_club = self.club_id.id
            query += """ where sc.id = %s""" % str(school_club)

        self.env.cr.execute(query, parms)
        date = str(datetime.today().date())
        report = self.env.cr.dictfetchall()
        company = self.env.user.company_id.name
        company_address = self.env.user.company_id.street
        data = {'report': report, 'date': date, 'company': company, 'address': company_address}
        if len(data['report']) > 0:
            return {
                'type': 'ir.actions.report',
                'data': {'model': 'event.details',
                         'options': json.dumps(data,
                                               default=date_utils.json_default),
                         'output_format': 'xlsx',
                         'report_name': 'Event Details Excel Report',
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
        sheet.merge_range('A4:D5', 'Event Details', head)
        sheet.write('A3', 'Printed On : ' + data.get('date', False), txt)
        sheet.merge_range('A1:B1', data.get('company', False), txt)
        sheet.merge_range('A2:B2', data.get('address', False), txt)
        sheet.write('A6', 'Name:', cell_format)
        sheet.write('B6', 'Status:', cell_format)
        sheet.write('C6', 'Start Date:', cell_format)
        sheet.write('D6', 'End Date:', cell_format)
        sheet.write('E6', 'Responsible', cell_format)
        for i, events in enumerate(data['report'], start=7):
            sheet.write(f'A{i}', events['names'], txt)
            sheet.write(f'B{i}', events['status'], txt)
            sheet.write(f'C{i}', events['start_date'], txt)
            sheet.write(f'D{i}', events['end_date'], txt)
            sheet.write(f'E{i}', events['name'], txt)
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
