from django.shortcuts import render
from .models import Product



# homepage + json content
def exchange(request):
    product_list = Product.objects.all()
    return render(request, 'exchange_app/index.html', {"products": product_list})

def documentation(request):
    return render(request, 'exchange_app/documentation.html')

