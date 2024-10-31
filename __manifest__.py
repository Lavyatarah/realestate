# -*- coding: utf-8 -*-
{
    'name': "realestate",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
        """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base'],

   'data': [
        'security/ir.model.access.csv',
        'views/estate_property_type_views.xml',
        'views/res_users_views.xml',
        'views/estate_property_views.xml',
        'views/views.xml',
        'views/templates.xml',
        'views/estate_menus.xml',
    ],

    'installable': True,
    'application': True,

    'demo': [
        'demo/demo.xml',
    ],
}
