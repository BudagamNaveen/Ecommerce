from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegistrationForm,UserUpdateForm,ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from shop.views import extra,searchfunction,Pagination,cartcount


# Create your views here.
def Registration(request):
	if request.method == 'POST':
		form = UserRegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			messages.success(request,f'Your account has been created! You are now able to log in')
			return redirect('Login')
	else:
		form = UserRegistrationForm()
	return render(request,'users/Register.html',{ 'form' : form })

@login_required
def Profile(request):
    Listofmains = extra(request) 
    order_obj = cartcount(request)
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

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('Profile')

    else:
        u_form = UserUpdateForm(instance=request.user)

    context = {
        'u_form': u_form,
        'Listofmains' : Listofmains
    }

    return render(request, 'users/Profile.html', context)

# @login_required
# def Profile(request):
# 	if request.method == 'POST':
# 		u_form = UserUpdateForm(request.POST,instance=request.user)
# 		p_form = ProfileUpdateForm(request.POST,instance=request.user)
# 		if u_form.is_valid() and p_form.is_valid():
# 			u_form.save()
# 			p_form.save()
#         	messages.success(request,'Your account has been updated!')
#         	return redirect('Profile')
#     else:
#     	u_form = UserUpdateForm(instance=request.user)
#     	p_form = ProfileUpdateForm(instance=request.user.profile)

#         context ={
#         	'u_form' : u_form,
#         	'p_form' : p_form
#         }

# 	return render(request, 'users/Profile.html', context)