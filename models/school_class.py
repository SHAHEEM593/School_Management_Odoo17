# -*- coding: utf-8 -*-
from odoo import models, fields


class ManageClass(models.Model):
    """ class creation model"""
    _name = 'school.class'
    _description = 'Class'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Class Name', required=True)
    departments_id = fields.Many2one('school.department', string="Department Id ")
    head_of_department_id = fields.Many2one(string="Head Of Department", related="departments_id.head_of_department_id")
    school_id = fields.Many2one('res.company', string="School")
