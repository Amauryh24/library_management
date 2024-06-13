from odoo import fields, models, api


class LibraryBookBorrow(models.Model):
    _name = 'library.book.borrow'
    _description = 'Library Book Borrow'

    borrow_date = fields.Date(string='Borrow Date', default=fields.Date.today)
    status = fields.Selection(
        selection=[('accepted', 'Accepted'), ('onhold', 'On hold'), ('refused', 'Refused')],
        copy=False)

    borrower_id = fields.Many2one('res.partner', string='Borrower', required=True)
    borrower_address = fields.Char(string="Street", compute="_compute_address")
    book_id = fields.Many2one(comodel_name='library.book')

    def action_set_status_accepted(self):
        for record in self:
            record.status = "accepted"

            # One offer can be accepted
            self.search([
                ('book_id', '=', record.book_id.id),
                ('id', '!=', record.id),
                ('status', '!=', 'refused')]
            ).write({'status': 'onhold'})

            record.book_id.borrower_id = record.borrower_id
            record.book_id.state = 'borrowed'

            return True

    def _update_book_state(self, book_id):
        count_all_record = self.search_count([('book_id', '=', book_id)])
        count_no_accepted_record = self.search_count(
            [('book_id', '=', book_id), ('status', 'in', ['onhold', 'refused'])])
        if count_all_record == count_no_accepted_record:
            book = self.env['library.book'].browse(book_id)
            book.state = 'available'

    def action_set_status_refused(self):
        for record in self:
            record.status = "refused"

            self._update_book_state(record.book_id.id)
        return True

    def action_set_status_onhold(self):
        for record in self:
            record.status = "onhold"
            self._update_book_state(record.book_id.id)

        return True

    @api.depends("borrower_id")
    def _compute_address(self):
        for rec in self:
            rec.borrower_address = rec.borrower_id.street
