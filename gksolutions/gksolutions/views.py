from django.http import HttpResponse

def index(request):
    id = request.GET.get('id')
    print(f"ID: {id}")
    return HttpResponse(f"<h1>Welcome to GK Solutions ID: {id} </h1>")