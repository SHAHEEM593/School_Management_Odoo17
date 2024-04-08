# -*- coding: utf-8 -*-
from odoo import models, fields


class AcademicYear(models.Model):
    """academic year model"""
    _name = 'academic.year'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Academic Year'

    name = fields.Char()
