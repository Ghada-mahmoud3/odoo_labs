{
    'name': 'Hospitals Management System',
    'version': '2.0.0',
    'summary': 'Manage hospital patients, departments and doctors',
    'description': """
        Module for managing hospital information
        - Patients
        - Departments
        - Doctors
    """,
    'author': 'ghada',
    'depends': ['base','crm'],
    #,'crm'
    'data': [
        'views/menu_views.xml',
        'views/patient_views.xml',
        'views/patient_log_views.xml',
        'views/department_views.xml',
        'views/doctor_views.xml',
        'views/res_partner_views.xml',        
    ],
    #'views/crm_customer_views.xml',

    'installable': True,
    'application':True,
    'license': 'LGPL-3'
}