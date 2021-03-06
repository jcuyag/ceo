# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class Wizard(models.TransientModel):
    _name = 'openacademy.wizard'

    def _default_sessions(self):
        return self.env['openacademy.session'].browse(self._context.get('active_ids'))
        
    attendee_ids = fields.Many2many(string='Attendees',
                                    comodel_name='res.partner')

    session_ids = fields.Many2many('openacademy.session',
        string="Sessions", required=True, default=_default_sessions)

    @api.multi
    def subscribe(self):
        for session in self.session_ids:
            _logger.debug()
            _logger.debug(session.attendee_ids)
            _logger.debug(self.attendee_ids)
            session.attendee_ids |= self.attendee_ids
        return {}