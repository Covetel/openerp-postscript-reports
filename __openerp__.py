{
   'name': 'PostScripts reports',
   'version': '0.01',
   'category': 'Reports',
   'description': "Openerp module that adds a postscript reports certain existing modules",
   'author': 'Covetel R.S',
   'website': 'http://www.covetel.com.ve',
   'depends': ['stock', 'procurement', 'board', 'sale'],
   'data': [],
   'init_xml': [],
   'update_xml': [
       #'reports.xml',
       'invoices_postscript_view.xml',
   ],
   'demo_xml': [],
   'test': [],
   'installable': True,
   'active': False,
}
