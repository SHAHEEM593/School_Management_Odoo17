# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from datetime import datetime, date
from odoo.exceptions import ValidationError


class Registration(models.Model):
    """ registration model"""
    _name = 'students.registration'
    _description = 'Student registration'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'first_name'
    _order = 'id desc'

    first_name = fields.Char(required=True, copy=True)
    last_name = fields.Char(string='Last Name', required=True)
    full_name = fields.Char(compute="_compute_full_name")
    reference = fields.Char(string="sequence", copy=False, readonly=True, default=lambda self: _('New'))
    father_name = fields.Char(string='Father Name')
    mother_name = fields.Char(string='Mother Name')
    communication_address = fields.Text(string="Address", required=True)
    student_class_id = fields.Many2one('school.class', string='Class')
    is_it_a_permanent_address = fields.Boolean()
    permanent_address = fields.Text(string="Permanent Address")
    email = fields.Char(string='Email', required=True)
    phone = fields.Char(string="Phone")
    dob = fields.Date(required=True, string='DOB')
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string='Gender', required=True)
    registration_date = fields.Date(default=datetime.today())
    photo = fields.Image()
    previous_department = fields.Selection(
        [('preschool', 'PRE SCHOOL'), ('highschool', 'HIGH SCHOOL'), ('highersec', 'HIGHER SEC')],
        string="previous_academic_department_id")

    previous_class = fields.Selection([('lkg', 'LKG'), ('ukg', 'UKG'), ('one', 'ONE'), ('tenth', 'TENTH'),
                                       ('plustwo', 'PLUS TWO'), ('plusone', 'PLUS ONE')], string='previous_class_id')
    multi_school_id = fields.Many2one('res.company', string='School', default=lambda self: self.env.user.company_id.id)
    tc = fields.Binary()
    aadhaar_number = fields.Char(string='aadhaar number')
    status = fields.Selection([('draft', 'Draft'), ('registration', 'Registration'), ],
                              default="draft", tracking=True)
    notes = fields.Text()
    age = fields.Integer(compute="_compute_dob", store=True)
    clubs_ids = fields.Many2many('school.club', string='Club')
    events_ids = fields.Many2many('school.event', compute='_compute_event')
    active = fields.Boolean(default=True)
    exam_student_ids = fields.Many2many('school.exam', string="exam")
    attendance = fields.Boolean()
    leave_id = fields.Many2one('school.leave')
    user_id = fields.Many2one(
        'res.users', string='Student', )
    website = fields.Boolean(default=False)

    """ aadhar unique"""
    _sql_constraints = [('email_unique', 'UNIQUE(email)', "The Email must be unique"),
                        ('unique_id', 'UNIQUE(aadhaar_number)', "Aadhaar Number Must Be Unique"), ]

    @api.model
    def create(self, vals):
        """sequence creation"""
        vals['reference'] = self.env['ir.sequence'].next_by_code(
            'student.register') or _('New')
        res = super(Registration, self).create(vals)

        return res

    @api.model
    def user_automation(self):
        """USER CREATION AUTOMATION"""
        student = self.env.ref('school_management.school_student_group')
        user = self.env['res.users'].create({
            'name': self.full_name,
            'login': self.email
        })
        self.write({'user_id': user.id})
        user.write({'groups_id': [(fields.Command.link(student.id))]})

    @api.depends('first_name', 'last_name')
    def _compute_full_name(self):
        """ first name and last name add"""
        for rec in self:
            rec.full_name = str(rec.first_name) + str(rec.last_name)

    def _compute_event(self):
        """to get the events with club"""
        for rec in self:
            rec.events_ids = rec.clubs_ids.mapped('events_ids')

    @api.depends('dob')
    def _compute_dob(self):
        """age calculated based on dob"""
        today = date.today()
        if self.dob:
            self.age = today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))
            if self.age < 1:
                raise ValidationError(_('Age Must Be Positive'))

    def confirm_register(self):
        """status change button"""
        self.status = 'registration'

    def back_to_draft(self):
        """status change button"""
        self.status = 'draft'

    def attendance_check(self):
        """automation rule to create a user"""
        leaves = self.env['school.leave'].search([])
        leaves_students = leaves.student_id
        if leaves_students:
            leaves_students.attendance = False
