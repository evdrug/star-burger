from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Sum, F, FloatField
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View

from foodcartapp.models import Product, Restaurant, Order, RestaurantMenuItem
from restaurateur.utils import distance_points


class Login(forms.Form):
    username = forms.CharField(
        label='Логин', max_length=75, required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Укажите имя пользователя'
        })
    )
    password = forms.CharField(
        label='Пароль', max_length=75, required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        })
    )


class LoginView(View):
    def get(self, request, *args, **kwargs):
        form = Login()
        return render(request, "login.html", context={
            'form': form
        })

    def post(self, request):
        form = Login(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                if user.is_staff:  # FIXME replace with specific permission
                    return redirect("restaurateur:RestaurantView")
                return redirect("start_page")

        return render(request, "login.html", context={
            'form': form,
            'ivalid': True,
        })


class LogoutView(auth_views.LogoutView):
    next_page = reverse_lazy('restaurateur:login')


def is_manager(user):
    return user.is_staff  # FIXME replace with specific permission


@user_passes_test(is_manager, login_url='restaurateur:login')
def view_products(request):
    restaurants = list(Restaurant.objects.order_by('name'))
    products = list(Product.objects.prefetch_related('menu_items'))

    default_availability = {restaurant.id: False for restaurant in restaurants}
    products_with_restaurants = []
    for product in products:
        availability = {
            **default_availability,
            **{item.restaurant_id: item.availability for item in
               product.menu_items.all()},
        }
        orderer_availability = [availability[restaurant.id] for restaurant in
                                restaurants]

        products_with_restaurants.append(
            (product, orderer_availability)
        )

    return render(request, template_name="products_list.html", context={
        'products_with_restaurants': products_with_restaurants,
        'restaurants': restaurants,
    })


@user_passes_test(is_manager, login_url='restaurateur:login')
def view_restaurants(request):
    return render(request, template_name="restaurants_list.html", context={
        'restaurants': Restaurant.objects.all(),
    })


@user_passes_test(is_manager, login_url='restaurateur:login')
def view_orders(request):
    orders = Order.object.order_price()
    menu = RestaurantMenuItem.objects.prefetch_related('restaurant')

    products_in_restaurant = {}
    for position in menu:
        if position.restaurant not in products_in_restaurant:
            products_in_restaurant[position.restaurant] = []
        if position.availability:
            products_in_restaurant[position.restaurant].append(
                position.product_id)

    orders_for_restaurant = []
    for order in orders:
        restaurants = []
        for restaurant, products_restaurant in products_in_restaurant.items():
            products_available = []
            for product_order in order.products.all():
                products_available.append(
                    product_order.product_id in products_restaurant
                )

            if all(products_available):
                restaurants.append(
                    {'name': restaurant.name,
                     'distance_to_client': distance_points(restaurant.address,
                                                           order.address)})
        restaurants.sort(
            key=lambda restaurant: restaurant['distance_to_client'])
        order.restaurants = restaurants
        orders_for_restaurant.append(order)

    return render(request, template_name='order_items.html', context={
        'order_items': orders_for_restaurant
    })
