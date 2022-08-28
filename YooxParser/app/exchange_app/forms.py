from django import forms

from .models import Product

class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = (
            'brand',
            'group',
            'old_price',
            'discount',
            'new_price',
            'fullprice',
            'sizes',
            'colors',
            'link',
            'art',
        )
        widgets = {
            'art': forms.TextInput,
        }
