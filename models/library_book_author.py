from odoo import fields, models
# from odoo.tools import image_guess_size_from_field_name


class LibraryBookAuthor(models.Model):
    _name = 'library.book.author'
    _description = 'Library Book Author'

    name = fields.Char(string="Author Name", required=True,)
    born_date = fields.Date()
    image = fields.Image(string="Image", help="Select your image here", max_width=150, max_height=150)
