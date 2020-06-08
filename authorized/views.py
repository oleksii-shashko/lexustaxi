from django.shortcuts import render
from django.apps import apps
from django.http import HttpResponseRedirect
from .forms import Order
import datetime


def index(request):
    if 'id_client' not in request.session:
        return HttpResponseRedirect('/')

    Cars = apps.get_model('index', 'Car')
    Distance = apps.get_model("index", "Distance")
    Request = apps.get_model("index", "Request")
    Client = apps.get_model("index", "Client")

    cars = Cars.objects.all()

    if "_logout" in request.POST:
        del request.session['name']
        del request.session['phone_number']
        del request.session['id_client']
        return HttpResponseRedirect('/')

    locker = 0
    initial_data = {}
    if "_car_order" in request.POST:
        initial_data = {
            "car": request.POST.get('_car_order')
        }
        locker = 3

    form = Order(initial=initial_data)
    if request.method == "POST" and "_car_order" not in request.POST:
        form = Order(request.POST)
        if form.is_valid():
            car = Cars.objects.get(id=request.POST.get("car"))
            client = Client.objects.get(id=request.session["id_client"])
            distance = (Distance.objects.filter(
                            from_address=request.POST.get("_from"))
                        ).get(
                            to_address=request.POST.get("_to")
                            )
            comment = request.POST.get("comment")
            today = datetime.datetime.today().date()

            order_obj = Request(client=client, car=car, distance=distance, comment=comment, data=today)
            order_obj.save()

            form = Order()

    client = Client.objects.get(id=request.session["id_client"])
    all_orders = Request.objects.filter(client__exact=client)

    context = {
        "all_orders": all_orders,
        "client": client,
        "cars_list": cars,
        "form": form,
        "reload": locker
    }
    return render(request, 'authorized/authorized.html', context)

