from odoo import models, fields, api
from odoo.exceptions import ValidationError
import logging

logger = logging.getLogger(__name__)


class Product(models.Model):
    _name = "custom.product"
    _description = "Product Model"

    name = fields.Char(string="Product Name", required=True)
    amount = fields.Float(string="Product Amount", required=True)
    price = fields.Monetary(string="Product Price", required=True, currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', string="Currency", required=True)
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ('pending', 'Pending'),
            ('done', 'Done')
        ], default="draft", string="Product State", group_expand="_read_product_states"
    )
    quality = fields.Selection(
        [
            ('1', 'Low'),
            ('2', 'Medium'),
            ('3', 'High')
        ]
    )
    status = fields.Selection(
        [
            ('not_started', 'Not Started'),
            ('started', 'Started'),
            ('finished', 'Finished')
        ], default='not_started'
    )

    @api.model
    def default_get(self, fields_list):
        print(fields_list)
        rtn = super(Product, self).default_get(fields_list)
        rtn['amount'] = 20
        rtn['name'] = 'Sample Product'
        rtn['quality'] = '3'
        print(rtn)
        return rtn

    @api.model
    def _read_product_states(self, values, domain):
        return [key for key, label in self._fields['state'].selection]

    @api.model
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = f"{self.name} - {self.amount}"

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('amount') < 0:
                raise ValidationError("Amount cannot be negative")

        records = super(Product, self).create(vals_list)

        for record in records:
            logger.info(f"Product {record.name} created")

        return records

    def write(self, vals):
        if 'amount' in vals and vals['amount'] < 0:
            raise ValidationError("Amount cannot be negative")

        # if self.filtered(lambda rec: rec.state == 'done'):
        #     raise ValidationError("Completed product cannot be changed")

        result = super(Product, self).write(vals)
        for rec in self:
            logger.info("Product %s updated", rec.name)

        return result

    def unlink(self):
        for rec in self:
            if rec.state == 'done':
                raise ValidationError("Completed product cannot be deleted.")

        res = super(Product, self).unlink()
        print(res)
        logger.info("Product deleted.")

        return res

    def action_done(self):
        for rec in self:
            rec.state = 'done'

    def action_draft(self):
        for rec in self:
            rec.state = 'draft'
