# -*- coding: utf-8 -*-
from odoo import models, api


class ExamDetailsReport(models.AbstractModel):
    _name = 'report.school_management.exam_detail_template'

    @api.model
    def _get_report_values(self, docids, data=None):
        return {
            'doc_ids': docids,
            'doc_model': 'school.exam',
            'data': data,
        }
