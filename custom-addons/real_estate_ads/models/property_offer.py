from email.policy import default

from odoo import fields, models, api, _
from datetime import timedelta
from odoo.exceptions import ValidationError
from odoo import release


# Abstract, Transient, Regular Model

class AbstractOffer(models.AbstractModel):
    _name = 'abstract.model.offer'
    _description = 'Abstract Offers'

    partner_email = fields.Char(string='Email')
    partner_phone = fields.Char(string='Phone')


class PropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _inherit = ['abstract.model.offer']
    _description = 'Estate Property Offers'

    @api.depends('property_id', 'partner_id')
    def _compute_name(self):
        for rec in self:
            if rec.property_id and rec.partner_id:
                rec.name = f"{rec.property_id.name} - {rec.partner_id.name}"
            else:
                rec.name = False

    name = fields.Char(string='Description', compute='_compute_name')

    price = fields.Float(string='Price')
    status = fields.Selection(
        [('accepted', 'Accepted'), ('refused', 'Refused')], string='Status')
    partner_id = fields.Many2one('res.partner', string='Customer')
    property_id = fields.Many2one('estate.property', string='Property')
    validity = fields.Integer(string='Validity')
    deadline = fields.Date(string='Deadline', compute='_compute_deadline', inverse='_inverse_deadline')

    # _sql_constraints = [
    #     ('check_validity', 'CHECK(validity > 0)', 'Deadline must be greater than creation date')
    # ]

    @api.model
    def _set_create_date(self):
        return fields.Date.today()

    creation_date = fields.Date(string='Create Date', default=_set_create_date)

    @api.depends('validity', 'creation_date')
    def _compute_deadline(self):
        for rec in self:
            if rec.creation_date:
                rec.deadline = rec.creation_date + timedelta(days=rec.validity)
            else:
                rec.deadline = False


    def _inverse_deadline(self):
        for rec in self:
            if rec.deadline and rec.creation_date:
                rec.validity = (rec.deadline -rec.creation_date).days
            else:
                rec.validity = False


    # @api.autovacuum
    # def _clean_offers(self):
    #     self.search([('status', '=', 'refused')]).unlink()

    @api.model_create_multi
    def create(self, vals):
        for rec in vals:
            if not rec.get('creation_date'):
                rec['creation_date'] = fields.Date.today()
        return super(PropertyOffer, self).create(vals)

    @api.constrains('validity')
    def _check_validity(self):
        for rec in self:
            if rec.deadline <= rec.creation_date:
                raise ValidationError(_('Deadline must be greater than creation date'))

    def action_accept_offer(self):
        self.status = 'accepted'

    def action_decline_offer(self):
        self.status = 'refused'

    def write(self, vals):
        # print(vals)

        print(self.env.cr)
        print(self.env.uid)
        print(self.env.context)

        # self.env['res.partner'].browse(1) # res.partner(1)
        # res_partner_ids = self.env['res.partner'].browse(10)
        # res_partner_ids = self.env['res.partner'].search_count([

        res_partner_ids = self.env['res.partner'].search([
         ('is_company', '=', True),

         # ('name', '=', vals.get('name')),
         # ], limit=6, offset=2, order='id DESC')
         # ]).mapped('phone')

        ]).filtered(lambda x: x.phone == '(870)-931-0505')
        print(res_partner_ids)

        # print(res_partner_ids.name)

        return super(PropertyOffer, self).write(vals)
