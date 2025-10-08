from django.shortcuts import render



#! Aqui se agregan las views (templates).
def control(request):
    return render(request, 'home_control.html')


def stock(request):
    return render(request,'stock.html')

def pedidos(request):
    return render(request,'pedidos.html')

def pedido_detail(request):
    return render(request,'pedido_detail.html')
