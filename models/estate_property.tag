# estate_property_tag.py
from odoo import models, fields

class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Real Estate Property Tag'

    name = fields.Char(string="Tag Name", required=True)
