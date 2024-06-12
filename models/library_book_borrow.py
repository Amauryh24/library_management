from odoo import fields, models


class LibraryBookBorrow(models.Model):
    _name = 'library.book.borrow'
    _description = 'Library Book Borrow'

    borrow_date = fields.Date(string='Borrow Date', default=fields.Date.today)
    status = fields.Selection(
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        copy=False)

    borrower_id = fields.Many2one('res.partner', string='Borrower', required=True)
    book_id = fields.Many2one(comodel_name='library.book')
