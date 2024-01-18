from django.shortcuts import render
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from shop.models import Category
from .tasks import order_created

def order_create(request):
    # Получаем экземпляр корзины из сессии пользователя.
    cart = Cart(request)

    if request.method == 'POST':
        # Если запрос методом POST, обрабатываем форму.
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            # Если форма валидна, сохраняем заказ в базе данных.
            order = form.save()
            # Для каждого товара в корзине создаем объект OrderItem и связываем его с созданным заказом.
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # Очищаем корзину после создания заказа.
            cart.clear()
            # Запускаем асинхронное задание для обработки созданного заказа.
            # order_created.delay(order.id)
            # Рендерим шаблон для отображения страницы успешного создания заказа.
            return render(request,
                          'orders/order/created.html',
                          {'order': order})
    else:
        # Если запрос не методом POST, создаем пустую форму.
        form = OrderCreateForm()

    # Рендерим шаблон для отображения формы создания заказа.
    categories = Category.objects.all()
    return render(request,
                  'orders/order/create.html',
                  {'cart': cart,
                   'form': form,
                   'categories': categories})
