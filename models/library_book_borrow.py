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

    def action_set_status_accepted(self):
        for record in self:
            record.status = "accepted"

            # One offer can be accepted
            self.search([
                ('book_id', '=', record.book_id.id),
                ('id', '!=', record.id)]
            ).write({'status': 'refused'})

            # Update borrower and status book
            record.book_id.borrower_id = record.borrower_id
            record.book_id.state = 'borrowed'

            return True

    def action_set_status_refused(self):
        for records in self:
            records.status = "refused"
            return True
