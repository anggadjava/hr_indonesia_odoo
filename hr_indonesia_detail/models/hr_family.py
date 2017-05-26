
from openerp import models, fields, api, exceptions
import re
from psycopg2 import OperationalError
from openerp import SUPERUSER_ID
from datetime import datetime, date, time
from openerp.exceptions import ValidationError
from openerp.tools.translate import _
from dateutil.relativedelta import *
import calendar
from openerp.tools import (DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT)
class HrFamily(models.Model):

    _name = 'hr.family'

    name            = fields.Char('Name', required=True)
    active_status  = fields.Boolean('Active')
    status          = fields.Many2one('hr.status.family',required=True)
    gender      = fields.Selection([
        ('male', 'Male'),
        ('female','Female')], required=True)
    identif_no  = fields.Char('Identification No')
    job_id      = fields.Many2one('hr.family.job','Last Job')
    parent_id   = fields.Many2one('hr.employee', 'Parent')
    birthdate   = fields.Date('Birth Date', required=True)
    birthplace  = fields.Many2one('res.country.state', domain=[('regional_level','=','city')], required=True)
    birthplace_date = fields.Char(compute='compute_date_place')
    checking    = fields.Boolean('Checking', compute='compute_checking')
    marital     = fields.Selection([('single','Single'),('married','Married'),('divorced', 'Divorced')])
    age         = fields.Integer('Age', compute='_compute_age')
    ticket      = fields.Selection([('covered','Covered'),('not_covered','Not Covered')])
    health      = fields.Selection([('covered', 'Covered'), ('not_covered', 'Not Covered')])

    @api.multi
    @api.depends('birthdate')
    def _compute_age(self):
        for item in self:
            if item.birthdate == False:
                return True
            else:
                fmt='%Y-%m-%d'
                datenow= datetime.today()
                birthdate = item.birthdate

                conv_bitrhdate = datetime.strptime(str(birthdate),fmt)
                init_birthdate =conv_bitrhdate.date()

                result_year = datenow.year - init_birthdate.year - ((datenow.month, init_birthdate.day) < (init_birthdate.month, init_birthdate.day))

                item.age=result_year

    @api.multi
    @api.depends('birthdate','birthplace','birthplace_date', 'age')
    def compute_date_place(self):
        for item in self:
            if item.birthdate and item.birthplace :
                place_date = item.birthplace.name + ', ' + str(item.birthdate)+' (Age '+str(item.age)+')'
                item.birthplace_date = place_date

    @api.multi
    @api.depends('checking','birthdate','birthplace','birthplace_date')
    def compute_checking(self):
        for item in self:
            if item.birthdate and item.birthplace :
                item.checking=True
            elif item.birthplace_date:
                item.checking=False
            else:
                item.checking=False

    @api.multi
    @api.constrains('name')
    def _constraint_name(self):
        for item in self:
            if bool(re.search(r'\d', item.name)):
                raise exceptions.ValidationError("Fields name family contain alphabet only")
            elif len(item.name) < 3 or len(item.name) > 30:
                raise exceptions.ValidationError('Name family must be 3-5 character')

    @api.multi
    @api.constrains('identif_no')
    def _constraint_identif_no(self):
        for item in self:
            val = item.identif_no
            if val==False:
                return True
            elif not val.isdigit():
                raise exceptions.ValidationError('Identification No. family must be numeric')

class HrFamilyJob(models.Model):
    _name       = 'hr.family.job'
    _inherits   = {'hr.job' : 'job_id'}

    job_id      = fields.Many2one('hr.job','Job')


class HrStatusFamily(models.Model):
    _name       = 'hr.status.family'

    name        = fields.Char('Status')

