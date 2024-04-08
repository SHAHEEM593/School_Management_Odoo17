# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class Event(http.Controller):
    @http.route(['/latest_event'], type="json", auth="public")
    def events(self):
        events = request.env['school.event'].sudo().search_read([], fields=['names', 'photo'])
        n = 4
        event = [events[i:i + n] for i in range(0, len(events), n)]
        return event


class EventData(http.Controller):
    @http.route(['/events/<int:data_id>'], type="http", auth="public", website=True)
    def events_data(self, data_id):
        events = request.env['school.event'].browse(data_id)
        values = {
            'events': events
        }
        return request.render('school_management.Events', values)
