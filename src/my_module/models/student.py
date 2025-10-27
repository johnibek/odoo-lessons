from odoo import models, fields, api
import logging
from datetime import datetime


logger = logging.getLogger(__name__)

class Student(models.Model):
    _name = 'school.student'
    _description = 'Student'

    first_name = fields.Char(string="First Name", required=True)
    last_name = fields.Char(string="Last Name", required=True)
    full_name = fields.Char(string="Full Name", compute='_compute_full_name', store=True)
    age = fields.Integer(string="Age", required=True)
    phone = fields.Char(string="Phone", required=True, copy=True)  # copy=True by default
    email = fields.Char(string="Email", required=False, copy=False)
    grade = fields.Char(string="Grade", required=False, copy=False)

    @api.depends('first_name', 'last_name')
    def _compute_full_name(self):
        for student in self:
            student.full_name = f"{student.first_name} {student.last_name}"

    @api.onchange('age')
    def _onchange_age(self):
        if self.age < 7:
            self.grade = 'Kindergarten'

        elif 7 < self.age < 10:
            self.grade = 'Primary school'

        else:
            self.grade = 'High school'

    @api.model_create_multi
    def create(self, vals_list):
        print(vals_list)
        res = super().create(vals_list)
        print(res)
        return res

    def custom_method(self):
        print("Button clicked!")
        student = self.browse(1)
        new_data = {
            "email": "sample.email@gmail.com"
        }
        student.write(new_data)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def cleanup_inactive_partners(self):
        partners = self.search([('active', '=', False)])
        count = len(partners)

        if partners:
            partners.unlink()

        logger.info(f"{count} inactive partners deleted at {datetime.now()}")
