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

@csrf_exempt
def add_to_cart(request, id):
    if request.method == "POST":
        product = get_object_or_404(Product_Details, id=id)
        cart = request.session.get("cart", {}) 
        if str(id) in cart:
            cart[str(id)] += 1  
        else:
            cart[str(id)] = 1  
        request.session["cart"] = cart  
        request.session.modified = True  
        return JsonResponse({"message": "Cart updated!", "new_status": "1"})

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




# wrong id pass in cart 