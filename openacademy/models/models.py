# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Course(models.Model):
    _name = 'openacademy.course'

    name = fields.Char(string='Title', required=True,)
    description = fields.Text()

    responsible_id = fields.Many2one(string='Responsible',
                                     index=True,
                                     comodel_name='res.users',
                                     ondelete='set null' 
                                    )

    session_id = fields.One2many(string='Sessions',
                                 comodel_name='openacademy.session',
                                 inverse_name='course_id'
                                )

class Session(models.Model):
    _name = 'openacademy.session'
    
    name = fields.Char(required=False)
    start_date = fields.Date(default=fields.Date.today)
    duration = fields.Float(digits=(6, 2), help='Duration Days')
    seats = fields.Integer(string='Number of Seats')
    active = fields.Boolean(default=True)

    instructor_id = fields.Many2one(string='Responsible', 
                                    comodel_name='res.partner',
                                    domain=['|',('instructor','=', True),
                                            ('category_id.name','ilike', 'Teacher')]
                                    )
    course_id = fields.Many2one(string='Course', 
                                comodel_name='openacademy.course',
                                ondelete="cascade",
                                required=True )
    attendee_ids = fields.Many2many(string='Attendees', 
                                    comodel_name='res.partner')

    taken_seats = fields.Float(string='Taken seats', 
                               compute='_taken_seats')
    
    @api.depends('seats', 'attendee_ids')
    def _taken_seats(self):
        for r in self:
            if not r.seats:
                r.taken_seats = 0.0
            else:
                r.taken_seats = 100.0 * len(r.attendee_ids) / r.seats

    @api.onchange('seats', 'attendee_ids')
    def _verify_valid_seats(self):
        if self.seats < 0:
            return {
                'warning' : {
                    'title':"Incorrect 'seats' value",
                    'message':"The number of available seats may not be negative."
                },
            }
        if self.seats < len(self.attendee_ids):
            return {
                'warning': {
                    'title': "Too many attendees",
                    'message':"Increase seats or remove excess attendees",
                },
            }
    