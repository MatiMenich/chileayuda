from django.db import models

class Catastrophes(models.Model):
    name = models.CharField(max_length=50)
    latitud = models.FloatField()
    longitud = models.FloatField()
    fecha = models.DateField()
    def __str__(self):
        return self.name+" "+str(self.latitud)+" "+str(self.longitud)
    def get_catastrofes(self):
        catastrofes = []
        c = Catastrophes.objects.all()
        for i in range(len(c)):
            catastrofes.append(Catastrophes.objects.filter(pk=i+1))
        return catastrofes


class Category(models.Model):
    category = models.CharField(max_length=50)
    style = models.CharField(max_length=50, default="")
    catastrophe = models.ForeignKey('Catastrophes')

    def __str__(self):
        return self.category

    def get_syle(self):
        return self.style

    def get_by_catastrophe(id_catastrophe):
        return Category.objects.filter(catastrophe=id_catastrophe)
    def get_categories_by_cat(self):
        cats = []
        catastrophes = Catastrophes.objects.all()
        for c in catastrophes:
            cats.append(self.get_by_catastrophe(c.pk))
        return cats



class Mark(models.Model):
    latitud = models.FloatField()
    longitud = models.FloatField()
    category = models.ForeignKey('Category')
    description = models.CharField(max_length=50)
    catastrophe = models.ForeignKey('Catastrophes')

    def __str__(self):
        return "X= " + str(self.longitud) + " Y= " + str(self.latitud) + " Categoria= " + str(self.category)

    def get_x(self):
        return self.longitud

    def get_y(self):
        return self.latitud

    def get_marks_by_category(id_category):
        marks = Mark.objects.filter(category=id_category)
        return marks

    def get_marks_groupBy_category(id_catastrofe):
        marcadores = []
        categorias = Category.get_by_catastrophe(id_catastrofe)
        for categoria in categorias:
            marcadores.append(Mark.get_marks_by_category(categoria.pk))
        return marcadores

    def get_marks_groupBy_catastrophe(self):
        catastrofes = []
        c = Catastrophes.objects.all()
        for cat in c:
            catastrofes.append(Mark.get_marks_groupBy_category(cat.pk))
        return catastrofes
