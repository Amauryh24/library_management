from odoo import fields, models


class LibraryBookAuthor(models.Model):
    _name = 'library.book.author'
    _description = 'Library Book Author'

    name = fields.Char()
