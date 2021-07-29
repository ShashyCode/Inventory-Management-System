from django.http.response import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from home.models import *
from django.contrib import messages
from django.db.models.functions import Now

# Create your views here.
def index(request):
    items = Product.objects.all()
    context = {
        'items' : items
    }
    return render(request, 'home.html', context)

def location(request):
    items = Locations.objects.values('locationid').distinct()
    context = {
        'items' : items
    }
    return render(request, 'location.html', context)

def moving(request):
    if request.method == "POST":
        productid = request.POST.get('ProductID')
        movementid = request.POST.get('MovementID')
        q = request.POST.get('Quantity')
        from_location = request.POST.get('From_Location')
        to_location = request.POST.get('To_Location')
        
        if not from_location and not to_location:
            messages.warning(request, 'Please Check Values')
            return render(request, 'moving.html')
        elif ProductMovement.objects.filter(movementId=movementid).exists():
            messages.warning(request, 'The Movement ID already exists!')
            return render(request, 'moving.html')
        elif not from_location:
            if not Locations.objects.filter(locationid= to_location).exists():
                messages.warning(request, 'The Destination does not exist!')
                return render(request, 'moving.html')
            elif not Product.objects.filter(ProductId=productid).exists():
                messages.warning(request, 'The Product does not exist!')
                return render(request, 'moving.html')
            else:
                temp = Product.objects.get(ProductId=productid, locationid=to_location)
                temp.qt += int(q)
                Move = ProductMovement(locationid=to_location, ProductId=productid, qt=0, movementId=movementid, timestamp=Now(), to_location=to_location, qty=temp.qt)
                Move.save()
                temp.delete()
                messages.success(request, 'The Product has been added!')
                return render(request, 'moving.html')
        elif not to_location:
            if not Locations.objects.filter(locationid= from_location).exists():
                messages.warning(request, 'The Origin does not exist!')
                return render(request, 'moving.html')
            elif not Product.objects.filter(ProductId=productid, locationid=from_location).exists():
                messages.warning(request, 'The Product does not exist!')
                return render(request, 'moving.html')
            else:
                temp = Product.objects.get(ProductId=productid, locationid=from_location)
                temp.qt -= int(q)
                Move = ProductMovement(locationid=from_location, ProductId=productid, qt=temp.qt, movementId=movementid, timestamp=Now(), from_location=from_location, qty=q)
                if temp.qt>0:
                    Move.save()
                temp.delete()
                messages.success(request, 'The Product has been removed!')
                return render(request, 'moving.html')
        else:
            if not Locations.objects.filter(locationid= from_location).exists() or not Locations.objects.filter(locationid= to_location).exists():
                messages.warning(request, 'The Locations does not exist!')
                return render(request, 'moving.html')
            elif not Product.objects.filter(ProductId=productid, locationid=from_location).exists():
                messages.warning(request, 'The Product does not exist!')
                return render(request, 'moving.html')
            elif not Product.objects.filter(ProductId=productid, locationid=to_location).exists():
                Move = ProductMovement(locationid=to_location, ProductId=productid, qt=q, movementId=movementid, timestamp=Now(), from_location=from_location, to_location=to_location, qty=q)
                Move.save()
                temp = Product.objects.get(ProductId=productid, locationid=from_location)
                temp.qt -= int(q)
                if temp.qt<=0:
                    temp.delete()
                else:
                    temp.save()
                messages.success(request, 'The Product has been transeferred!')
                return render(request, 'moving.html')
            else:
                
                temp = Product.objects.get(ProductId=productid, locationid=from_location)
                temp2 = Product.objects.get(ProductId=productid, locationid=to_location)
                temp.qt -= int(q)
                Move = ProductMovement(locationid=from_location, ProductId=productid, qt=temp.qt, movementId=movementid, timestamp=Now(), from_location=from_location, to_location=to_location, qty=q)
                if temp.qt>0:
                    Move.save()
                temp.delete()
                temp2.qt += int(q)
                temp2.save()
                messages.success(request, 'The Product has been transferred!')
                return render(request, 'moving.html')

    return render(request, 'moving.html')





def add_location(request):
    if request.method == "POST":
        locationid = request.POST.get('LocationID')
        if not Locations.objects.filter(locationid= locationid).exists():
            Location = Locations(locationid= locationid)
            Location.save()
            messages.success(request, 'The Location has been added!')
            return render(request, 'add_location.html')
        else:
            messages.warning(request, 'The Location already exists!')
            return render(request, 'add_location.html')
    return render(request, 'add_location.html')


def add_product(request):
    if request.method == "POST":
        productid = request.POST.get('ProductID')
        locationid = request.POST.get('LocationID')
        q = request.POST.get('Quantity')
        if not Locations.objects.filter(locationid= locationid).exists():
            messages.warning(request, 'The Location does not exist!')
            return render(request, 'add_product.html')
        elif not Product.objects.filter(ProductId=productid, locationid=locationid).exists():
            Products = Product(ProductId=productid, locationid=locationid, qt=q)
            Products.save()
            messages.success(request, 'The Product has been added!')
            return render(request, 'add_product.html')
        else:
            temp = Product.objects.get(ProductId=productid, locationid=locationid)
            temp.qt += int(q)
            temp.save()
            messages.success(request, 'The Product has been added!')
            return render(request, 'add_product.html')
    return render(request, 'add_product.html')


def movement(request):
    items = ProductMovement.objects.all()
    context = {
        'items' : items
    }
    return render(request, 'movement.html', context)


def editlocation(request, pk):
    item = get_object_or_404(Locations, pk =pk)
    context = {
        'item': item
    }
    if request == 'POST':
        item = get_object_or_404(Locations, pk =pk)
        locationId = request.POST.get('LocationID')
        item.locationid = locationId
        item.save()
        messages.success(request, 'The Location has been edited!')
        return redirect('/locations')
    return render(request, 'editlocation.html', context)
    

def editproduct(request, pk):
    item = get_object_or_404(Product, pk =pk)
    context = {
        'item': item
    }
    if request.method == "POST":
        productid = request.POST.get('ProductID')
        locationid = request.POST.get('LocationID')
        q = request.POST.get('Quantity')
        if not Locations.objects.filter(locationid= locationid).exists():
            messages.warning(request, 'The Location does not exist!')
            return render(request, 'editproduct.html', context)
        else:
            item = get_object_or_404(Product, pk =pk)
            item.ProductId = productid
            item.locationid = locationid
            item.qt = q
            item.save()
            loc = Locations.objects.filter(locationid=locationid)
            loc.delete()
            messages.success(request, 'The Location has been edited!')
            return redirect('/home')
    return render(request, 'editproduct.html', context)


def deleteproduct(request, pk):
    item = get_object_or_404(Product, pk= pk)
    item.delete()
    
    return redirect('/home')


def deletelocation(request, pk):
    item = get_object_or_404(Locations, pk= pk)
    item.delete()
    
    return redirect('/locations')


def deletemovement(request, pk):
    item = get_object_or_404(ProductMovement, pk= pk)
    item.delete()
    
    return redirect('/movement')
        