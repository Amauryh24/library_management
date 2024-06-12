from odoo import fields, models, api
from odoo.exceptions import ValidationError


class LibraryBookCategory(models.Model):
    _name = 'library.book.category'
    _description = 'Library Book Category'

    name = fields.Char(required=True, size=30)
    color = fields.Integer(string="Color")

    # https://www.odoo.com/ro_RO/forum/suport-1/odoo-14-unique-values-but-how-to-prevent-with-spelling-mistakes-182159
    @api.constrains('name')
    def _check_unique_name_case_sensitive(self):
        category_ids = self.search([]) - self
        value = [rec.name.lower() for rec in category_ids]
        if self.name and self.name.lower() in value:
            raise ValidationError("The category [%s] already exists!" % self.name.lower())
        return True
