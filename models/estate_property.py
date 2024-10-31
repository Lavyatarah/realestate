from datetime import date, timedelta  # Import the required modules
from odoo import models, fields, api
from odoo.exceptions import ValidationError  # Import ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero  # Import float comparison utilities

class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Real Estate Property'

    name = fields.Char(string="Title", required=True)

    # Add the Many2many relationship for tags
    tag_ids = fields.Many2many(
        'estate.property.tag',
        string="Tags"
    )

    buyer_id = fields.Many2one(
        'res.partner',
        string="Buyer",
        copy=False  # Do not copy the buyer field
    )
    salesperson_id = fields.Many2one(
        'res.users',
        string="Salesperson",
        default=lambda self: self.env.user  # Default to current user
    )

    property_type_id = fields.Many2one(
        'estate.property.type',
        string="Property Type"
    )

    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")

    date_availability = fields.Date(
        string="Date of Availability",
        default=lambda self: fields.Date.to_string(date.today() + timedelta(days=90)),
        copy=False  # Prevent copyingfv
    )
    expected_price = fields.Float(string="Expected Price")  # Add expected price field
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False)  # Read-only and prevent copying
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer(string="Number of Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area (sqm)")

    # Total area computed as the sum of living_area and garden_area
    total_area = fields.Float(string="Total Area (sqm)", compute="_compute_total_area", store=True)

    # Best offer price computed from related offers
    best_price = fields.Float(string="Best Offer Price", compute="_compute_best_price", store=True)

    # Define garden orientation choices
    garden_orientation = fields.Selection(
        [
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')
        ],
        string="Garden Orientation"
    )
    active = fields.Boolean('Active', default=True)

    state = fields.Selection(
        [
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled')
        ],
        string="State",
        required=True,
        default='new',  # Default value set to 'New'
        copy=False  # Prevent copying
    )

    # Add the One2many relationship for offers
    offer_ids = fields.One2many(
        'estate.property.offer',  # Model name for the offers
        'property_id',           # Field in the offer model that relates to this property
        string="Offers"          # Label for the field
    )

    validity = fields.Integer(string="Validity (Days)", default=7)  # Default to 7 days
    date_deadline = fields.Date(string="Deadline Date", compute="_compute_date_deadline", store=True)
    availability = fields.Boolean(string="Available", default=True)  # Add availability field

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for property in self:
            property.total_area = (property.living_area or 0) + (property.garden_area or 0)

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for property in self:
            property.best_price = max(property.offer_ids.mapped('price') or [0])

    @api.depends('validity', 'create_date')
    def _compute_date_deadline(self):
        for property in self:
            if property.create_date:
                # Compute the date_deadline as the sum of create_date and validity
                deadline_date = property.create_date + timedelta(days=property.validity)
                property.date_deadline = fields.Date.to_string(deadline_date)
            else:
                property.date_deadline = False  # Fallback if create_date is not available

    @api.onchange('garden')
    def _onchange_garden(self):
        """Set garden area and orientation based on garden field."""
        if self.garden:
            self.garden_area = 10  # Set default garden area
            self.garden_orientation = 'north'  # Set default orientation
        else:
            self.garden_area = 0  # Clear the garden area
            self.garden_orientation = False  # Clear the orientation

    @api.model
    def unlink(self):
        for property in self:
            if property.state not in ['new', 'cancelled']:
                raise ValidationError("You cannot delete a property that is not 'New' or 'Cancelled'.")
        return super(EstateProperty, self).unlink()
    # Add SQL constraints
    _sql_constraints = [
        ('expected_price_positive', 'CHECK(expected_price > 0)', 'The expected price must be strictly positive.'),
        ('selling_price_positive', 'CHECK(selling_price > 0)', 'The selling price must be strictly positive.'),
    ]

    # Add Python constraint to check selling price
    @api.constrains('expected_price', 'selling_price')
    def _check_selling_price(self):
        for property in self:
            if not float_is_zero(property.expected_price, precision_digits=2) and property.selling_price:
                # Check if selling price is less than 90% of expected price
                if float_compare(property.selling_price, property.expected_price * 0.9, precision_digits=2) < 0:
                    raise ValidationError("The selling price cannot be lower than 90% of the expected price.")
