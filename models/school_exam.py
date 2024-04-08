# -*- coding: utf-8 -*-
from odoo import models, fields


class Exam(models.Model):
    """ school exams"""
    _name = "school.exam"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Exam"
    _rec_name = 'names'

    names = fields.Char(string="Name", required=True)
    exam_class_id = fields.Many2one('school.class', string='Class', required=True)
    exam_papers_ids = fields.Many2many('school.subject', string='Exam Paper')
    students_ids = fields.Many2many('students.registration', string="Student")
    status = fields.Selection([('draft', 'Draft'), ('assigned', 'Assigned')])

    def assign_exam(self):
        """ assign exam when clicking button"""
        self.students_ids = self.env['students.registration'].search([('student_class_id', '=', self.exam_class_id.id)])
        self.status = 'assigned'
