# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Wizard(models.Model):
    _name = 'openacademy.wizard'

    def _default_session(self):
        return self.env['openacademy.session'].browse(self._context.get('active_id'))

    session_id = fields.Many2one(string='Session',
                                 required=True,
                                 default=_default_session,
                                 comodel_name='openacademy.session')
    attendee_ids = fields.Many2many(string='Attendees',
                                    comodel_name='res.partner')