# -*- coding: utf-8 -*-
from odoo import models, fields


class Department(models.Model):
    """ department creation model"""
    _name = 'school.department'
    _description = "Department"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(required=True, string='Department Name')
    head_of_department_id = fields.Many2one("res.partner")
