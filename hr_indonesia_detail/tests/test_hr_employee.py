from openerp.tests import TransactionCase
from openerp.exceptions import ValidationError

from openerp import api

class TestHrEmployee(TransactionCase):

    def setUp(self):
        super(TestHrEmployee, self).setUp()
        self.employee=self.env["hr.employee"]
        self.person_cindy = {'name': 'Cindy', 'nik_number': '', 'identification_id': ''}

    @api.model
    def test_check_employee(self):
        """ tidak boleh ada employye yang memiliki no id sama"""
        person = self.employee.create(self.person_cindy)
        self.assertTrue(person)

