from django.shortcuts import render, render_to_response, RequestContext
from django.core import serializers
from maps.models import *
from maps.forms import *
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template.defaulttags import register


def example(request):
	return render_to_response("example.html", locals(), context_instance = RequestContext(request))

def mapa(request):
	markform = MarkForm(request.POST or None, prefix="marks")

	if request.method == "POST":
		if markform.is_valid():
			des = markform.cleaned_data['description']
			cat = markform.cleaned_data['category']
			lat = markform.cleaned_data['latitud']
			lon = markform.cleaned_data['longitud']
			idmap = markform.cleaned_data['idmap']
			catas = Catastrophes.objects.get(pk=int(idmap[3:]))
			new_mark = Mark(latitud=lat, longitud=lon, description=des, category=cat, catastrophe=catas)
			new_mark.save()
			return HttpResponseRedirect(reverse("maps.views.home2"))

	serialized_obj = encodeJson(Mark.get_marks_groupBy_catastrophe(Mark))
	categories2 = Category.get_categories_by_cat(Category)
	serialized_cat = encodeJson2(Catastrophes.get_catastrofes(Catastrophes))
	instance_dict = []
	i = 1
	for cat in Catastrophes.objects.all():
		d = {'place': cat.name, 'idcat':cat.pk, 'idmap': str("map" + str(i)), 'categories': categories2[i - 1]}
		instance_dict.append(d)
		i += 1
	categories = encodeJson2(categories2)

	return render_to_response("mapa.html", locals(), context_instance = RequestContext(request))


def home(request):
	catastrophes = Catastrophes.objects.all()
	return render_to_response("home.html", locals(), context_instance = RequestContext(request))

def encodeJson(object):
	string = '['
	for cat in object:
		string2 = "["
		for var in cat:
			string2 += serializers.serialize('json', var) + ","
		string2 = string2[:len(string2) - 1] + "]"
		string += string2 + ","
	return string[:len(string) - 1] + "]"


def encodeJson2(object):
	string = '['
	for cat in object:
		string += serializers.serialize('json', cat, use_natural_keys = True) + ","
	return string[:len(string) - 1] + "]"


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


def panel(request):
	return render_to_response("panel.html", locals(), context_instance = RequestContext(request))

def wizard(request):
	wizardform = WizardForm(request.POST or None, prefix="wizard")
	catform = CategoryFormSet(request.POST or None, prefix="category")
	if request.method == "POST":

		if wizardform.is_valid():
			name = wizardform.cleaned_data['name']
			latitud = wizardform.cleaned_data['latitud']
			longitud = wizardform.cleaned_data['longitud']
			zoom = wizardform.cleaned_data['zoom']
			new_cat = Catastrophes(latitud=lat, longitud=lon, description=des, category=cat, catastrophe=catas)
			new_mark.save()
		if catform.is_valid():
			print(catform)
			for form in catform:
				print(form.cleaned_data['name']+"   "+str(form.cleaned_data['style']))
				if form.is_valid():
					catName = form.cleaned_data['name']
					catStyle = form.cleaned_data['style']

	return render_to_response("wizard.html", locals(), context_instance = RequestContext(request))

def wizard2(request):
	return render_to_response("wizard2.html", locals(), context_instance = RequestContext(request))
