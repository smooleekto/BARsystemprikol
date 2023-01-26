from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Departaments(models.Model):
    departament_id = models.AutoField(primary_key=True)
    departament = models.CharField(max_length=100)
    def __str__(self):
        return self.departament

class DepartamentGroups(models.Model):
    group_id = models.AutoField(primary_key=True)
    departament = models.ForeignKey(Departaments, on_delete=models.CASCADE)
    group = models.CharField(max_length=5)


class Teachers(models.Model):
    user_id = models.IntegerField(primary_key=True)
    last_name = models.CharField(max_length=20)
    first_name = models.CharField(max_length=20)
    patronymic = models.CharField(max_length=20)
    departament = models.ForeignKey(Departaments, on_delete=models.CASCADE, default=199999)
    quantity = models.IntegerField(default=0)
    def __str__(self):
        return (self.last_name + ' ' + self.first_name + ' ' +self.patronymic)

class TeachersThemes(models.Model):
    theme_id = models.AutoField(primary_key=True)
    theme = models.CharField(max_length=60)
    teacher = models.ForeignKey(Teachers, on_delete=models.CASCADE)
    def __str__(self):
        return (self.theme)

class Students(models.Model):
    user_id = models.IntegerField(primary_key=True, default=199999)
    last_name = models.CharField(max_length=20)
    first_name = models.CharField(max_length=20)
    patronymic = models.CharField(max_length=20)
    group = models.CharField(max_length=5)
    teacher = models.ForeignKey(Teachers, on_delete=models.CASCADE, default=199999)
    theme = models.CharField(max_length=60)
    theme_status = models.CharField(max_length=30, default='Очікується підтвердження')
    def __str__(self):
        return (self.last_name)
    
    @property
    def teacher_lastname(self):
        return self.teacher.last_name

    @property
    def teacher_firstname(self):
        return self.teacher.first_name

    @property
    def teacher_ptr(self):
        return self.teacher.patronymic

class TeacherStudents(models.Model):
    teacherstudent_id = models.AutoField(primary_key=True)
    teacher =  models.ForeignKey(Teachers, on_delete=models.CASCADE)
    student = models.ForeignKey(Students, on_delete=models.CASCADE, default=199999)
    def __str__(self):
        return (self.student)

