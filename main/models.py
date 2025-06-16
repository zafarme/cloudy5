from django.db import models
from users.models import CustomUser
from simple_history.models import HistoricalRecords


class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    parent_contact = models.CharField(max_length=15)

    def __str__(self):
        return self.user.get_full_name()


class Class(models.Model):
    name = models.CharField(max_length=100)
    teacher = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='classes')
    students = models.ManyToManyField(Student, related_name='classes')
    schedule = models.TextField()
    history = HistoricalRecords()

    def __str__(self):
        return self.namez


class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    present = models.BooleanField()
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.student} - {self.date} - {'Present' if self.present else 'Absent'}"


class Grade(models.Model):
    SUBJECT_CHOICES = [
        ('frontend', 'Frontend'),
        ('backend', 'Backend'),
        ('full_stack', 'Full-Stack')
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.CharField(max_length=15, choices=SUBJECT_CHOICES)
    score = models.IntegerField()
    date = models.DateField()
    year = models.IntegerField()
    month = models.IntegerField()
    history = HistoricalRecords()

    class Meta:
        unique_together = ['student', 'subject', 'date']

    def __str__(self):
        return f"{self.student} - {self.subject} - {self.score}"


class Salary(models.Model):
    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    month = models.DateField()
    planned_salary = models.FloatField()
    actual_salary = models.FloatField()
    payment_date = models.DateField(null=True, blank=True)
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.teacher.username} - {self.month.strftime('%Y-%m')}"


class SalaryHistory(models.Model):
    salary = models.ForeignKey(Salary, on_delete=models.CASCADE)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_date = models.DateField()

    def __str__(self):
        return f"{self.salary} - {self.paid_amount} - {self.paid_date}"
