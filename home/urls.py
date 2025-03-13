from django.urls import path
from home import views

urlpatterns = [
    path("",views.index,name="home"),
    path("contact",views.contact,name="contact"),
    path("Add_to_cart/<int:id>",views.add_to_cart,name="Add_to_cart"),
    path("cart",views.cart,name="cart"),
    path('remove_one_item/<int:id>',views.remove_one_item,name="remove_one_item"),
    path('remove_item/<int:id>',views.remove_item,name="remove_item")
]
