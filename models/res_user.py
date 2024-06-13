from odoo import fields, models


class Users(models.Model):
    _inherit = 'res.users'

    book_ids = fields.One2many("library.book", "owner_id", domain=lambda self: [('state', '=', 'available')])
