from django.shortcuts import render

# Create your views here.

def homeback(request):
    #return HttpResponse('this Home Page')
    return render(request,'pages/homeback.html')
def home(request):
    #return HttpResponse('this Home Page')
    return render(request,'pages/home.html')