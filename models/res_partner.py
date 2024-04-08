# -*- coding: utf-8 -*-
from odoo import fields, models


class Employee(models.Model):
    """partner model for teacher and staff"""
    _inherit = 'res.partner'

    partner = fields.Selection([('teacher', 'Teacher'),
                                ('office_staff', 'Office Staff')])

    def user_automation_res(self):
        """USER CREATION AUTOMATION"""
        teacher = self.env.ref('school_management.school_teacher_group')
        office_staff = self.env.ref('school_management.school_office_staff_group')
        user = self.env['res.users'].create({
            'name': self.name,
            'login': self.email,
            'partner_id': self.id
        })
        if self.partner == 'teacher':
            user.write({'groups_id': [(fields.Command.link(teacher.id))]})
        if self.partner == 'office_staff':
            user.write({'groups_id': [(fields.Command.link(office_staff.id))]})
