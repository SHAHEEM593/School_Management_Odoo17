# -*- coding: utf-8 -*-
from odoo import api, fields, models
import numpy as np
import datetime as dt


class SchoolLeave(models.Model):
    """leave model"""
    _name = 'school.leave'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Leave"
    _rec_name = "student_id"

    student_id = fields.Many2one("students.registration", string='Students', required=True, ondelete="cascade")
    school_class_id = fields.Many2one("school.class", string="Class", related='student_id.student_class_id', store=True)
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string="End Date", required=True)
    total_days = fields.Float(compute="compute_calculate_date", store=True)
    half_day = fields.Boolean()
    reason = fields.Char()

    @api.depends('start_date', 'end_date', 'total_days', 'half_day')
    def compute_calculate_date(self):
        """duration calculated on the basis of DOB and removed sunday and saturday"""
        if self.end_date:
            start = dt.datetime.strptime(str(self.start_date), '%Y-%m-%d').date()
            end = dt.datetime.strptime(str(self.end_date), '%Y-%m-%d').date()
            total_days = np.busday_count(start, end, weekmask='1111100')
            end_week = end.weekday()

            if start < end:
                if end_week == 5 or end_week == 6:
                    self.total_days = str(int(total_days))
                else:
                    self.total_days = str(int(total_days) + 1)
                if self.half_day:
                    self.total_days = 0.5

            else:
                self.total_days = 0
