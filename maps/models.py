from django.db import models

class CatastrophesManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name)

class Catastrophes(models.Model):

    objects = CatastrophesManager()

    name = models.CharField(max_length=50)
    latitud = models.FloatField()
    longitud = models.FloatField()
    fecha = models.DateField()

    def natural_key(self):
        return (self.name, self.latitud, self.longitud, self.fecha,)
    def __str__(self):
        return self.name+" "+str(self.latitud)+" "+str(self.longitud)
    def get_catastrofes(self):
        catastrofes = []
        c = Catastrophes.objects.all()
        for i in range(len(c)):
            catastrofes.append(Catastrophes.objects.filter(pk=i+1))
        return catastrofes

class StyleManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name)

class Style(models.Model):
    objects = StyleManager()
    name = models.CharField(max_length=10)
    def __str__(self):
        return self.name
    def natural_key(self):
        return self.name

class CategoryManager(models.Manager):
    def get_by_natural_key(self, category, style_key, catastrophe_key):
        style = Style.objects.get_by_natural_key(style_key)
        catastrophe = Catastrophes.objects.get_by_natural_key(catastrophe_key)
        return self.get(category=category, style=style, catastrophe=catastrophe)

class Category(models.Model):
    category = models.CharField(max_length=50)
    style = models.ForeignKey('Style')
    catastrophe = models.ForeignKey('Catastrophes')

    def __str__(self):
        return self.style.name

    def natural_key(self):
        return (self.category,) + self.style.natural_key() + self.catastrophe.natural_key()
    natural_key.dependencies = ['maps.Style','maps.Catastrophes']

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
