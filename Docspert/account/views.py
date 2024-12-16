from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest


# Create your views here.
def index(request):
    if request.method == "GET":
        query = request.GET.get("query")
        # Get Accounts matching the query
        return render(request, "index.html", context={"file_upload_success": False})
    elif request.method == "POST":
        file = request.FILES
        print("File", file)
        # Take file, insert items into database, show success message and render the file
        return render(request, "index.html", context={"file_upload_success": False})
    else:
        return HttpResponseBadRequest("Method not allowed")
