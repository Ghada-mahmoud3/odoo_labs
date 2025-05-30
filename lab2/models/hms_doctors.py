from odoo import models, fields
class HMSDoctor(models.Model):
    _name = 'hms.doctor'
    _description = 'Hospital Doctor'
    first_name=fields.Char(required=True)
    last_name = fields.Char(required=True)
    image=fields.Binary()