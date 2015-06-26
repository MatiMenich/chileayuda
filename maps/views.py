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
			des = markform.cleaned_data['description']
			cat = markform.cleaned_data['category']
			lat = markform.cleaned_data['latitud']
			lon = markform.cleaned_data['longitud']
			idmap = markform.cleaned_data['idmap']
			catas = Catastrophes.objects.get(pk=int(idmap[3:]))
			new_mark = Mark(latitud=lat, longitud=lon, description=des, category=cat, catastrophe=catas)
			new_mark.save()
			return HttpResponseRedirect(reverse("maps.views.home"))

	s = Mark.get_marks_groupBy_catastrophe(Mark)
	serialized_obj = encodeJson(s)
	number_catastrophes = len(s)
	categories = Category.objects.all()
	categories2 = encodeJson2(Category.get_categories_by_cat(Category)) #categorias separadas por catastrofes
	# usar en el html de la misma forma, pero tratar esta variable como arreglo
	return render_to_response("test.html", locals(), context_instance = RequestContext(request))

def encodeJson(object):
	string = '['
	for cat in object:
		string2 = "["
		for var in cat:
			string2 += serializers.serialize('json', var) + ","
		string2 = string2[:len(string2)-1] + "]"
		string += string2 +","
	return string[:len(string)-1] + "]"
def encodeJson2(object):
	string = '['
	for cat in object:
		string+= serializers.serialize('json',cat)+ ","
	return string[:len(string)-1] + "]"
