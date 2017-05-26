# -*- coding: utf-8 -*-

from openerp import models, fields, api, exceptions


class InheritResCountryState(models.Model):
    _inherit = 'res.country.state'
    _order   = 'name asc'

    regional_level  = fields.Selection([
        ('province', 'Province'),
        ('city', 'City'),
        ('district', 'District'),
        ('subdistrict', 'Sub-District')])
    parent_id       = fields.Many2one('res.country.state')

    @api.multi
    @api.onchange('regional_level','parent_id')
    def _onchange_parent_id(self):
        for item in self:
            arrParent = []
            if item.regional_level=='city':
                parent=item.env['res.country.state'].search([('regional_level','=','province')])
                for record in parent:
                    arrParent.append(record.id)
                return {
                    'domain':{'parent_id':[('id','in',arrParent)]}
                }
            elif item.regional_level=='district':
                parent=item.env['res.country.state'].search([('regional_level','=','city')])
                for record in parent:
                    arrParent.append(record.id)
                return {
                    'domain':{'parent_id':[('id','in',arrParent)]}
                }
            elif item.regional_level=='subdistrict':
                parent=item.env['res.country.state'].search([('regional_level','=','district')])
                for record in parent:
                    arrParent.append(record.id)
                return {
                    'domain':{'parent_id':[('id','in',arrParent)]}
                }

    @api.multi
    @api.constrains('city_id')
    def _constraint_city(self):
        for item in self:
            if len(item.city_id) < 3 or len(item.city_id) > 30:
                raise exceptions.ValidationError('City must be 3-5 character')

    @api.multi
    @api.constrains('district_id')
    def _constraint_district(self):
        for item in self:
            if len(item.district_id) < 3 or len(item.district_id) > 30:
                raise exceptions.ValidationError('District must be 3-5 character')

    @api.multi
    @api.constrains('subdistrict_id')
    def _constraint_subdistrict(self):
        for item in self:
            if len(item.subdistrict_id) < 3 or len(item.subdistrict_id) > 30:
                raise exceptions.ValidationError('Sub_District must be 3-5 character')