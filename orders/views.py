from django.shortcuts import render, redirect
from cart.cart import Cart
from .models import OrderItem
from .tasks import order_created
from .forms import OrderCreateForm

def order_create(request):
    cart = Cart(request)
    print(cart)
    if request.method == "POST":
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product =item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            cart.clear()
            order_created.delay(order.id)
            request.session['order_id'] = order.id
            # return render(
            #     request, 'orders/order/created.html', {'order': order}
            # )
            return redirect('payment:process')
    else:
        form = OrderCreateForm()
    return render(
        request, 'orders/order/create.html',
        {'cart': cart, 'form': form}
    )

