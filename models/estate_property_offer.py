# estate_property_offer.py
from odoo import models, fields, api
from datetime import timedelta

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Real Estate Property Offer'

    price = fields.Float(string="Offer Price")
    status = fields.Selection(
        [('accepted', 'Accepted'), ('refused', 'Refused')],
        string="Status",
        copy=False  # No copy
    )
    partner_id = fields.Many2one(
        'res.partner',
        string="Partner",
        required=True
    )
    property_id = fields.Many2one(
        'estate.property',
        string="Property",
        required=True
    )
    property_type_id = fields.Many2one(
        'estate.property.type',
        string="Property Type",
        related='property_id.property_type_id',
        store=True
    )

    offer_count = fields.Integer(
        string="Offer Count",
        compute='_compute_offer_count'
    )

    # Validity field with default value
    validity = fields.Integer(string="Validity (Days)", default=7)

    # Date deadline computed field
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        store=True
    )

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for offer in self:
            if offer.create_date:
                offer.date_deadline = offer.create_date + timedelta(days=offer.validity)
            else:
                offer.date_deadline = False  # Prevent crashing when create_date is not set

    @api.onchange('date_deadline')
    def _onchange_date_deadline(self):
        for offer in self:
            if offer.date_deadline:
                # Calculate validity based on date_deadline
                if offer.create_date:
                    offer.validity = (offer.date_deadline - offer.create_date.date()).days

    def _inverse_date_deadline(self):
        for offer in self:
            if offer.create_date:
                offer.validity = (offer.date_deadline - offer.create_date.date()).days
