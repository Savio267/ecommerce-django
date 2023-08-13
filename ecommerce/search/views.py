from django.shortcuts import render
from shop.models import Products
from django.db.models import Q

def searchresults(request):
    query=""
    product=None
    if(request.method=='POST'):
        query=request.POST['q']
        print(query)
        if(query):
            product=Products.objects.filter(Q(name__icontains=query)| Q(desc__icontains=query))

    return render(request,'search.html',{'product':product,'query':query})

