from django.shortcuts import render,get_object_or_404,redirect,HttpResponse
from .models import (Products,
	OrderItem,
	Order,
	Billing_Address,
	Maincategories,
	Subcategories)
from django.core.paginator import Paginator
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CheckoutForm
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
def HomePage(request):  
	Listofmains = extra(request)   
	order_obj = cartcount(request)
	product_objects = Maincategories.objects.all()

	#Search code
	item_name = request.POST.get('item_name')
	if item_name != '' and item_name is not None:
		product_objects=searchfunction(request,title=item_name)
		product_objects = Pagination(request,objectset=product_objects)
		context ={
			'product_objects' : product_objects,
			'order_obj' : order_obj,
			'Listofmains' : Listofmains
		}
		return render(request,'shop/SearchPage.html',context=context)

	product_objects = Pagination(request,objectset=product_objects)
	
	#other Logic
	context ={
		'product_objects' : product_objects,
		'order_obj' : order_obj,
		'Listofmains' : Listofmains
	}
	return render(request,'shop/HomePage.html',context=context)

def SubCatergory_View(request,id):
	Listofmains = extra(request)     
	order_obj = cartcount(request)
	Subcategories_obj = Subcategories.objects.filter(MainCategory=id)
	Subcategories_obj = Pagination(request,objectset=Subcategories_obj)

	#Search code
	item_name = request.POST.get('item_name')
	if item_name != '' and item_name is not None:
		product_objects=searchfunction(request,title=item_name)
		product_objects = Pagination(request,objectset=product_objects)
		context ={
			'product_objects' : product_objects,
			'order_obj' : order_obj,
			'Listofmains' : Listofmains
		}
		return render(request,'shop/SearchPage.html',context=context)

	context ={
		'order_obj' : order_obj,
		'Listofmains' : Listofmains,
		'Subcategories_obj' : Subcategories_obj
	}
	return render(request,'shop/SubCatergory.html',context=context)

def Products_View(request,id):
	Listofmains = extra(request)  
	order_obj = cartcount(request)
	Products_obj = Products.objects.filter(SubCategory=id)
	Products_obj = Pagination(request,objectset=Products_obj)

	#Search code
	item_name = request.POST.get('item_name')
	if item_name != '' and item_name is not None:
		product_objects=searchfunction(request,title=item_name)
		product_objects = Pagination(request,objectset=product_objects)
		context ={
			'product_objects' : product_objects,
			'order_obj' : order_obj,
			'Listofmains' : Listofmains
		}
		return render(request,'shop/SearchPage.html',context=context)
		
	context={
		'order_obj':order_obj,
		'subcat_id': id,
		'Products_obj' : Products_obj,
		'Listofmains' : Listofmains
			}
	return render(request,'shop/Products.html',context=context)

def Sortingfunc(request,id):
	Listofmains = extra(request)  
	order_obj = cartcount(request)
	Products_obj = Products.objects.filter(SubCategory=id).order_by('discount_price')
	Products_obj = Pagination(request,objectset=Products_obj)

	#Search code
	item_name = request.POST.get('item_name')
	if item_name != '' and item_name is not None:
		product_objects=searchfunction(request,title=item_name)
		product_objects = Pagination(request,objectset=product_objects)
		context ={
			'product_objects' : product_objects,
			'order_obj' : order_obj,
			'Listofmains' : Listofmains
		}
		return render(request,'shop/SearchPage.html',context=context)
		
	context={
		'order_obj' : order_obj,
		'subcat_id': id,
		'Products_obj' : Products_obj,
		'Listofmains' : Listofmains
			}
	return render(request,'shop/Products.html',context=context)

def DetailView(request,id):
	Listofmains = extra(request) 
	order_obj = cartcount(request) 
	product_object = Products.objects.get(id=id)

	#Search code
	item_name = request.POST.get('item_name')
	if item_name != '' and item_name is not None:
		product_objects=searchfunction(request,title=item_name)
		product_objects = Pagination(request,objectset=product_objects)
		context ={
			'product_objects' : product_objects,
			'order_obj' : order_obj,
			'Listofmains' : Listofmains
		}
		return render(request,'shop/SearchPage.html',context=context)
		
	#other Logic
	context ={
		'product_object' : product_object,
		'order_obj' : order_obj,
		'Listofmains' : Listofmains
	}
	return render(request,'shop/Itemdetail.html',context=context)

@login_required
def Addtocart(request,id):
	item = get_object_or_404(Products,id=id)
	order_item,created = OrderItem.objects.get_or_create(
		item=item,
		user=request.user,
		ordered=False
		)
	order_qs = Order.objects.filter(user=request.user,ordered=False)
	if order_qs.exists():
		order = order_qs[0]
		#check order item in order
		if order.items.filter(item__id=item.id).exists():
			order_item.quantity += 1
			order_item.save()
		else:
			order.items.add(order_item)
	else:
		ordered_date = timezone.now()
		order = Order.objects.create(
			user = request.user,
			ordered_date = ordered_date)
		order.items.add(order_item)
	messages.success(request,f"Item has been added to cart!")
	return redirect('DetailView', id=id)

@login_required
def Ordersummary(request):
	Listofmains = extra(request)  
	try:
		order_obj = Order.objects.get(user=request.user,ordered=False)
	except ObjectDoesNotExist:
		order_obj = None

	#Search code
	item_name = request.POST.get('item_name')
	if item_name != '' and item_name is not None:
		product_objects=searchfunction(request,title=item_name)
		product_objects = Pagination(request,objectset=product_objects)
		return render(request,'shop/SearchPage.html',{'product_objects' : product_objects})
	
	context={
		'order_obj' : order_obj,
		'Listofmains' : Listofmains
	}
	return render(request,'shop/ordersummary.html',context=context)

@login_required
def Increment_cart_quantity(request,id):
	item = get_object_or_404(Products,id=id)
	order_item,created = OrderItem.objects.get_or_create(
		item=item,
		user=request.user,
		ordered=False
		)
	order_qs = Order.objects.filter(user=request.user,ordered=False)
	if order_qs.exists():
		order = order_qs[0]
		#check order item in order
		if order.items.filter(item__id=item.id).exists():
			order_item.quantity += 1
			order_item.save()
		else:
			order.items.add(order_item)
	else:
		ordered_date = timezone.now()
		order = Order.objects.create(
			user = request.user,
			ordered_date = ordered_date)
		order.items.add(order_item)
	return redirect('Ordersummary')

@login_required
def remove_single_item_from_cart(request, id):
    item = get_object_or_404(Products, id=id)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__id=item.id).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quantity was updated.")
            return redirect("Ordersummary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("Ordersummary")
    else:
        messages.info(request, "You do not have an active order")
        return redirect("Ordersummary")

@login_required
def RemoveFromcart(request, id):
    item = get_object_or_404(Products, id=id)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__id=item.id).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            messages.info(request, "This item quantity was updated.")
            return redirect("Ordersummary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("Ordersummary")
    else:
        messages.info(request, "You do not have an active order")
        return redirect("Ordersummary")

@login_required
def checkout(request):
	if request.method == 'POST':
		order_obj = Order.objects.get(user=request.user,ordered=False)
		user = request.user
		address = request.POST.get('address',"")
		landmark = request.POST.get('landmark',"")
		city = request.POST.get('city',"")
		country = request.POST.get('country',"")
		zipcode = request.POST.get('zipcode',"")
		billing = Billing_Address(user=user,
			address=address,
			landmark=landmark,
			city=city,
			country=country,
			zipcode=zipcode)
		billing.save()
		order_obj.billing_address = billing
		order_obj.save()
		messages.success(request,"Your order has been placed successfully !")
		return redirect('index')
	return render(request,'shop/checkout.html')

#Extra Functions
def searchfunction(request,title):
	product_objects = Products.objects.filter(title__icontains=title)
	return product_objects

def Pagination(request,objectset):
	paginator = Paginator(objectset,9)
	page = request.GET.get('page')
	product_objects = paginator.get_page(page)
	return product_objects

def cartcount(request):
	if request.user.is_authenticated:
		try:
			order_obj = Order.objects.get(user=request.user,ordered=False)
		except ObjectDoesNotExist:
			order_obj =0
	else:
		order_obj = None
	return order_obj

def extra(request):
	maincats = Maincategories.objects.all()
	olddict ={}
	for i in maincats:
		olddict[i] = Subcategories.objects.filter(MainCategory=i.id)
	return olddict
