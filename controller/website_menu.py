# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import base64


class ServiceRequest(http.Controller):
    @http.route(['/students'], type='http', auth="public", website=True, csrf=False)
    def service_request(self):
        """Student Registration"""
        students = request.env['students.registration'].search([])
        values = {
            'students': students
        }
        return request.render(
            "school_management.Student", values)

    @http.route(['/student_registration'], type='http', auth="public", website=True, csrf=False)
    def action_create_student_registration(self, **sr):
        """ Student Creation"""
        first_name = sr.get('first_name')
        last_name = sr.get('last_name')
        phone = sr.get('phone')
        email = sr.get('email')
        dob = sr.get('dob')
        gender = sr.get('gender')
        address = sr.get('address')
        file = sr.get('Upload')
        tc = file.encode("ascii")
        tc_file = base64.b64encode(tc)
        request.env['students.registration'].create({
            'first_name': first_name,
            'last_name': last_name,
            'communication_address': address,
            'email': email,
            'phone': phone,
            'dob': dob,
            'gender': gender,
            'tc': tc_file,
            'website': True,

        })
        return request.render('school_management.thanks_form')


class Events(http.Controller):
    @http.route(['/events'], type='http', auth="public", website=True, csrf=False)
    def EventSchool(self):
        """Events"""
        events = request.env['school.event'].search([])
        club = request.env['school.club'].search([])
        user = request.env.user
        values = {
            'user': user,
            'events': events,
            'club': club,
        }
        return request.render(
            "school_management.Event", values)

    @http.route(['/events_create'], type='http', auth="public", website=True, csrf=False)
    def action_create_event_registration(self, **ev):
        """Events Creation"""
        name = ev.get('name')
        start_date = ev.get('start_date')
        end_date = ev.get('end_date')
        user = request.env.user
        request.env['school.event'].create({
            'names': name,
            'start_date': start_date,
            'end_date': end_date,
            'responsible_id': user.partner_id.id,

        })
        return request.render('school_management.thanks_form')


class Leave(http.Controller):
    @http.route(['/leave'], type='http', auth="public", website=True, csrf=False)
    def LeaveSchool(self):
        """Leave"""
        leave = request.env['school.leave'].search([])
        students = request.env['students.registration'].search([])

        values = {
            'leave': leave,
            'students': students,
        }
        return request.render(
            "school_management.Leave", values)

    @http.route(['/leave/create'], type='http', auth="public", website=True, csrf=False)
    def action_create_leave(self, **le):
        """Leave Creation"""
        user = request.env.user
        start_date = le.get('start_date')
        end_date = le.get('end_date')
        reason = le.get('reason')
        student = request.env['students.registration'].search([('email', '=', user.login)])
        class_id = student.student_class_id
        request.env['school.leave'].create({
            'student_id': student.id,
            'school_class_id': class_id.id,
            'start_date': start_date,
            'end_date': end_date,
            'reason': reason,
        })
        return request.render('school_management.thanks_form')


# tree
class Students(http.Controller):
    """Student Tree View"""

    @http.route(['/student'], type='http', auth="public", website=True, csrf=False)
    def student_tree_view(self):
        students = request.env['students.registration'].search([])
        values = {
            'students': students
        }
        return request.render(
            "school_management.Students", values)


class EventTree(http.Controller):
    @http.route(['/event_tree'], type='http', auth="public", website=True, csrf=False)
    def event_tree_view(self):
        """Event Tree View"""
        events = request.env['school.event'].search([])
        club = request.env['school.club'].search([])
        values = {
            'events': events,
            'club': club
        }
        return request.render(
            "school_management.events", values)


class LeaveTree(http.Controller):
    @http.route(['/leave_tree'], type='http', auth="public", website=True, csrf=False)
    def LeaveSchool(self):
        """Leave Tree view"""
        leave = request.env['school.leave'].search([])
        students = request.env['students.registration'].search([])
        class_id = request.env['school.class'].search([])
        values = {
            'leave': leave,
            'students': students,
            'class': class_id
        }
        return request.render(
            "school_management.Leaves", values)


