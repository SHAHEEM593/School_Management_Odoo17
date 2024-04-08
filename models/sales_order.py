# -*- coding: utf-8 -*-
from odoo import models, fields


class SalesStatus(models.Model):
    """status bar updated in sales module"""
    _inherit = 'sale.order'

    state = fields.Selection(selection_add=[('admitted', 'Admitted')])

    def status_admitted_action(self):
        """ to set the status to admitted when clicking the button"""
        self.state = 'admitted'
