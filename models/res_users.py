from odoo import models, fields, api

class ResUsers(models.Model):
    _inherit = 'res.users'  # Inherit from the res.users model

    property_ids = fields.One2many(
        'estate.property',          # The model being referenced
        'salesperson_id',          # The field in the estate.property model that relates to this user
        string="Managed Properties",
        domain="[('availability', '=', True)]"  # Domain to list only available properties
    )

