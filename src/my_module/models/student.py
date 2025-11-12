from odoo import models, fields, api
import logging
from datetime import datetime
import os, base64


logger = logging.getLogger(__name__)

class Student(models.Model):
    _name = 'school.student'
    _description = 'Student'
    _rec_name = 'full_name'
    _rec_names_search = ['first_name', 'last_name', 'phone', 'email']

    first_name = fields.Char(string="First Name", required=True)
    last_name = fields.Char(string="Last Name", required=True)
    full_name = fields.Char(string="Full Name", compute='_compute_full_name', store=True)
    age = fields.Integer(string="Age", required=True)
    phone = fields.Char(string="Phone", required=True, copy=True)  # copy=True by default
    email = fields.Char(string="Email", required=False, copy=False)
    grade = fields.Char(string="Grade", required=False, copy=False)
    is_active = fields.Boolean(string="Is Active", default=False)
    country = fields.Many2one('res.country', string="Country")

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

    @api.onchange('first_name', 'last_name')
    def set_email(self):
        for rec in self:
            if rec.first_name and rec.last_name:
                rec.email = f"{rec.first_name[0].lower()}.{rec.last_name.lower()}@gmail.com"

    def custom_method(self):
        print("Button clicked!")
        student = self.browse(1)
        new_data = {
            "email": "sample.email@gmail.com"
        }
        student.write(new_data)

    @api.model
    def name_create(self, name):
        print(name)
        rtn = super().create({'first_name': name, 'last_name': name, 'age': 20, 'phone': '+998901234567'})
        return rtn.id, rtn.display_name


class StudentScore(models.Model):  # Just for learning purposes
    _name = 'student.score'
    _description = 'Student Score'

    student_id = fields.Many2one('school.student', string="Student", ondelete='cascade')
    exam_score = fields.Float(string="Exam Score")


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def cleanup_inactive_partners(self):
        partners = self.search([('active', '=', False)])
        count = len(partners)

        if partners:
            partners.unlink()

        logger.info(f"{count} inactive partners deleted at {datetime.now()}")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            current_file_path = os.path.abspath(__file__)
            current_dir = os.path.dirname(current_file_path)
            module_dir = os.path.dirname(current_dir)
            img_path = vals.pop('image_1920', None)

            img_exists = os.path.isfile(module_dir + img_path) if img_path else False
            if img_exists:
                with open(module_dir + img_path, 'rb') as img:
                    img_base64 = base64.b64encode(img.read()).decode('utf-8')
                    print(img_base64)
                    vals['image_1920'] = img_base64


        super(ResPartner, self).create(vals_list)

