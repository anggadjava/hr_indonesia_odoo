from openerp import models, fields, api, exceptions
import re

from psycopg2 import OperationalError

from openerp import SUPERUSER_ID
from datetime import datetime, date, time

class HrEducation(models.Model):
    _name = 'hr.education'
    _rec_name = 'nama'

    nama = fields.Char('Nama')
    education_type = fields.Many2one('hr.education.type')
    country_id = fields.Many2one('res.country',string='Country')


class HrEducationDetail(models.Model):
    _name = 'hr.education.detail'

    name                = fields.Char('Nama' )
    education_type      = fields.Many2one('hr.education.type')
    education_id        = fields.Many2one('hr.education','Education ID')
    parent_id           = fields.Many2one('hr.employee', 'Parent')
    start_date          = fields.Date('Start Date')
    end_date            = fields.Date('End Date')
    country_id          = fields.Many2one('res.country', string='Country')
    gpa                 = fields.Float('Index/GPA')
    image_certificate   = fields.Binary('Upload certificate')
    certificate_name    = fields.Char()

    type = fields.Selection([
        ('staterun', 'State Run School'),
        ('private', 'Private School')])

    @api.multi
    @api.onchange('education_id','country_id')
    def _onchange_education_id(self):

        for item in self:
            if item.education_type and item.country_id:
                return {
                    'domain' : {
                        'education_id' : [('education_type','=',item.education_type.id),('country_id','=',item.country_id.id)]
                    }
                }

    @api.one
    @api.constrains('certificate_name')
    def _check_certificate_name(self):
        if self.certificate_name:
            if not self.certificate_name:
                raise exceptions.ValidationError("There is no file")
            else:
                # Check the file's extension
                tmp = self.certificate_name.split('.')
                ext = tmp[len(tmp) - 1]
                if ext != 'jpg' and ext != 'img' and ext != 'jpeg' and ext != 'png' and ext != 'pdf':
                    raise exceptions.ValidationError(
                        "Certificate file must be a img, png, jpg, jpeg, or pdf file")

    @api.multi
    @api.constrains('gpa','education_type')
    def _check_gpa(self):
        for item in self:
            val=item.gpa
            edutype=item.education_type
            if val>100:
                raise exceptions.ValidationError("Range Index/GPA is 0.00-100.00")
            elif val<0:
                raise  exceptions.ValidationError("Range Index/GPA is 0.00-100.00")



class HrEducationType(models.Model):
    _name       = 'hr.education.type'

    name        = fields.Char('Education Type')