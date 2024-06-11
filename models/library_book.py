from odoo import fields, models, api
from odoo.exceptions import ValidationError
# Information
# status.borrowed  -> when another user has the book
# status.travaling -> when the book is inside a book box


class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Library Book'

    name = fields.Char(string='Title', required=True, size=60)
    isbn = fields.Char(help='International Standard Book Number', size=17)

    status = fields.Selection([
        ('available', 'Available'),
        ('borrowed', 'Borrowed'),
        ('traveling', 'Traveling')
    ], string='Status', default='available')

    owner_id = fields.Many2one('res.users', string="Owner", default=lambda self: self.env.user)
    category_ids = fields.Many2many('library.book.category')
    author_id = fields.Many2one('library.book.author')

    _sql_constraints = [
        ('unique_isbn', 'UNIQUE(isbn)', 'The ISBN must be unique'),
    ]

    @api.constrains('isbn')
    def _check_isbn(self):
        if len(self.isbn.replace('-', '')) not in (10, 13):
            raise ValidationError("The ISBN must be either 10 or 13 digits long.")

        if not self.isbn.replace('-', '').isdigit():
            raise ValidationError("The ISBN must be only digits.")
