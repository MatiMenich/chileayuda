from django.shortcuts import render, render_to_response, RequestContext
from django.core import serializers
from maps.models import *

def home(request):
    serialized_obj = serializers.serialize('json', Mark.objects.all())
    categories = Category.objects.all()
    return render_to_response("test.html", locals(), context_instance = RequestContext(request))

