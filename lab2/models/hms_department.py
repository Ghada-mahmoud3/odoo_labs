from email.policy import default

from odoo import models, fields
class HMSDepartment(models.Model):
    _name = 'hms.department'
    _description = 'Hospital Department'
    name=fields.Char(required=True)
    capacity=fields.Integer()
    is_opened = fields.Boolean(string='Is Opened', default=True)
    patient_ids = fields.One2many('hms.patient', 'department_id', string='Patients')