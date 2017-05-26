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

class EmployeeAddress(models.Model):
    _inherits = {'res.partner': 'address_id'}
    _name       = 'employee.address.inherits'

    employee_id      = fields.Many2one('hr.employee', string='Employee')
    city_id         = fields.Many2one('res.country.state',string='City')
    district_id     = fields.Many2one('res.country.state', string='District')
    subdistrict_id  = fields.Many2one('res.country.state', string='Sub-District')
    address_id      = fields.Many2one('res.partner',string='Address')
    type            = fields.Selection([
                                        ('default','Default'),
                                        ('home','Home'),
                                        ('mail','Mail'),
                                        ('working','Working')])

    full_address    = fields.Char('Address', compute='_compute_address')


    @api.multi
    @api.onchange('name', 'employee_id')
    def _onchange_city(self):
        for item in self:
            if item.employee_id:
                kota_temp = 'Alamat' + ' ' + item.employee_id.name
                item.name = kota_temp

    @api.multi
    @api.constrains('zip')
    def _constraint_zip(self):
        for item in self:
            val = item.zip
            if val==False:
                return True
            elif not val.isdigit():
                raise exceptions.ValidationError('Zip Code must be numeric')
            elif len(val) < 5 or len(val) > 6:
                raise exceptions.ValidationError('Zip Code must 5-6 character')

    @api.multi
    @api.depends('full_address', 'city_id', 'district_id', 'subdistrict_id', 'state_id', 'zip', 'street', 'type')
    def _compute_address(self):
        for item in self:
            if item.type=="working" and item.street and item.state_id and item.city_id and item.district_id and item.subdistrict_id and item.zip:
                temp = item.street +', '+item.subdistrict_id.name+', '+item.district_id.name+', '+item.city_id.name+', '+item.state_id.name+', '+item.zip
                item.full_address = temp
            elif item.type=="working" and item.street and item.state_id and item.city_id and item.district_id and item.zip:
                temp = item.street +', '+item.district_id.name+', '+item.city_id.name+', '+item.state_id.name+', '+item.zip
                item.full_address = temp
            elif item.type=="working" and item.street and item.state_id and item.city_id and item.zip:
                temp = item.street +', '+item.city_id.name+', '+item.state_id.name+', '+item.zip
                item.full_address = temp
            elif item.type=="working" and item.street and item.state_id and item.zip:
                temp = item.street +', '+item.state_id.name+', '+item.zip
                item.full_address = temp
            elif item.type=="working" and item.street and item.state_id and item.city_id and item.district_id and item.subdistrict_id:
                temp = item.street +', '+item.subdistrict_id.name+', '+item.district_id.name+', '+item.city_id.name+', '+item.state_id.name
                item.full_address = temp
            elif item.type=="working" and item.street and item.state_id and item.city_id and item.district_id:
                temp = item.street +', '+item.district_id.name+', '+item.city_id.name+', '+item.state_id.name
                item.full_address = temp
            elif item.type=="working" and item.street and item.state_id and item.city_id:
                temp = item.street +', '+item.city_id.name+', '+item.state_id.name
                item.full_address = temp
            elif item.type=="working" and item.street and item.state_id:
                temp = item.street +', '+item.state_id.name
                item.full_address = temp
