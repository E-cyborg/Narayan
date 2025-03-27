from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import Product_Details ,UserProfile
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import os


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



@csrf_exempt  # Use this only for testing; ideally, handle CSRF properly
def add_fav(request, id):
    if request.method == "POST":
        if request.user.is_authenticated:  # Ensure it only processes PUT requests
            product = get_object_or_404(Product_Details, id=id)
            user_profile = UserProfile.objects.filter(user=request.user).first()
            if not user_profile:
                user_profile = UserProfile.objects.create(user=request.user, favorite_items="")
            favorites_list = user_profile.favorite_items.split(',') if user_profile.favorite_items else []
            if str(product.id) in favorites_list:
                messages.info(request, "Item already in Favorites")
                return JsonResponse({"message": "Item already in favorites","favorites": favorites_list}, status=200)

            # Add the new product ID to favorites
            favorites_list.append(str(product.id))
            user_profile.favorite_items = ','.join(favorites_list) 
            user_profile.save()  # Save the updated list

            return JsonResponse({"message": "Item added to favorites"}, status=200)

    return JsonResponse({"error": "Invalid request method"}, status=400)

@csrf_exempt
def remove_fav(request, id):
    if request.method == "DELETE":  
        if request.user.is_authenticated:
            user_profile = UserProfile.objects.filter(user=request.user).first()
            if not user_profile:
                user_profile = UserProfile.objects.create(user=request.user, favorite_items="")
            favorites_list = user_profile.favorite_items.split(',') if user_profile.favorite_items else []
            if str(id) in favorites_list:
                favorites_list.remove(str(id))
                user_profile.favorite_items=','.join(favorites_list)
                user_profile.save()
                return JsonResponse({"message": "Item removed from favorites", "favorites": favorites_list}, status=200)

            return JsonResponse({"error": f"Item not found in favorites=-{id}"}, status=404)

    return JsonResponse({"error": "Invalid request method"}, status=405)


def favorites(request):
    if request.user.is_authenticated:

        """Show list of favorite products"""
        user_profile = UserProfile.objects.filter(user__email=request.user.email).first()
        fav_ids = user_profile.favorite_items.split(',') if user_profile.favorite_items else []
        fav_items = Product_Details.objects.filter(id__in=fav_ids)  # Fetch products

        print(fav_ids)
        return render(request, "favorite.html", {"fav_items":fav_items,"product":fav_items})
    else:
        messages.info(request,"Please login")
        return redirect('login')


# in case of db failure use session
            # if product.id in favorites_list:
            #     messages.info(request,"Item allready in Favorites")
            #     return JsonResponse({"message": "Item already in favorites"}, status=200)

            # favorites_list.append(product.id)
            # request.session['fav'] = favorites_list
            # request.session.modified = True



def More_detail_products(request,id):
    product= get_object_or_404(Product_Details,id=id)
    image_paths = {}

    # Loop to check for up to 4 images
    for i in range(4):
        image_path = f'static/image/{product.product_name}/{i}.png'
        if os.path.exists(image_path):
            image_paths[f'image{i+1}'] = f"/static/image/{product.product_name}/{i}.png"

    # Pass both product and images to the template
    return render(request, "product.html", {"product_d": product, "images": image_paths})

