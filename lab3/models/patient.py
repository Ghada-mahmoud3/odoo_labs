from odoo import models, fields, api, _
from datetime import date  
import re
from odoo.exceptions import ValidationError


class Patient(models.Model):
    _name = 'hms.patient'
    _description = 'Hospital Patient'
    _inherit = ['mail.thread']
    first_name = fields.Char(string='First Name', required=True)
    last_name = fields.Char(string='Last Name', required=True)
    birth_date = fields.Date(string='Birth Date')
    age = fields.Integer(string='Age', compute='_compute_age', store=True)
    blood_type = fields.Selection([
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    ], string='Blood Type')
    pcr = fields.Boolean(string='PCR')
    image = fields.Binary(string='Image')
    history = fields.Html(string='Medical History')
    address = fields.Text(string='Address')
    cr_ratio = fields.Float(string='CR Ratio')
    department_id = fields.Many2one('hms.department', string='Department')
    doctor_ids = fields.Many2many('hms.doctor', string='Doctors', domain="[('department_id', '=', department_id)]" )
    log_ids = fields.One2many('hms.patient.log', 'patient_id', string='History Logs')
    state = fields.Selection([
        ('undetermined', 'Undetermined'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('serious', 'Serious'),
    ], default='undetermined')
    email = fields.Char(
        string='Email'
    )
    @api.constrains('email')
    def _check_valid_email(self):
        for record in self:
            if record.email:
                if not re.match(r'^[^@]+@[^@]+\.[^@]+$', record.email):
                    raise ValidationError(_('Please enter a valid email address'))
  
    def write(self, vals):
        if 'state' in vals and vals['state'] != self.state:
            self.env['hms.patient.log'].create({
                'patient_id': self.id,
                'description': f"State changed to {dict(self._fields['state'].selection).get(vals['state'])}"
            })
        return super(Patient, self).write(vals)
        
    @api.model
    def create(self, vals):
        # Set default state if not provided
        if 'state' not in vals:
            vals['state'] = 'undetermined'
        return super().create(vals)

    @api.depends('birth_date')
    def _compute_age(self):
        today = date.today()
        for patient in self:
            if patient.birth_date:
                delta = today - patient.birth_date
                patient.age = delta.days // 365
                if patient.age < 30 and not patient.pcr:
                    patient.pcr = True
                    return {
                        'warning': {
                            'title': "PCR Auto-Checked",
                            'message': "PCR was automatically checked because patient is under 30 years old",
                        }
                    }
            else:
                patient.age = 0


    # @api.onchange('state')
    # def _onchange_state(self):
    #     if self.state:
    #         self.env['hms.patient.log'].create({
    #             'patient_id': self.id,
    #             'description': f"State changed to {self.state}",
    #             'old_state': self._origin.state if self._origin else '',
    #             'new_state': self.state
    #         })

    @api.onchange('department_id')
    def _onchange_department(self):
        if self.department_id and not self.department_id.is_opened:
            self.department_id = False
            return {
                'warning': {
                    'title': "Closed Department",
                    'message': "You cannot select a closed department!",
                }
            }
    
    _sql_constraints = [
        ('check_cr_ratio_if_pcr', 
        'CHECK(pcr = False OR cr_ratio IS NOT NULL)',
        'CR Ratio is required when PCR is checked.'),
        ('email_unique', 'UNIQUE(email)', 'Email must be unique!'),
    ]