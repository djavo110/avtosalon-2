from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.http import JsonResponse
from .models import *
from .forms import *
from django.template.loader import render_to_string
import qrcode
import base64
from io import BytesIO
from weasyprint import HTML
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def index(request):
    word = request.GET.get('word', '').strip()
    if word:
        car = Car.objects.filter(model__istartswith=word)
    else:
        car = Car.objects.all()
    avtosalon = Avtosalon.objects.all()
    brend = Brend.objects.all()
    context = {
        "avtosalon": avtosalon,
        "brend": brend,
        "car": car,
        "title": "NEW TITLE"
    }
    return render(request, 'index.html', context)

def search_suggestions(request):
    q = request.GET.get('q', '').strip()
    if q:
        results = Car.objects.filter(title__istartswith=q).values_list('title', flat=True)[:5]
        return JsonResponse(list(results), safe=False)
    return JsonResponse([], safe=False)

def category(request, pk):
    cars = Car.objects.filter(brend__id = pk)
    brend = Brend.objects.all() 
    context = {
        "cars": cars,
        "brend": brend
    }
    return render(request,  'category.html', context=context)

def add_car(request):
    if request.method == 'POST':
        form = CarForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('index')
    else:
        form = CarForm()
    return render(request, 'add_car.html', context={"form": form})

def detail_car(request, pk):
    car = get_object_or_404(Car, pk=pk)
    car_url = request.build_absolute_uri(car.get_absolute_url())
    qr = qrcode.make(car_url)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    qr_code_base64 = base64.b64encode(buffer.getvalue()).decode()
    context = {
        "car": car,
        "qr_code": qr_code_base64
    }
    return render(request, 'detail_car.html', context=context)

def salon_car(request, brend_pk, salon_pk):
    cars = Car.objects.filter(brend= brend_pk, salon=salon_pk)
    brend = Brend.objects.all()
    context = {
        "salon_pk":salon_pk,
        "cars": cars,
        "brend": brend,
    }
    return render(request, 'salon_car.html', context)

# def car_pdf(request, pk):
#     car = get_object_or_404(Car, pk=pk)
#     html_string = render_to_string("car_pdf.html", {"car": car})
#     pdf_file = HTML(string=html_string).write_pdf()

#     response = HttpResponse(pdf_file, content_type="application/pdf")
#     response["Content-Disposition"] = f'attachment; filename="car_{car.pk}.pdf"'
#     return response

def car_pdf(request, pk):
    car = get_object_or_404(Car, pk=pk)

    base_url = request.build_absolute_uri('/').rstrip('/')
   
    qr_img = qrcode.make(f"{car.brend} {car.model} {car.price}$ {car.color} {car.context}")
    buffer = BytesIO()
    qr_img.save(buffer, format="PNG")
    qr_code_b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
    qr_base64 = base64.b64encode(buffer.getvalue()).decode()

    if car.image:  # Agar mashina rasmi mavjud bo'lsa
        car_image_url = f"{base_url}{car.image.url}"
    else:
        car_image_url = f"{base_url}/static/default_car.jpg"

    html_string = render_to_string("car_pdf.html", {
        "car": car,
        "qr_code": qr_base64,
        "car_image_url": car_image_url,  # Rasm URL
        "car_link": f"{base_url}/car/{car.pk}/"  # Mashina sahifasiga link
    })

    pdf_file = HTML(string=html_string, base_url=base_url).write_pdf()
    response = HttpResponse(pdf_file, content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="car_{car.pk}.pdf"'
    return response

def login_views(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')


        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
            messages.success(request, 'ok!')

        else:
            messages.error(request, 'Login yoki parol xato!')     
            
    form = UserLoginForm()

    return render(request, 'login.html', {'form': form})

@login_required(login_url='login')
def index(request):
    word = request.GET.get('word', '').strip()
    if word:
        car = Car.objects.filter(model__istartswith=word)
    else:
        car = Car.objects.all()
    avtosalon = Avtosalon.objects.all()
    brend = Brend.objects.all()
    context = {
        "avtosalon": avtosalon,
        "brend": brend,
        "car": car,
        "title": "NEW TITLE"
    }
    return render(request, 'index.html', context)

def logout_view(request):
    logout(request)
    return redirect('login')
