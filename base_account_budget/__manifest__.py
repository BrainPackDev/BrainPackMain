{
    'name': 'BrainPack Budget Management',
    'version': '16.0.1.0.0',
    'summary': """ Budget Management for Odoo 16 Community Edition. """,
    'description': """ This module allows accountants to manage analytic and budgets.

     Once the Budgets are defined (in Accounting/Accounting/Budgets), the Project Managers
     can set the planned amount on each Analytic Account.
     
     The accountant has the possibility to see the total of amount planned for each
     Budget in order to ensure the total planned is not greater/lower than what he
     planned for this Budget. Each list of record can also be switched to a graphical
     view of it.
     
     Three reports are available:

     1. The first is available from a list of Budgets. It gives the spreading, for
     these Budgets, of the Analytic Accounts.
     2. The second is a summary of the previous one, it only gives the spreading,
     for the selected Budgets, of the Analytic Accounts.
     3. The last one is available from the Analytic Chart of Accounts. It gives
     the spreading, for the selected Analytic Accounts of Budgets. 
     Odoo 15 Budget Management,Odoo 15, Odoo 15 Budget, Odoo 15 Accounting, 
     Odoo 15 Account,Budget Management, Budget""",
    'category': 'Accounting',
    'author': 'BrainPack',
    'company': 'BrainPack',
    'maintainer': 'BrainPack',
    'depends': ['base', 'account'],
    'website': 'https://www.brainpack.io',
    'data': [
        'security/ir.model.access.csv',
        'security/account_budget_security.xml',
        'views/account_analytic_account_views.xml',
        'views/account_budget_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
