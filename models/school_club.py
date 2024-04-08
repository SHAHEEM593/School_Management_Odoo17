# -*- coding: utf-8 -*-
from odoo import api, fields, models


class SchoolClub(models.Model):
    """school club"""
    _name = "school.club"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = " School Club"

    name = fields.Char()
    students_ids = fields.Many2many('students.registration', string='Students',
                                    domain=[('status', '=', 'registration')])
    events_ids = fields.Many2many("school.event", string='Event')
    events_count = fields.Integer(string='Events', compute='get_event_count')

    def get_event(self):
        """ to get event smart button"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Events',
            'view_mode': 'tree',
            'res_model': 'school.event',
            'domain': [('club_id', '=', self.id)],
            'context': "{'create': False}"

        }

    def get_event_count(self):
        """to get the count of the event"""
        for rec in self:
            rec.events_count = rec.env['school.event'].search_count([('club_id', '=', rec.id)])
            rec.events_ids = self.env['school.event'].search([('club_id', '=', rec.id)])
