# -*- coding: utf-8 -*-
{
    'name': "HR Indonesia Detail",

    'summary': """
        Deatil Family, Deatil Address, Detail Education""",

    'description': """
        Long description of module's purpose
    """,

    'author': " Mahroza Pradana , M.Nurmayyahdi A., M.Rafi , Wilson Lumadi",
    'website': "http://www.palmagroup.co.id",

    'category': 'Human Resources',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','hr_indonesia'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/view_inherit_res_country_state.xml',
        'views/view_inherit_hr_employee.xml',
        'views/view_hr_family.xml',
        'views/view_family_job.xml',
        'views/view_education_detail.xml',
        'views/view_configuration_hr_detail.xml',
        'views/view_employee_address.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
