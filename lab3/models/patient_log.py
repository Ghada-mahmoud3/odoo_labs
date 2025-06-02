from odoo import models, fields

class PatientLog(models.Model):
    _name = 'hms.patient.log'
    _description = 'Patient State Log'
    _order = 'create_date desc'

    patient_id = fields.Many2one(
        'hms.patient',
        string='Patient',
        required=True,  # This makes it mandatory
        ondelete='cascade'  # Logs are deleted if patient is deleted
    )
    created_by = fields.Many2one('res.users', default=lambda self: self.env.user)
    date = fields.Datetime(string='Date',default=lambda self: fields.Datetime.now())
    description = fields.Text(string='Description')
    old_state = fields.Char(string='Old State')
    new_state = fields.Char(string='New State')