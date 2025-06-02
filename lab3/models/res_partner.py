from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError

class ResPartner(models.Model):
    _inherit = 'res.partner'
    _description = 'Contact'  # Required for inherited models

    related_patient_id = fields.Many2one(
        'hms.patient',
        string='Related Patient',
        tracking=True,
        ondelete='restrict'  # Prevent accidental deletion
    )
    
    # Make Tax ID mandatory
    vat = fields.Char(
        string='Tax ID',
        required=True,
        help="Tax Identification Number"
    )

    @api.constrains('related_patient_id', 'email')
    def _check_patient_email_uniqueness(self):
        for partner in self.filtered('related_patient_id'):
            if partner.email:
                conflict = self.search([
                    ('email', '=', partner.email),
                    ('related_patient_id', '!=', False),
                    ('id', '!=', partner.id)
                ], limit=1)
                if conflict:
                    raise ValidationError(_(
                        'Email %s already used by customer %s',
                        partner.email, conflict.name
                    ))

    def unlink(self):
        protected = self.filtered('related_patient_id')
        if protected:
            raise UserError(_(
                'Cannot delete customers linked to patients: %s',
                ', '.join(protected.mapped('name'))
            ))
        return super().unlink()