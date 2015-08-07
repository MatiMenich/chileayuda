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
	idCatastrophe = request.GET["idCat"]
	marks = Mark.get_marks_groupBy_category(idCatastrophe)
	categories = Category.get_by_catastrophe(idCatastrophe)
	catastrophe = Catastrophes.find_by_id(idCatastrophe)

	serializedCategories = serializers.serialize('json', categories)
	serializedMarks = encodeArrayOfArray(marks)
	serializedCatastrophe = serializers.serialize('json', [catastrophe])[1:-1]

	markform = MarkForm(idCatastrophe,request.POST or None, prefix="marks")

	if request.method == "POST":
		if markform.is_valid():
			des = markform.cleaned_data['description']
			cat = markform.cleaned_data['category']
			lat = markform.cleaned_data['latitud']
			lon = markform.cleaned_data['longitud']
			idmap = markform.cleaned_data['idmap']
			catas = Catastrophes.objects.get(pk=markform.cleaned_data['catastrophe'])

			new_mark = Mark(latitud=lat, longitud=lon, description=des, category=cat, catastrophe=catas)
			new_mark.save()
			return HttpResponseRedirect("mapa?idCat="+idCatastrophe)

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


def encodeArrayOfArray(arrayOfArray):
	string = '['
	for array in arrayOfArray:
		string += serializers.serialize('json', array) + ","
	return string[:len(string) - 1] + "]"

def encodeJson2(arrayOfArray):
	string = '['
	for array in arrayOfArray:
		string += serializers.serialize('json', array, use_natural_keys=True) + ","
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

		if wizardform.is_valid() and catform.is_valid():
			name = wizardform.cleaned_data['name']
			date = wizardform.cleaned_data['date']
			description = wizardform.cleaned_data['description']
			latitud = wizardform.cleaned_data['latitud']
			longitud = wizardform.cleaned_data['longitud']
			zoom = wizardform.cleaned_data['zoom']
			new_cat = Catastrophes(name=name,fecha=date,description=description,latitud=latitud, longitud=longitud)
			new_cat.save()

			for form in catform:
				catName = form.cleaned_data['name']
				categoryStyle = form.cleaned_data['style']
				new_category = Category(category=catName, style=categoryStyle, catastrophe=new_cat)
				new_category.save()
			return render_to_response("panel.html", locals(), context_instance = RequestContext(request))
		else:
			return render_to_response("panel.html", locals(), context_instance = RequestContext(request))

	return render_to_response("wizard.html", locals(), context_instance = RequestContext(request))

def wizard2(request):
	catastrophes = encodeJson2(Catastrophes.get_catastrofes(Catastrophes))
	print(catastrophes)
	edit_cat = EditCatastropheForm(request.POST or None, prefix="edit_cat")
	wizardform = WizardForm(request.POST or None, prefix="wizard")
	catform = CategoryFormSet(request.POST or None, prefix="category")

	return render_to_response("edit_catastrophe.html", locals(), context_instance = RequestContext(request))
