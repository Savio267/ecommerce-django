from django.shortcuts import render
from shop.models import Category,Products
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages

def allprodcat(request):
    f=Category.objects.all()
    return render(request,'category.html',{'f':f})

def allproducts(request,p):
    f=Category.objects.get(slug=p)
    p=Products.objects.filter(category__slug=p)
    return render(request,'products.html',{'p':p,'f':f})

def detail(request,p):
    p=Products.objects.get(slug=p)
    return render(request,'detail.html',{'p':p})

def register(request):
    if (request.method=="POST"):
        u=request.POST['u']
        f=request.POST['f']
        l=request.POST['l']
        e=request.POST['e']
        p=request.POST['p']
        z=User.objects.create_user(username=u,first_name=f,last_name=l,email=e,password=p)
        z.save()
        messages.success(request, "You have been registered")
    return render(request,'register.html')


def user_login(request):
    if (request.method == "POST"):
      u = request.POST['u']
      p = request.POST['p']
      user = authenticate(username=u, password=p)
      if user:
         login(request,user)
         return allprodcat(request)
      else:
          messages.error(request, "INVALID CREDENTIALS")
    return render(request,'login.html')

def user_logout(request):
    logout(request)
    return render(request,'category.html')
