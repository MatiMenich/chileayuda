from django.shortcuts import render, render_to_response, RequestContext
from django.core import serializers
from maps.models import *
from maps.forms import *

def home(request):
    serialized_obj = encodeJson(Mark.get_marks_groupBy_category())
    categories = Category.objects.all() 
    
    markform = MarkForm(request.POST or None, prefix="marks")

    if request.method =="POST":
        print("hola")
    return render_to_response("test.html", locals(), context_instance = RequestContext(request))

def encodeJson(object):
	string = "["
	for var in object:
		string += serializers.serialize('json', var) + ","
	return string[:len(string)-1] + "]"
