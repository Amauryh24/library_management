from odoo import fields, models, api
from odoo.exceptions import ValidationError

# Information
# status.unavailable    -> The owner doesn't want to borrow the book
# status.available      -> The book can be borrow
# status.borrowed       -> The book is borrowed
# borrower_id           -> The owner accepted to borrow his book
# borrow_ids            -> The borrowing request


class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Library Book'

    name = fields.Char(string='Title', required=True, size=60)
    publication_date = fields.Date()
    pages = fields.Integer(default=0)
    isbn = fields.Char(help='International Standard Book Number', size=17, copy=False)
    state = fields.Selection(
        selection=[
            ('unavailable', 'Unavailable'),
            ('available', 'Available'),
            ('borrowed', 'Borrowed'),
            ('lost', 'Lost')
        ], string='State', default='available', group_expand='_expand_states')
    color = fields.Integer(string="Color")

    owner_id = fields.Many2one(comodel_name='res.users', string="Owner", default=lambda self: self.env.user)
    owner_street = fields.Char(related="owner_id.partner_id.street")
    borrower_id = fields.Many2one('res.partner', string="Borrower", copy=False, readonly=True)
    category_ids = fields.Many2many('library.book.category')
    author_id = fields.Many2one('library.book.author')
    borrow_ids = fields.One2many('library.book.borrow', 'book_id', string='Borrows')

    _sql_constraints = [
        ('check_pages', 'CHECK(pages > 0)', 'The number of pages must be stricly positive.'),
        ('unique_isbn', 'UNIQUE(isbn)', 'The ISBN must be unique'),
    ]

    @api.constrains('isbn')
    def _check_isbn(self):
        if len(self.isbn.replace('-', '')) not in (10, 13):
            raise ValidationError("The ISBN must be either 10 or 13 digits long.")

        if not self.isbn.replace('-', '').isdigit():
            raise ValidationError("The ISBN must be only digits.")

    def action_set_state(self):
        for record in self:
            record.state = self.env.context.get('state')
        return True

    def _expand_states(self, states, domain, order):
        return [key for key, val in type(self).state.selection]
