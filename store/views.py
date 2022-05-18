from django.shortcuts import get_object_or_404, render
from basket.basket import Basket
from .models import Category, Product


def categories(request):
    return{
        'categories': Category.objects.all()
    }


# def all_products(request):
#     products = Product.objects.filter(is_active=True)
#     return render(request, 'store/home.html', {'products': products})


def all_products(request):
    products = Product.objects.filter(is_active=True)
    currentBasket = Basket(request)
    categoryID = currentBasket.declareWishList()
    advertiseStatus = False
    productsToRecommend = []
    categoryName = ""
    if categoryID != -1:
        advertiseStatus = True
        productsToRecommend = Product.objects.filter(category=categoryID)[:5]
        # category = get_object_or_404(Category, id=categoryID)
        categoryName = categoryID.name

    return render(request, 'store/home.html', {'products': products, 'productsToRecommend': productsToRecommend, 'advertiseStatus': advertiseStatus, 'categoryName': categoryName})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, in_stock=True)
    return render(request, 'store/products/detail.html', {'product': product})


def category_list(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category)
    return render(request, 'store/products/category.html', {'category': category, 'products': products})


def searchDetail(request):
    if request.method == "POST":
        searched = request.POST['searched']
        products = Product.objects.filter(title__contains=searched)
        return render(request, 'store/products/searchDetail.html', {'searched': searched, 'products': products})
    else:
        return render(request, 'store/products/searchDetail.html', {})
