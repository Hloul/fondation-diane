{
    'name': "Project Workflow",
    'version': '1.2',
    'depends': ['base','project'],
    'author': "Hloul-BAS",
    'category': 'Management',
    'description': """
    New
    """,
    'license': 'AGPL-3',
    'data':[
        'views/category.xml',
        'views/phase.xml',
        'views/project_views.xml',
        'views/status.xml',
        'security/ir.model.access.csv', 
        'demo/data.xml'
        
    ],
    # data files always loaded at installation
    'installable':True,
}