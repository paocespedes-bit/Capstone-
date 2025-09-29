from django.shortcuts import render


#! Aqui se agregan las views (templates).
def control(request):
    return render(request, 'home_control.html')
