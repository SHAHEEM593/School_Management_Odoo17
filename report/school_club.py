# -*- coding: utf-8 -*-
from odoo import models, api


class SchoolClubReport(models.AbstractModel):
    _name = 'report.school_management.school_club_template'

    @api.model
    def _get_report_values(self, docids, data=None):
        return {
            'doc_ids': docids,
            'doc_model': 'school.club',
            'data': data,
        }
