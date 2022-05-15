import json

# import stripe
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
from .forms import OrderForm
from basket.basket import Basket
# from orders.views import payment_confirmation


# def order_placed(request):
#     basket = Basket(request)
#     basket.clear()
#     return render(request, 'payment/orderplaced.html')


# class Error(TemplateView):
#     template_name = 'payment/error.html'


@login_required
def BasketView(request):

    basket = Basket(request)
    total = basket.get_total_price()
    # total = total.replace('.', '')
    # total = int(total)

    if request.method == 'POST':
        orderingForm = OrderForm(request.POST)

        if orderingForm.is_valid():
            order = orderingForm.save(commit=False)
            order.user = request.user
            order.full_name = orderingForm.cleaned_data['full_name']
            # order.email = orderingForm.cleaned_data['email']
            order.address = orderingForm.cleaned_data['address']
            order.total_paid = total
            order.save()
            clean_basket(request)
            return render(request, 'account/user/dashboard.html')
    else:
        orderingForm = OrderForm()

    return render(request, 'payment/home.html', {'form': orderingForm})


def clean_basket(request):
    basket = Basket(request)
    basket.clear()
    # basketqty = basket.__len__()
    # baskettotal = basket.get_total_price()
    # response = JsonResponse({'qty': basketqty, 'subtotal': baskettotal})
    # return response



