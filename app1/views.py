
from django.shortcuts import redirect, render
from .models import * 
# Create your views here.

def home(request):

    home_list = {
        'explore_products': Product.objects.filter(category__name="explore")
    }

    return render(request, 'home.html', home_list)


def shop(request):

    shop_list = {
        'shop_products': Product.objects.all()
    }

    return render(request, 'shop.html', shop_list)



def chair(request):
    chair_list={
        'explore_products':Product.objects.filter(category__name="explore"),
        'chair_product':Product.objects.filter(category__name='chair')
    }
    
    return render(request, 'chairs.html',chair_list)


def sofa(request):
    sofa_list={
        'sofa_product':Product.objects.filter(category__name='sofa')
    }

    return render(request, 'sofas.html',sofa_list)



def table(request):
    table_list={
        'table_product':Product.objects.filter(category__name='tables')
    }

    return render(request, 'tables.html',table_list)


def beds(request):
    beds_list={
        'beds_product':Product.objects.filter(category__name__iexact='beds')
    }
    
    return render(request,'beds.html',beds_list)

# category__name__iexact iexact kodukunnath backendil letter small capital ayalum kittan an 


def out(request):
    out_list={
        'outdoor_product':Product.objects.filter(category__name__iexact='outdoors')
    }
    
    return render(request,'outdoor.html',out_list)


def about(request):
    return render(request,'about.html')


def service(request):
    home_list={
        'explore_products':Product.objects.filter(category__name="explore"),
    }
    
    return render(request , 'service.html',home_list)


def contact(request):
    return render(request,'contact.html')


from django.contrib import messages
from .forms import CreateUserForm 
def signup(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data.get('username')
            messages.success(request, f'Account created successfully for user {username}!')
            return redirect(user_login)
    else:
        form = CreateUserForm()
    
    return render(request, 'signup.html', {'form': form})




from django.contrib.auth import authenticate,login
from django.contrib.auth.forms import AuthenticationForm  
         
def user_login(request):
    if request.method=='POST':
        form=AuthenticationForm(request,data=request.POST)
        if form.is_valid():
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')
            user=authenticate(username=username,password=password)
            if user is not None:

                login(request,user)
                return redirect('home') 
    else:        
        form=AuthenticationForm()
    return render(request,'login.html',{'form':form})


from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required ##login_required decorator use cheythath user login aayittillenkilum profile pageil varan pattum @login_required means only logged-in users can see the profile page.
def profile_view(request):
    profile,created=Profile.objects.get_or_create(user=request.user)
    return render(request, 'profile.html',{'profile':profile})

    

from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    return redirect('home')
        

# profile-edit
@login_required
def profile_form(request):
    ob, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        ph = request.POST.get('phone')
        em = request.POST.get('email')
        ad = request.POST.get('address')

        ob.phone = ph
        ob.email = em
        ob.address = ad
        ob.save()

        return redirect('profile')
    
    return render(request,'profile_edit.html',{'obs':ob})




# cart ulla bagham

from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product, Cart


# Product => ith model an 
# product_id => url vayi verunna product id an
#  id=product_id:
# URL-il ninn kittiya id use cheyyum
# Database-il same id ulla product find cheyyum
# product=varible aan


# ee function cart model lott product addd cheyyan an
@login_required # login cheythhal mathre veran patollu
def add_to_cart(request, product_id): #product id url vayi verunna annnn
    product = get_object_or_404(Product, id=product_id) #cart il click cheytha product id kond product object kittum get_object_or_404 use cheythath kond product id valid allenkil 404 error varum. valid aayal product object kittum.
    cart_item, created = Cart.objects.get_or_create(user=request.user,product=product)# get_or_create use cheythal, already undenkil create cheyyilla… existing item edukkum… created False aavum illenkil new row create akum
#user=request.user > current user                                     (model fld)    variable (melethe)
# product=product > selected product
    
    if not created: #cart item already undenkil quantity 1 aayi increase cheyyum if not created use cheythath kond.
        cart_item.quantity += 1 
        cart_item.save()
    
    return redirect('cart') #cart pageil redirect cheyyum add to cart click cheythath kond.


#ividenn an cart page il knikunne

@login_required
def cart_page(request):

    cart_vw = Cart.objects.filter(user=request.user) #Login cheytha user-inde cart items mathram kaanikkan vendi aanu.


    # cart il ulllaa ellaa product inteem sum total price edukan an
    total = 0 #defual ayi 0 
    for it in cart_vw: #
        total += it.get_total() #cart lott model ile get_total method call cheyyth, product price um quantity um multiply cheyyth total price kittan vendi aanu.

    return render(request, 'cart.html', {'cart_items': cart_vw,'total': total}) #cart pageil cart itemsum total priceum pass cheyyum render cheythath kond.
                                  # key an ith html lekk   #value an viws il eduthath

def increase_quantity(request, cart_id):

    cart_qy = get_object_or_404(Cart, id=cart_id, user=request.user)

    cart_qy.quantity += 1
    cart_qy.save()

    return redirect('cart')


def decrease_quantity(request, cart_id):

    cart_qy = get_object_or_404(Cart, id=cart_id, user=request.user)

    if cart_qy.quantity > 1:
        cart_qy.quantity -= 1
        cart_qy.save()
    else:
        cart_qy.delete()

    return redirect('cart')


def remove_item(request, cart_id):

    cart_qym = get_object_or_404(Cart, id=cart_id, user=request.user)
    cart_qym.delete()

    return redirect('cart')



from datetime import date, timedelta
# import profile
# checkout pageil cart itemsum total priceum pass cheyyum. checkout form submit cheythal order create cheyyum. order items create cheyyum. cart clear cheyyum. order place aayathinu success message kanikkum. checkout pageil cart items loop cheythu total price calculate cheyyum.
@login_required
# cart_id=None ennu kodukkunnath optional parameter aakkan vendi aanu.
# cart_id illaenkil None aayi varum.
# if cart_id condition use cheythu:
# - cart_id undenkil → single product checkout
# - illaenkil → full cart checkout
def checkout(request, cart_id=None):#cart id none aki koduthu  cart vayi an id vera ividekku varan pattum. cart id url vayi varum. cart id use cheythu specific cart item edukkum. checkout pageil just aa product kaanikkanum total price calculate cheyyum.
    profile, created = Profile.objects.get_or_create(user=request.user)
    # BUY NOW case (one product buy cheyyan click cheythal cart_id url vayi varum. cart_id use cheythu specific cart item edukkum. checkout pageil just aa product kaanikkanum total price calculate cheyyum.)
    if cart_id:
        cart_items = Cart.objects.filter(id=cart_id, user=request.user)
  #varible= Cart mobel ninnum filter cheyth (vanna id ulla item cartil undo enn noki curent user nte ullil ninn edukum)
    else:
        #  Normal cart (cart pageil checkout click cheythal cart_id url vayi varilla. cart_id illaathath kond aa user-inde ella cart items edukkum. checkout pageil aa ellaa products kaanikkanum total price calculate cheyyum.)
        cart_items = Cart.objects.filter(user=request.user)


    total = 0
    for ii in cart_items:
        total += ii.get_total()


    # html form submit cheythal order create cheyyum. order items create cheyyum. cart clear cheyyum.
    if request.method == "POST":
        adr = request.POST.get('address')
        ph = request.POST.get('phone')
        deliverydate = date.today() + timedelta(days=5)

        #User oru order place cheythu ennu database-il save cheyyunnu
        created_order = Order.objects.create(
            user=request.user,
            address=adr,
            phone=ph,
            total_amount=total,
            delivery_date=deliverydate
        )

        for it in cart_items:
            OrderItem.objects.create(
                order=created_order, #order item create cheyyan vendi aanu. order item um order um product um quantity um price um store cheyyum.
                product=it.product,
                quantity=it.quantity,
                price=it.product.price
            )

        #  checkout aayathinu sesham cart clear cheyyum. cart items delete cheyyum.
        if cart_id:
            cart_items.delete()   # single item delete
        else:
            Cart.objects.filter(user=request.user).delete() #full cart delete cheyyum. user-inde ella cart items delete cheyyum.

        return redirect('thankyou')

    #user page il kerumbol ithan adhym run aka
    return render(request, 'checkout.html', {
        'checkout_items': cart_items,
        'total': total,
        'profile': profile 
    })
  

@login_required
def buy_now(request, product_id):
    product = get_object_or_404(Product, id=product_id)


    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product
    )

    # already undenkil quantity increase
    if not created:
        cart_item.quantity += 1
        cart_item.save()


    return redirect('checkout_one', cart_id=cart_item.id)
    
@login_required
def thankyou(request):
    return render(request,'thankyou.html')



@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    

    return render(request, 'my_orders.html', {
        'orders': orders,
    })
    
    

     
def search(request):
    query = request.GET.get('q')
    results = None

    if query:
        results = Product.objects.filter(name__icontains=query
        )| Product.objects.filter(description__icontains=query
        )| Product.objects.filter(category__name__icontains=query
        )
    return render(request, 'search.html', {
        'results': results,
        'query': query
    })
    
    

@login_required
def product_detail(request, product_id):#product detail pageil specific productinte details kaanikkan vendi aanu. product_id url vayi varum. get_object_or_404 use cheythu product id valid allenkil 404 error varum. valid aayal product object kittum. product object pass cheythu product_detail.html render cheyyum.
    prdt = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': prdt})





@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    Wishlist.objects.get_or_create(user=request.user,product=product)

    return redirect('wishlist')

@login_required
def wishlist_page(request):
    items = Wishlist.objects.filter(user=request.user)

    return render(request, 'wishlist.html', {'wishlist_items': items})
    

@login_required
def remove_wishlist(request, id):
    item = get_object_or_404(Wishlist, id=id, user=request.user)
    item.delete()
    return redirect('wishlist')
