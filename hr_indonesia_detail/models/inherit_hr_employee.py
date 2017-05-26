from openerp import models, fields, api, exceptions
import re

from psycopg2 import OperationalError

from openerp import SUPERUSER_ID
from datetime import datetime, date, time

class InheritHrEmployee(models.Model):

    def return_action_family(self, cr, uid, ids, context=None):
        """ This opens the xml view specified in xml_id for the current Family form """
        if context is None:
            context = {}
        if context.get('xml_id'):
            res = self.pool.get('ir.actions.act_window').for_xml_id(cr, uid, 'hr_indonesia_detail', context['xml_id'],
                                                                    context=context)
            res['context'] = context
            res['context'].update({'default_parent_id': ids[0]})
            res['domain'] = [('parent_id', '=', ids[0])]
            return res
        return False

    def return_action_education(self, cr, uid, ids, context=None):
        """ This opens the xml view specified in xml_id for the current Education form """
        if context is None:
            context = {}
        if context.get('xml_id'):
            res = self.pool.get('ir.actions.act_window').for_xml_id(cr, uid, 'hr_indonesia_detail', context['xml_id'],
                                                                    context=context)
            res['context'] = context
            res['context'].update({'default_parent_id': ids[0]})
            res['domain'] = [('parent_id', '=', ids[0])]
            return res
        return False

    def return_action_address(self, cr, uid, ids, context=None):
        """ This opens the xml view specified in xml_id for the current Address form """
        if context is None:
            context = {}
        if context.get('xml_id'):
            res = self.pool.get('ir.actions.act_window').for_xml_id(cr, uid, 'hr_indonesia_detail', context['xml_id'],
                                                                    context=context)
            res['context'] = context
            res['context'].update({'default_employee_id': ids[0]})
            res['domain'] = [('employee_id', '=', ids[0])]
            return res
        return False




    _inherit = 'hr.employee'


    address_home_ids    = fields.One2many('employee.address.inherits','employee_id', string='Address Home')
    detail_family_ids   = fields.One2many('hr.family','parent_id',string='Family')
    detail_education_ids= fields.One2many('hr.education.detail','parent_id',string='Education')
    contract_type       = fields.Selection(selection_add=[('3','PKWTT Probation')])
    date_probation      = fields.Char('Date of Probation', compute='_compute_probation')
    month_probation     = fields.Integer('Month Probation')
    children            = fields.Integer('Children', compute='compute_children')
    image_family_card   = fields.Binary('Upload Family Card')
    family_card_name    = fields.Char()
    family_card         = fields.Char('Family Card')
    image_npwp          = fields.Binary('Upload NPWP')
    npwp_name           = fields.Char()
    gender              = fields.Selection([('male','Male'),('female','Female')])
    marital             = fields.Selection([('single','Single'),('married','Married'),('divorced', 'Divorced')])
    emergency_person    = fields.Char('Emergency Contact Person')
    emergency_phone     = fields.Char('Emergency Contact Phone')
    identif_num         = fields.Char('Identification Number', related='identification_id')
    status_employee     = fields.Selection([('internship','Internship'),('outsource','Outsource')])
    age_employee        = fields.Char('Age', compute='_compute_age', readonly="True")
    resigndate          = fields.Date('Date of Resign')
    hiredate            = fields.Date('Date of Hired')
    grade_id            = fields.Many2one('hr.indonesia.grade', 'Grade')
    city_id             = fields.Many2one('res.country.state', string='City')
    working_address_id  = fields.Many2one('employee.address.inherits','Working Address')

    religion            = fields.Char('Religion', compute='_compute_religion')

    @api.multi
    @api.depends('religion_id', 'religion')
    def _compute_religion(self):
        for item in self:
            if item.religion_id:
                temp= item.religion_id
                item.religion=temp

    @api.multi
    @api.onchange('working_address_id')
    def _onchange_working_address_id(self):
        for item in self:
            item.env.cr.execute("select id from employee_address_inherits where type='working' and employee_id = %d"
                %(item.id))
            result_count = item.env.cr.fetchone()[0]
            # request = item.env['employee.address.inherits'].search([('type','=','working'),('employee_id','=',item.id)])
            arrAddress = []
            print result_count
            for address in result_count:
                arrAddress.append(address.id)

            print arrAddress
            print 'wkkwkwk'
            return {
                    'domain' : {
                        'working_address_id' : [('id','in',arrAddress)]}
                }


    @api.multi
    @api.constrains('joindate', 'hiredate')
    def _check_joindate(self):
        for item in self:
            if item.joindate == False:
                return True
            elif item.hiredate == False:
                raise exceptions.ValidationError("Input Date of Hired first")
            elif item.joindate < item.hiredate:
                raise exceptions.ValidationError("Date of join is Invalid")

    @api.multi
    @api.constrains('joindate','resigndate')
    def _check_resigndate(self):
        for item in self:
            if item.resigndate==False:
                return True
            elif item.joindate==False:
                raise exceptions.ValidationError("Input Date of Join first")
            elif item.resigndate < item.joindate :
                raise exceptions.ValidationError("Date of Resign is Invalid")

    @api.multi
    @api.depends('month_probation', 'joindate')
    def _compute_probation(self):
        for item in self:
            if item.joindate == False:
                return True
            else:
                fmt = '%Y-%m-%d'

                conv_joindate = datetime.strptime(str(item.joindate), fmt)
                init_joindate = conv_joindate.date()

                result = init_joindate.month + item.month_probation

                item.date_probation = result

    @api.multi
    @api.depends('birthday')
    def _compute_age(self):
        for item in self:
            if item.birthday==False:
                return True
            else:
                fmt = '%Y-%m-%d'
                datenow = datetime.today()
                birthday = item.birthday

                conv_bitrhday = datetime.strptime(str(birthday), fmt)
                init_birthday = conv_bitrhday.date()

                result_year = datenow.year - init_birthday.year - (
                (datenow.month, init_birthday.day) < (init_birthday.month, init_birthday.day))
                if result_year < 18 :
                    item.age_employee = str(result_year) + ' Under Age'
                else:
                    item.age_employee = str(result_year)

    @api.multi
    @api.depends('children','detail_family_ids')
    def compute_children(self):
        for item in self:
            if item.detail_family_ids:
                arrChild = []
                child=item.env['hr.family'].search([('status','=','Child'),('parent_id','=',item.id),('active_status','=',True)])
                for record in child:
                    arrChild.append(record.id)
                count_child=len(arrChild)
                item.children=count_child

    @api.multi
    @api.constrains('place_of_birth')
    def _check_description(self):
        for item in self:
            if item.place_of_birth==False:
                return True
            elif bool(re.search(r'\d', item.place_of_birth)):
                raise exceptions.ValidationError("Fields place of birth contain aphabet only")

    @api.multi
    @api.constrains('emergency_person')
    def _check_person(self):
        for item in self:
            if item.emergency_person==False:
                return True
            elif bool(re.search(r'\d', item.emergency_person)):
                raise exceptions.ValidationError("Fields Emergency Contact Person contain alphabet only")
            elif len(item.emergency_person) < 3 or len(item.emergency_person) > 30:
                raise exceptions.ValidationError('Emergency Contact Person must 3-30 character')

    @api.multi
    @api.constrains('emergency_phone')
    def _constraint_emergency_phone(self):
        for item in self:
            val = item.emergency_phone
            if val==False:
                return True
            elif not val.isdigit():
                raise exceptions.ValidationError('Emergency Contact Phone must be numeric')
            elif len(val) < 10 or len(val) > 14:
                raise exceptions.ValidationError('Emergency Contact Phone is not valid')

    @api.multi
    @api.constrains('mobile_phone')
    def check_numval_mobile_phone(self):
        for item in self:
            val = item.mobile_phone
            if val==False:
                return True
            elif not val.isdigit():
                raise exceptions.ValidationError('Work Mobile must be numeric')

    # @api.multi
    # @api.constrains('work_phone')
    # def check_numval_work_phone(self):
    #     for item in self:
    #         val = item.work_phone
    #         if val==False:
    #             return True
    #         elif not val.isdigit():
    #             raise exceptions.ValidationError('Work Phone must be numeric')

    @api.multi
    @api.constrains('identification_id')
    def check_numval_identification_id(self):
        for item in self:
            val = item.identification_id
            if val==False:
                return True
            elif not val.isdigit():
                raise exceptions.ValidationError('Identification No. must be numeric')


    @api.multi
    @api.constrains('passport_id')
    def check_numval_passport_id(self):
        for item in self:
            val = item.passport_id
            if val==False:
                return True
            elif not val.isdigit():
                raise exceptions.ValidationError('Passport Number must be numeric')

    @api.multi
    @api.constrains('nik_number')
    def check_numval_nik_number(self):
        for item in self:
            val = item.nik_number
            if val==False:
                return True
            elif not val.isdigit():
                raise exceptions.ValidationError('Employee Identity Number must be numeric')


    @api.multi
    @api.constrains('bpjs_number')
    def check_numval_bpjs_number(self):
        for item in self:
            val = item.bpjs_number
            if val==False:
                return True
            elif not val.isdigit():
                raise exceptions.ValidationError('BPJS TK must be numeric')

    @api.multi
    @api.constrains('health_insurance_number')
    def check_numval_health_insurance_number(self):
        for item in self:
            val = item.health_insurance_number
            if val==False:
                return True
            elif not val.isdigit():
                raise exceptions.ValidationError('BPJS K must be numeric')

    @api.multi
    @api.constrains('npwp_number')
    def check_numval_npwp_number(self):
        for item in self:
            val = item.npwp_number
            if val==False:
                return True
            elif not val.isdigit():
                raise exceptions.ValidationError('NPWP must be numeric')

    @api.one
    @api.constrains('family_card_name')
    def _check_filename(self):
        if self.family_card_name:
            if not self.family_card_name:
                raise exceptions.ValidationError("There is no file")
            else:
                # Check the file's extension
                tmp = self.family_card_name.split('.')
                ext = tmp[len(tmp) - 1]
                if ext != 'jpg' and ext !='img' and ext !='jpeg' and ext !='png' and ext !='pdf' :
                    raise exceptions.ValidationError("The family card file must be a img, png, jpg, jpeg, or pdf format file")

    @api.one
    @api.constrains('npwp_name')
    def _check_npwpname(self):
        if self.npwp_name:
            if not self.npwp_name:
                raise exceptions.ValidationError("There is no file")
            else:
                # Check the file's extension
                tmp = self.npwp_name.split('.')
                ext = tmp[len(tmp) - 1]
                if ext != 'jpg' and ext != 'img' and ext != 'jpeg' and ext != 'png' and ext != 'pdf':
                    raise exceptions.ValidationError(
                        "The NPWP file must be a img, png, jpg, jpeg, or pdf file")


    class hr_indonesia_grade(models.Model):
        _name = 'hr.indonesia.grade'

        name    = fields.Char('Grade')