from odoo import fields, models, api
from odoo.exceptions import ValidationError

# Information
# status.borrowed   -> when another user has the book
# status.travaling  -> when the book is inside a book box
# borrower_id       -> The owner accepted to borrow his book
# borrow_ids        -> The borrowing request


class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Library Book'

    name = fields.Char(string='Title', required=True, size=60)
    isbn = fields.Char(help='International Standard Book Number', size=17)
    state = fields.Selection(
        selection=[
            ('unavailable', 'Unavailable'),
            ('available', 'Available'),
            ('borrowing', 'Borrowing'),
            ('traveling', 'Traveling'),
            ('lost', 'Lost')
        ], string='State', default='available')
    color = fields.Integer(string="Color")

    owner_id = fields.Many2one('res.users', string="Owner", default=lambda self: self.env.user)
    borrower_id = fields.Many2one('res.partner', string="Borrower", copy=False, readonly=True)
    category_ids = fields.Many2many('library.book.category')
    author_id = fields.Many2one('library.book.author')
    borrow_ids = fields.One2many('library.book.borrow', 'book_id', string='Borrows')

    _sql_constraints = [
        ('unique_isbn', 'UNIQUE(isbn)', 'The ISBN must be unique'),
    ]

    @api.constrains('isbn')
    def _check_isbn(self):
        if len(self.isbn.replace('-', '')) not in (10, 13):
            raise ValidationError("The ISBN must be either 10 or 13 digits long.")

        if not self.isbn.replace('-', '').isdigit():
            raise ValidationError("The ISBN must be only digits.")

    def action_set_available(self):
        for record in self:
            record.state = "available"
        return True
