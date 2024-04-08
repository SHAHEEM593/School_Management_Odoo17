# -*- coding: utf-8 -*-
from odoo import models, api


class StudentInformationReport(models.AbstractModel):
    _name = 'report.school_management.student_information_template'

    @api.model
    def _get_report_values(self, docids, data=None):
        return {
            'doc_ids': docids,
            'doc_model': 'students.registration',
            'data': data,
        }
