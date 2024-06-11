{
    'name': "Library Management",
    'depends': ['base'],
    'application': True,
    'version': '1.0.0',
    'data': [
        'security/ir.model.access.csv',
        'views/library_book_view.xml',
        'views/library_book_category_view.xml',
        'views/library_book_author_view.xml',
        'views/library_menu_view.xml',
    ],
    'demo': [
        'demo/library_book_author_demo.xml',
        'demo/library_book_category_demo.xml',
        'demo/library_book_demo.xml'
    ],
    'license': 'LGPL-3',
}
