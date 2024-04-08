# -*- coding: utf-8 -*-
{
    'name': "School Management",
    'version': '17.0.1.0.0',
    'depends': ['base', 'mail', 'sale_management', 'base_automation','website'],
    'author': "Shaheem P S ",
    'category': 'category',
    'description': """
   about the school system
    """,
    'summary': 'Manage the school system',
    # data files always loaded at installation
    'data': [
        'security/res_groups.xml',
        'security/ir_rule.xml',
        'security/ir.model.access.csv',

        'report/leave_information_template.xml',
        'report/event_detail_template.xml',
        'report/school_club_template.xml',
        'report/student_information_template.xml',
        'report/exam_details_template.xml',
        'report/ir_actions_report.xml',

        'data/ir_sequence_data.xml',
        'data/mail_template_data.xml',
        'data/ir_cron_data.xml',
        'data/base_automation_data.xml',
        'data/academic_year_data.xml',
        # 'data/school_class_data.xml',
        'data/school_department_data.xml',
        'data/school_subject_data.xml',
        'data/website_menu_data.xml',

        'wizard/leave_report_views.xml',
        'wizard/event_details_views.xml',
        'wizard/club_data_views.xml',
        'wizard/student_information_view.xml',
        'wizard/exam_details_views.xml',

        'views/school_menu.xml',
        'views/registration_view.xml',
        'views/academic_year_view.xml',
        'views/class_view.xml',
        'views/department_view.xml',
        'views/subject_view.xml',
        'views/event_view.xml',
        'views/school_club_view.xml',
        'views/sale_order_view.xml',
        'views/respartner_view.xml',
        'views/leave_view.xml',
        'views/school_exam_view.xml',

        'views/website_event_template.xml',
        'views/website_student_template.xml',
        'views/website_leave_template.xml',
        'views/website_student_tree_view.xml',
        'views/website_event_tree_view.xml',
        'views/website_leave_tree_view.xml',
        'views/website_thank_you.xml',

        'views/snippets/website_events_form_snip.xml',
        'views/snippets/event_snippets.xml',

    ],
    'assets': {
        'web.assets_backend': [
            'school_management/static/src/js/action_manager.js'
        ],
        'web.assets_frontend': [
            'school_management/static/src/js/student_registartion.js',
            'school_management/static/src/js/school_leave.js',
            'school_management/static/src/js/event_snippet.js',
            'school_management/static/src/xml/event_snippet_template.xml'
        ],

    },
    'application': True,
    'installable': True,
    'external_dependencies': {'python': ["numpy"]}

}
