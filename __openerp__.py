{
   'name': 'PostScripts reports',
   'version': '0.02',
   'category': 'Reports',
   'description': "Openerp module that adds a postscript reports certain existing modules",
   'author': 'Covetel R.S',
   'website': 'http://www.covetel.com.ve',
   'depends': ['report_latex', 'stock', 'procurement', 'board', 'sale'],
   'js': ['static/src/js/print_invoices.js'],
   'data': [
       'invoices_postscript_view.xml',
	],
   'init_xml': [],
   'demo_xml': [],
   'test': [],
   'installable': True,
   'active': False,
}
