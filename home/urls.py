from django.urls import path
from home import views

urlpatterns = [
    path("",views.index,name="home"),
    path("contact",views.contact,name="contact"),
    path("Add_to_cart/<int:id>",views.add_to_cart,name="Add_to_cart"),
    path("cart",views.cart,name="cart"),
    path('remove_one_item/<int:id>',views.remove_one_item,name="remove_one_item"),
    path('remove_item/<int:id>',views.remove_item,name="remove_item"),
    path('add_fav-<int:id>',views.add_fav,name="Add_fav"),
    path('remove_fav-<int:id>',views.remove_fav,name="Remove_fav"),
    path('Favorites',views.favorites,name='Favorites'),
    path('products_details-<int:id>/', views.More_detail_products, name="products_details"),
    path('Edit_comment',views.comment_edit,name="edit_comm"),
]
