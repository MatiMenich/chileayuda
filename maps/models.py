from django.db import models


class Category(models.Model):
    category = models.CharField(max_length=50)
    style = models.CharField(max_length=50,default="")
    def __str__(self):
        return self.category
    def get_syle(self):
        return self.style

class Mark(models.Model):
    latitud = models.FloatField()
    longitud = models.FloatField()
    category = models.ForeignKey('Category')
    description = models.CharField(max_length=50)
    def __str__(self):
        return "X= "+ str(self.longitud) + " Y= " + str(self.latitud) + " Categoría= " + str(self.category)
    def get_x(self):
        return self.longitud
    def get_y(self):
        return self.latitud
    def get_marks_by_category(id_category):
        marks = Mark.objects.filter(category=id_category)
        return marks
