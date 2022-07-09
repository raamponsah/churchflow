from django.http import HttpResponse
from django.shortcuts import render

import xlwt

from Resources.resources import OfferingResource, PledgeResource

wb = xlwt.Workbook()
ws = wb.add_sheet('A Test Sheet')
wb = xlwt.Workbook(encoding='utf-8')


def setup_cashbook(request):
    return render(request, 'cashbook/setup.html')


def generate_total_contributions(request):
    offering_resource = OfferingResource()
    pledge_resource = PledgeResource()
    dataset = pledge_resource.export()
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="exported_data.xls"'
    return response