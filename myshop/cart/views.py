from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product, Category
from .cart import Cart
from .forms import CartAddProductForm

# Декоратор require_POST гарантирует, что запросы к этим представлениям принимаются только методом POST.

@require_POST
def cart_add(request, product_id):
    # Получаем экземпляр корзины из сессии пользователя.
    cart = Cart(request)
    # Получаем продукт или возвращаем 404, если продукт не найден.
    product = get_object_or_404(Product, id=product_id)
    # Создаем экземпляр формы для добавления продукта в корзину.
    form = CartAddProductForm(request.POST)
    # Проверяем валидность формы.
    if form.is_valid():
        # Получаем очищенные данные из формы.
        cd = form.cleaned_data
        # Добавляем продукт в корзину с указанным количеством.
        cart.add(product=product, quantity=cd['quantity'],
                 override_quantity=cd['override'])
    # Перенаправляем пользователя на страницу корзины.
    return redirect('cart:cart_detail')

# Еще один метод для удаления продукта из корзины.

@require_POST
def cart_remove(request, product_id):
    # Получаем экземпляр корзины из сессии пользователя.
    cart = Cart(request)
    # Получаем продукт или возвращаем 404, если продукт не найден.
    product = get_object_or_404(Product, id=product_id)
    # Удаляем продукт из корзины.
    cart.remove(product)
    # Перенаправляем пользователя на страницу корзины.
    return redirect('cart:cart_detail')

# Представление для отображения содержимого корзины.

def cart_detail(request):
    # Получаем экземпляр корзины из сессии пользователя.
    cart = Cart(request)
    categories = Category.objects.all()
    # Для каждого элемента в корзине добавляем форму для обновления количества.
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
            'quantity': item['quantity'],
            'override': True})
    # Рендерим шаблон с данными о корзине.
    return render(request, 'cart/detail.html', {'cart': cart,
                                                'categories': categories})
