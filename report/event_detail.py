# -*- coding: utf-8 -*-
from odoo import models, api


class LeaveInformationReport(models.AbstractModel):
    _name = 'report.school_management.event_details_template'

    @api.model
    def _get_report_values(self, docids, data=None):
        return {
            'doc_ids': docids,
            'doc_model': 'school.event',
            'data': data,
        }
