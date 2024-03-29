from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from cart.forms import CartAddProductForm

def product_list(request, category_slug=None):
    # Инициализируем переменные категории и товаров.
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    # Если передан слаг категории, фильтруем товары по этой категории.
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    # Рендерим шаблон списка товаров с переданными данными.
    return render(request,
                  'shop/product/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products})

def product_detail(request, id, slug):
    # Получаем объект продукта или 404, если продукт не найден или недоступен.
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    categories = Category.objects.all()

    # Создаем форму для добавления продукта в корзину.
    cart_product_form = CartAddProductForm()

    # Рендерим шаблон деталей продукта с переданными данными.
    return render(request, 'shop/product/detail.html',
                  {'product': product,
                   'categories': categories,
                   'cart_product_form': cart_product_form})
