from sqlite3.dbapi2 import apilevel

import re
from datetime import datetime

from odoo import models, fields,api
from odoo.exceptions import ValidationError
class HMSPatient(models.Model):
    _name = 'hms.patient'
    _description = 'Hospital Patient'


    # _rec_name = "age"
    first_name= fields.Char()
    last_name= fields.Char()
    birth_date= fields.Date()
    history= fields.Html()
    cr_ratio= fields.Float()
    blood_type= fields.Selection([ ('a','A'), ('b', 'B'),('ab', 'AB'), ('o', 'O')])
    pcr= fields.Boolean()
    image= fields.Binary()
    address= fields.Text()
    age = fields.Integer(compute='_compute_age', store=True, readonly=True)
    state = fields.Selection([
        ('undetermined', 'Undetermined'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('serious', 'Serious')
    ], default='undetermined', string='State')
    email = fields.Char(string="Email", required=True)
    department_id = fields.Many2one('hms.department')
    doctor_ids=fields.Many2many('hms.doctor',readonly=True)
    department_capacity=fields.Integer(related='department_id.capacity', readonly=True)

    @api.onchange('age')
    def _onchange_age(self):
        if self.age and self.age < 30:
            self.pcr = True
            return {
                'warning': {
                    'title': 'Warning',
                    'message': 'PCR has been automatically checked because the patient is under 30 years old.'
                }
            }

    # @api.onchange('department_id')
    # def _check_department_status(self):
    #     if self.department_id and self.department_id.is_opened:
    #         self.department_id = False
    #         return {
    #             'warning': {
    #                 'title': 'Error',
    #                 'message': 'Cannot select a closed department.'
    #             },
    #         }

    @api.onchange('pcr')
    def _onchange_pcr(self):
        if self.pcr:
            self.cr_ratio = None
            return {
                'warning': {
                    'title': 'Warning',
                    'message': 'CR ratio is now mandatory since PCR is checked.'
                }
            }
    @api.constrains('email')
    def check_email(self):
        for record in self:
            if record.email:
                if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", record.email):
                    raise ValidationError("Invalid email format.")
                if self.env['hms.patient'].search([('email', '=', record.email), ('id', '!=', record.id)]):
                    raise ValidationError("This email is already used by another patient.")

    @api.depends('birth_date')
    def _compute_age(self):
        today = datetime.today().date()
        for record in self:
            if record.birth_date:
                birth_date = fields.Date.from_string(record.birth_date)
                age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
                record.age = age
            else:
                record.age = 0