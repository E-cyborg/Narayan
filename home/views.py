from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import Product_Details
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

def index(req):
    products = Product_Details.objects.all()
    return render(req, "home.html", {"products": products})

def contact(req):
    return render(req, "contact.html")



# cart views
@csrf_exempt
def add_to_cart(request, id):
    if request.method == "POST":
        product = get_object_or_404(Product_Details, id=id)
        cart = request.session.get("cart", {}) 
        product_id = str(id)
        if product_id in cart:
            cart[product_id] += 1  
        else:
            cart[product_id] = 1  
        request.session["cart"] = cart  
        request.session.modified = True

        # Assuming you can compute new values like quantity and total price
        new_quantity = cart[product_id]
        # Example: calculating the total price for this product
        updated_price = new_quantity * product.price

        return JsonResponse({
            "message": "Cart updated!", 
            "new_status": "1",
            "quantity": new_quantity,
            "updated_price": updated_price
        })

    return JsonResponse({"error": "Invalid request method"}, status=400)

def cart(request):
    if request.method == "GET":
        cart_dict = request.session.get("cart", {})  # Get cart from session
        for x in cart_dict:
            if cart_dict[x]<=0:
                del cart_dict[x]
            request.session['cart']=cart_dict
            request.session.modified = True

        cart_data=request.session.get('cart',{})
        product_ids = cart_dict.keys()
        products = Product_Details.objects.filter(id__in=product_ids)
        cart_items = []
        total = 0
        for i,product in enumerate(products,start=1):
            product_id = str(product.id)
            quantity = cart_dict.get(product_id, 1)
            price = product.price
            total_price = price * quantity

            cart_items.append({
                'id':product.id,
                "product_name": product.product_name,
                "price": price,
                "quantity": quantity,
                "total_price": total_price
            })

            total += total_price  

        cart_data = {
            "items": cart_items,
            "total": total
        }
        return render(request, "cart.html", {"cart": cart_data})


@csrf_exempt
def remove_one_item(request, id):
    if request.method == "POST":
        id=str(id)
        cart_dict = request.session.get("cart", {})  
        for x in cart_dict:
            if cart_dict[x]<=0:
                del cart_dict[x]
            request.session['cart']=cart_dict
            request.session.modified = True

        product_id = str(id)  
        
        if not cart_dict:
            return JsonResponse({"error": "Cart is empty"}, status=400)

        if id in cart_dict:
            if cart_dict[id] > 1:
                cart_dict[product_id] -= 1  
            else:
                del cart_dict[product_id]  

            request.session["cart"] = cart_dict  
            request.session.modified = True  
            total_price = sum(int(qty) * float(request.session.get("prices", {}).get(pid, 0)) for pid, qty in cart_dict.items())

            return JsonResponse({"message": "Item removed", "cart": cart_dict, "total_price": total_price})

        return JsonResponse({"error": "Item not found in cart"}, status=404)

    return JsonResponse({"error": "Invalid request"}, status=400)

@csrf_exempt
def remove_item(request,id):
    if request.method == 'POST':
        cart_dict = request.session.get("cart", {})  
        product_id = str(id)  
        if product_id in cart_dict:
            del cart_dict[product_id]
            request.session['cart']=cart_dict
            request.session.modified = True  
            total_price = sum(int(qty) * float(request.session.get("prices", {}).get(pid, 0)) for pid, qty in cart_dict.items())
            return JsonResponse({"message": "Item removed", "cart": cart_dict, "total_price": total_price})

        return JsonResponse({"error": "Item not found in cart"}, status=404)

    return JsonResponse({"error": "Invalid request"}, status=400)



#  Favorites views
def Add_fav(request, id):
    product = get_object_or_404(Product_Details, id=id)
    favorites_list = request.session.get('fav', [])
    if product.product_name in favorites_list:
        return JsonResponse({"message": "Item already in favorites"}, status=200)
    
    favorites_list.append(product.product_name)
    request.session['fav'] = favorites_list
    request.session.modified = True
    
    return JsonResponse({"message": "Item added to favorites", "favorites": favorites_list}, status=200)


def Remove_fav(request, id):
    product = get_object_or_404(Product_Details, id=id)
    favorites_list = request.session.get('fav', [])

    if product.product_name in favorites_list:
        favorites_list.remove(product.product_name)
        request.session['fav'] = favorites_list
        request.session.modified = True
        return JsonResponse({"message": "Item removed from favorites", "favorites": favorites_list}, status=200)

    return JsonResponse({"error": "Item not found in favorites"}, status=404)


def Favorites(request):
    if request.user.is_authenticated:
        return JsonResponse({"status": "success", "message": "User is authenticated"})
    else:
        return JsonResponse({"status": "error", "message": "User is not authenticated"})
