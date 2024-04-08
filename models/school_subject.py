# -*- coding: utf-8 -*-
from odoo import models, fields


class ManageSubject(models.Model):
    """subject creation model"""
    _name = 'school.subject'
    _description = 'Subject'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Subject Name', required=True)
    department_id = fields.Many2one('school.department')
    pass_mark = fields.Integer(string="Pass Mark")
    max_mark = fields.Integer(string="Max Mark")
