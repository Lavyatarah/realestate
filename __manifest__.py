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
        'views/estate_property_views.xml',  # Comma added
        'views/views.xml',                   # Comma added
        'views/templates.xml',               # Comma added
        'views/estate_menus.xml',            # Comma added
    ],
    'demo': [
        'demo/demo.xml',
    ],
}
