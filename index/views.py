from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Car, Client
from .forms import AuthForm, RegForm


def index(request):

    if "name" in request.session:
        return HttpResponseRedirect('/authorized/')
    if "roll" in request.session:
        return HttpResponseRedirect('/manager/')

    cars = Car.objects.all()

    form_auth = AuthForm()
    if request.method == "POST":
        form_auth = AuthForm(request.POST)

    form_reg = RegForm()
    if request.method == "POST":
        form_reg = RegForm(request.POST)

    if not request.POST.getlist("login", -1) == -1 and request.POST.getlist("phone_number", -1) == -1:
        if form_auth.is_valid():
            roll = Client.objects.get(login=request.POST.get("login")).roll
        else:
            roll = ''

        if roll == 'c':
            client = Client.objects.get(login=request.POST.get("login"))
            request.session['name'] = client.name
            request.session['phone_number'] = client.phone_number
            request.session['id_client'] = client.id
            return HttpResponseRedirect('/authorized/')
        elif roll == 'a':
            request.session['roll'] = roll
            return HttpResponseRedirect('/manager/')
        locker = 2
    elif not request.POST.getlist("phone_number", -1) == -1 and not request.POST.getlist("login", -1) == -1:
        if form_reg.is_valid():
            form_reg.save()

            client = Client.objects.get(login=request.POST.get("login"))
            request.session['name'] = client.name
            request.session['phone_number'] = client.phone_number
            request.session['id_client'] = client.id

            return HttpResponseRedirect('/authorized/')
        locker = 1
    else:
        locker = 0

    if "_invalid_order" in request.GET:
        locker = 1

    context = {
        "form_reg": form_reg,
        "form_auth": form_auth,
        "cars_list": cars,
        "reload": locker
    }

    return render(request, 'index/index.html', context=context)


