from odoo import models, fields

class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Real Estate Property Type'

    name = fields.Char(string="Property Type", required=True)
    property_ids = fields.One2many(
        'estate.property',  # The model that this relates to
        'property_type_id',  # The field in estate.property that relates back to this type
        string="Properties"  # Label for the field
    )




	


	




	


	










