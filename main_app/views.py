from django.shortcuts import render
# from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Bike

# Add the Bike class & list and view function below the imports
# class Bike:  # Note that parens are optional if not inheriting from another class
#   def __init__(self, brand, model, year, condition):
#     self.brand = brand
#     self.model = model
#     self.year = year
#     self.condition = condition

# bikes = [
#   Bike('Peugeot', 'PGN 10', 1979, 'Used'),
#   Bike('Vitus', '787 Futural', 1987, 'NOS'),
#   Bike('Bianchi', 'Pista', 1990, 'New')
# ]

# Create your views here.
def home(request):
    # return HttpResponse('<h1>Hello /ᐠ｡‸｡ᐟ\ﾉ</h1>')
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')

def bikes_index(request):
    bikes = Bike.objects.all()
    return render(request, 'bikes/index.html', { 'bikes': bikes})

def bikes_detail(request, bike_id):
  bike = Bike.objects.get(id=bike_id)
  return render(request, 'bikes/detail.html', { 'bike': bike })

class BikeCreate(CreateView):
    model = Bike
    fields = '__all__'

class BikeUpdate(UpdateView):
    model = Bike
    fields = '__all__'

class BikeDelete(DeleteView):
    model = Bike
    success_url = '/bikes/'