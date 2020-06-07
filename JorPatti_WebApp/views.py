from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render


# Create your views here.

def index(request):
	return render(request, "Card_Game/index.html")

