from django.shortcuts import render, redirect
from django.apps import apps
from django.http import HttpResponseRedirect, HttpResponse

from index.models import *



import mimetypes, os
from django.conf import settings
import pdfkit
from wsgiref.util import FileWrapper
from .forms import *


def index(request):
    if 'id_client' not in request.session:
        return HttpResponseRedirect('/')

    Request = apps.get_model('index', 'Request')

    if "_logout" in request.POST:
        del request.session['id_client']
        return HttpResponseRedirect('/')

    if request.POST:
        if '_reject' in request.POST:
            obj = Request.objects.get(id=request.POST.get('_reject'))
            obj.status = 'r'
            obj.save()
        if '_accept' in request.POST:
            obj = Request.objects.get(id=request.POST.get('_accept'))
            obj.status = 'a'
            obj.save()

    form = DateRange
    if request.method == "POST":
        form = DateRange(request.POST, request.FILES)
        if form.is_valid():
            end = form.cleaned_data['endDate']
            start = form.cleaned_data['startDate']
            # return report(request, start, end)
            return report_download(request, start, end)

    all_new = Request.objects.filter(status__exact='u')
    all_accepted = Request.objects.filter(status__exact='a')
    all_rejected = Request.objects.filter(status__exact='r')
    all_orders = Request.objects.all()

    content = {
        "all_new": all_new,
        "all_accepted": all_accepted,
        "all_rejected": all_rejected,
        "all": all_orders,
        'form': form,
    }

    return render(request, 'manager/manager.html', content)




def report_download(request, start, end):
    pdf_path = os.path.join(settings.BASE_DIR, 'manager\\templates\\report\\report.pdf')
    file_report = pdfkit.from_url(f'http://localhost:8000/manager/report/{start}/{end}', pdf_path)
    print(f'FILE_REPORT_URL {file_report}')

    filename = 'report.pdf'
    path = os.path.expanduser(pdf_path)
    wrapper = FileWrapper(open(pdf_path, 'rb'))
    response = HttpResponse(wrapper, content_type=mimetypes.guess_type(filename)[0])
    response['Content-Disposition'] = f"attachment; filename={filename}"

    return response


def report(request, start, end):
    all = Request.objects.all().filter(data__range=[start, end])
    all_len = len(all)
    accept = all.filter(status__exact='a')
    accept_len = len(accept)
    reject = all.filter(status__exact='r')
    reject_len = len(reject)
    all_price = 0
    for i in accept:
        all_price += i.total


    content = {
        'start': start,
        'end': end,
        'all': all,
        'all_len': all_len,
        'accept': accept,
        'accept_len': accept_len,
        'reject': reject,
        'reject_len': reject_len,
        'all_price': all_price,
    }
    return render(request, 'report/report.html', content)
