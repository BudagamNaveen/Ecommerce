from django import forms
from .models import Billing_Address

class CheckoutForm(forms.ModelForm):
	class Meta():
		model = Billing_Address
		fields = ('address','landmark','city','country','zipcode')

		widgets={
			'address' : forms.TextInput(attrs={'placeholder':'address'}),
			'landmark' : forms.TextInput(attrs={'placeholder':'landmark'}),
			'city' : forms.TextInput(attrs={'placeholder':'city'}),
			'country' : forms.TextInput(attrs={'placeholder':'country'}),
			'zipcode' : forms.TextInput(attrs={'placeholder':'zipcode'})
		}