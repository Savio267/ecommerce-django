from django.shortcuts import render,redirect
from shop.models import Products
from cart.models import Cart,Account,Order

def cartview(request):
    total=0
    user=request.user
    try:
        cart=Cart.objects.filter(user=user)
        for i in cart:
            total+=i.quantity*i.product.price

    except Cart.DoesNotExist:
        pass
    return render(request,'cartview.html',{'cart':cart,'total': total})


def add_to_cart(request,p):
    p=Products.objects.get(id=p)
    user=request.user
    try:
        cart=Cart.objects.get(user=user,product=p)
        if(cart.quantity<cart.product.stock):
            cart.quantity+=1
            cart.save()
    except Cart.DoesNotExist:
            cart=Cart.objects.create(user=user,product=p,quantity=1)
            cart.save()


    return redirect('cart:cartview')


def cart_remove(request,p):
    p = Products.objects.get(id=p)
    user = request.user
    try:
        cart=Cart.objects.get(user=user, product=p)
        if(cart.quantity>1):
            cart.quantity-=1
            cart.save()
        else:
            cart.delete()
    except Cart.DoesNotExist:
        pass
    return redirect('cart:cartview')

def full_remove(request,p):
    p = Products.objects.get(id=p)
    user=request.user
    try:
        cart = Cart.objects.get(user=user, product=p)

        cart.delete()
    except Cart.DoesNotExist:
        pass
    return redirect('cart:cartview')


def orderform(request):
    total=0
    if(request.method=="POST"):
        a=request.POST['a']
        p=request.POST['p']
        n=request.POST['n']
        user=request.user
        cart=Cart.objects.filter(user=user)
        for i in  cart:
            total+=i.quantity*i.product.price
        ac=Account.objects.get(acctnumber=n)
        if(ac.amount>=total):
            ac.amount=ac.amount-total
            ac.save()
            for i in cart:
                o=Order.objects.create(user=user,product=i.product,address=a,phone=p,order_status='Paid',noofitems=i.quantity)
                o.save()
                i.product.stock=i.product.stock-i.quantity
                i.product.save()
            cart.delete()
            msg="Order has been placed successfully"
            return render(request,'orderview.html',{'msg':msg})


    return render(request,'orderform.html')
