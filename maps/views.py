from django.shortcuts import render, render_to_response, RequestContext
from django.core import serializers
from maps.models import *
from maps.forms import *
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

def home(request):
    markform = MarkForm(request.POST or None, prefix="marks")
    if request.method =="POST":
        if markform.is_valid():
            print(markform)
            des = markform.cleaned_data['description']
            cat = markform.cleaned_data['category']
            lat = markform.cleaned_data['latitud']
            lon = markform.cleaned_data['longitud']
            new_mark = Mark(latitud=lat, longitud=lon, description=des, category=cat)
            new_mark.save()
            return HttpResponseRedirect(reverse("maps.views.home"))

    serialized_obj = encodeJson(Mark.get_marks_groupBy_category())
    categories = Category.objects.all()

    return render_to_response("test.html", locals(), context_instance = RequestContext(request))

def encodeJson(object):
	string = "["
	for var in object:
		string += serializers.serialize('json', var) + ","
	return string[:len(string)-1] + "]"
