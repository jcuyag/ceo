from odoo import fields, models

class Partner(models.Model):
    _inherit = 'res.partner'

    instructor = fields.Boolean(string='Instructor', default=False)

    session_ids = fields.Many2many( string='Attendec Sessions', 
                                    readonly=True,
                                    comodel_name='openacademy.session')
    
    