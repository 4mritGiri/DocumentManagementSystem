from django.shortcuts import render

# Create your views here.

def AddDocument(request):
    return render(request, 'DocumentApps/add_document.html')