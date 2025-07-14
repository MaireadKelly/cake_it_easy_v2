from django.shortcuts import render

""" A view to return to the index page """
def home(request):
    return render(request, 'home/index.html')
