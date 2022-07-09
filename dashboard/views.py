from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render

# @login_not_required
from donations.models import MonetaryDonation, MemberMonetaryDonation
from expenses.models import Expense
from membership.models import Member
from offerings.models import Offering
from projects.models import Project
from utilities.send_sms import send_sms


def dashboard(request):
    total_offerings = Offering.objects.all().aggregate(Sum('amount'))
    total_monetary_donation = MonetaryDonation.objects.all().aggregate(Sum('amount'))
    total_projects = Project.objects.all().count()
    total_members = Member.objects.all().count()
    total_member_monetary_donation = MemberMonetaryDonation.objects.all().aggregate(Sum('amount'))
    total_expenses = Expense.objects.all().aggregate(Sum('amount'))
    if total_monetary_donation['amount__sum'] is None:
        total_monetary_donation['amount__sum'] = 0
    elif total_member_monetary_donation['amount__sum'] is None:
        total_member_monetary_donation['amount__sum'] = 0
    elif total_offerings['amount__sum'] is None:
        total_offerings['amount__sum'] = 0

    total_contributions = float(total_offerings['amount__sum'] or 0) + float(
        total_monetary_donation['amount__sum'] or 0) + \
                          float(total_member_monetary_donation['amount__sum'] or 0)
    te = round(total_expenses['amount__sum'] or 0, 2)
    tc = round(total_contributions or 0, 2)
    context = {'total_expenses': te, 'total_projects': total_projects,
               'total_members': total_members, 'total_contributions': tc}
    # send_sms(sendto='+233503422990', message_content="You did it!")
    return render(request, 'dashboard/dashboard.html', context)


# def runurl(request, token):
#     return HttpResponse("Kit surfing")