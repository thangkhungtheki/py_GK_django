from django.http import HttpResponse
# Để render 1 site động
from django.shortcuts import render

def index(request):
    return HttpResponse("Hello all, iam here not tktk.")

def testhtml(request):
    context = {
        "id": 'Chào cc',
        "ct": 'cc'
    }
    return render(request, 'gkcentral/filetest.html', context)