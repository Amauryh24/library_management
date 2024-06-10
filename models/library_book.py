from odoo import fields, models


class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Library Book'

    name = fields.Char(string='Title', required=True)
    author = fields.Char(string='Author')
    isbn = fields.Integer()

    # Borrowed  -> when another user has the book
    # Travaling -> when the book is inside a book box
    status = fields.Selection([
        ('available', 'Available'),
        ('borrowed', 'Borrowed'),
        ('traveling', 'Traveling')
    ], string='Status', default='available')

    owner_id = fields.Many2one('res.users', string="Owner", default=lambda self: self.env.user)
    category_id = fields.Many2one('library.book.category')
    author_id = fields.Many2one('library.book.author')
