from odoo import fields, models, api
from datetime import date
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError


class LibraryBookAuthor(models.Model):
    _name = 'library.book.author'
    _description = 'Library Book Author'

    name = fields.Char(string="Author Name", required=True, size=60)
    born_date = fields.Date(default=date.today() - relativedelta(years=18))
    image = fields.Image(string="Image", help="Select your image here", max_width=150, max_height=150)
    # image = fields.Binary(string="Image", help="Select your image here")

    @api.constrains('name')
    def _check_unique_name_case_sensitive(self):
        author_ids = self.search([]) - self
        value = [rec.name.lower() for rec in author_ids]
        if self.name and self.name.lower() in value:
            raise ValidationError("The author [%s] already exists!" % self.name.lower())
        return True

    @api.constrains('born_date')
    def _check_born_date_is_major(self):
        if self.born_date >= fields.date.today() - relativedelta(years=18):
            raise ValidationError("The author must be at least 18 years old!")
