from django.db import models

class Teacher(models.Model):
    name = models.CharField(max_length=100)
    tg_id = models.BigIntegerField(unique=True)

class Group(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

class Student(models.Model):
    name = models.CharField(max_length=100)
    tg_id = models.BigIntegerField(unique=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
