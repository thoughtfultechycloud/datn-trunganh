from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render


MOCK_PROJECTS = [
    {'name': 'Alpha — ERP Migration',     'manager': 'James Nguyen',   'budget': '620,000', 'spent': '508,400', 'pct': 82,  'status': 'Active',   'status_class': 'active'},
    {'name': 'Beta — Cloud Infra',        'manager': 'Sara Lee',        'budget': '340,000', 'spent': '363,800', 'pct': 107, 'status': 'Over Budget','status_class': 'over'},
    {'name': 'Gamma — Mobile App v2',     'manager': 'Tom Pham',        'budget': '280,000', 'spent': '182,000', 'pct': 65,  'status': 'Active',   'status_class': 'active'},
    {'name': 'Delta — BI Dashboard',      'manager': 'Lisa Tran',       'budget': '190,000', 'spent': '172,900', 'pct': 91,  'status': 'Review',   'status_class': 'review'},
    {'name': 'Epsilon — Security Audit',  'manager': 'Kevin Do',        'budget': '150,000', 'spent': '171,000', 'pct': 114, 'status': 'Over Budget','status_class': 'over'},
    {'name': 'Zeta — HR System',          'manager': 'Amy Vo',          'budget': '420,000', 'spent': '201,600', 'pct': 48,  'status': 'Active',   'status_class': 'active'},
    {'name': 'Eta — API Gateway',         'manager': 'Dan Hoang',       'budget': '210,000', 'spent': '153,300', 'pct': 73,  'status': 'Active',   'status_class': 'active'},
    {'name': 'Theta — Data Warehouse',    'manager': 'Mia Nguyen',      'budget': '550,000', 'spent': '550,000', 'pct': 100, 'status': 'Complete', 'status_class': 'complete'},
    {'name': 'Iota — DevOps Automation',  'manager': 'Ryan Le',         'budget': '175,000', 'spent': '140,000', 'pct': 80,  'status': 'Active',   'status_class': 'active'},
    {'name': 'Kappa — UX Redesign',       'manager': 'Nina Bui',        'budget': '130,000', 'spent': '136,500', 'pct': 105, 'status': 'Over Budget','status_class': 'over'},
    {'name': 'Lambda — CRM Integration', 'manager': 'Chris Mai',       'budget': '310,000', 'spent': '279,000', 'pct': 90,  'status': 'Review',   'status_class': 'review'},
    {'name': 'Mu — Compliance Platform',  'manager': 'Grace Dang',      'budget': '400,000', 'spent': '280,000', 'pct': 70,  'status': 'Active',   'status_class': 'active'},
    {'name': 'Nu — AI Analytics',         'manager': 'Victor Trinh',    'budget': '480,000', 'spent': '192,000', 'pct': 40,  'status': 'Active',   'status_class': 'active'},
    {'name': 'Xi — Legacy Migration',     'manager': 'Helen Phan',      'budget': '360,000', 'spent': '360,000', 'pct': 100, 'status': 'Complete', 'status_class': 'complete'},
]


@staff_member_required
def dashboard(request):
    context = {'projects': MOCK_PROJECTS}
    return render(request, 'dashboard/index.html', context)
