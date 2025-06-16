from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Teacher, Group, Student, Attendance, Grade
from django.contrib.auth.decorators import login_required



@login_required
def teacher_groups(request):
    teacher = Teacher.objects.get(user=request.user)
    groups = teacher.groups.all()
    return render(request, 'botapp/teacher_groups.html', {'groups': groups})


def group_students(request, group_id):
    group = Group.objects.get(id=group_id)
    students = group.students.all()
    return render(request, 'botapp/group_students.html', {'group': group, 'students': students})


@login_required
def mark_attendance(request, student_id, status):
    student = Student.objects.get(id=student_id)

    attendance, created = Attendance.objects.get_or_create(student=student, date=datetime.date.today())
    attendance.status = status
    attendance.save()
    return JsonResponse({'status': 'success', 'attendance': status})


@login_required
def assign_grade(request, student_id, grade_value):
    student = Student.objects.get(id=student_id)
    grade = Grade(student=student, value=grade_value, date=datetime.date.today())
    grade.save()
    return JsonResponse({'status': 'success', 'grade': grade_value})


@login_required
def student_count(request, group_id):
    group = Group.objects.get(id=group_id)
    students = group.students.all()
    return JsonResponse({'status': 'success', 'student_count': len(students)})

