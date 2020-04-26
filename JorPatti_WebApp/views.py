from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
#from JorPatti_WebApp.My_test.main import c
from JorPatti_WebApp import My_test 

# Create your views here.

def index(request):
	return render(request, "Card_Game/gameplay.html")

def basic(request):
	#c = {"cards":["AC.png","AD.png","AH.png","AS.png"]}
	
	List_of_Player_with_Cards = My_test.main()

	return render(request, "Card_Game/basic.html", context = List_of_Player_with_Cards)

def print_from_button(request):

    if(request.GET.get('print_btn')):
        print( int(request.GET.get('mytextbox')) )
        print('Button clicked')
    return render(request, 'Card_Game/basic.html',{'value':'Button clicked'})