from django.shortcuts import render

# Create your views here.
def quote(request):
    return render(request,'quote.html')
    