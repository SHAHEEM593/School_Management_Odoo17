# -*- coding: utf-8 -*-
from odoo import fields, models
from datetime import date
import datetime as dte


class SchoolEvent(models.Model):
    """Event Creation"""
    _name = "school.event"
    _description = "Event"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'names'
    _order = 'id desc'

    names = fields.Char(string='Name', required=True)
    club_id = fields.Many2one('school.club', string='Club')
    status = fields.Selection([('draft', 'Draft'), ('registration', 'Registration'), ('in_progress', 'In Progress'),
                               ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='draft')
    active = fields.Boolean(default=True)
    start_date = fields.Date()
    end_date = fields.Date()
    total_days = fields.Date()
    responsible_id = fields.Many2one('res.partner')
    event_template = fields.Html()
    photo = fields.Image()

    def check_end_date(self):
        """schedule action to check today is end date"""
        today = date.today()
        for rec in self.search([]):
            if rec.end_date:
                end = dte.datetime.strptime(str(rec.end_date), '%Y-%m-%d').date()
                if today == end:
                    rec.status = 'completed'
                    rec.active = False

    def event_mail(self):
        """schedule action to sent mail before 2 days"""
        today = date.today()
        for rec in self:
            if rec.end_date:
                end = dte.datetime.strptime(str(rec.end_date), '%Y-%m-%d').date()
                mail_template = self.env.ref('school_management.event_mail_template')
                for students in self.club_id.students_ids:
                    if today - end == 2:
                        mail_template.send_mail(students.id, force_send=True)
