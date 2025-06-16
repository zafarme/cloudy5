from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Avg, Count
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from main.models import Grade, Student, Class, Salary, Attendance, SalaryHistory
from .serializers import AttendanceSerializer, StudentSerializer, SalarySerializer, ClassSerializer, \
    GradeSerializer, HistorySerializer, StudentStatisticsSerializer

from users.models import CustomUser
from users.permissions import IsTeacher, IsAccountant, IsSalesManager




class HistoryViewSet(ReadOnlyModelViewSet):
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        model = self.kwargs['model']
        if model == 'salary':
            return get_history_model_for_model(Salary).objects.all()
        elif model == 'attendance':
            return get_history_model_for_model(Attendance).objects.all()
        elif model == 'grade':
            return get_history_model_for_model(Grade).objects.all()
        else:
            return None


class AttendanceViewSet(ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated, IsTeacher]


class StudentViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]


class SalaryViewSet(ModelViewSet):
    queryset = Salary.objects.all()
    serializer_class = SalarySerializer
    permission_classes = [IsAuthenticated, IsAccountant]


class ClassViewSet(ModelViewSet):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer
    permission_classes = [IsAuthenticated, IsSalesManager]


class GradeViewSet(ModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    permission_classes = [IsAuthenticated, IsTeacher]

    def update(self, request, *args, **kwargs):
        return Response({'error': "Редактирование оценок запрещено."}, status=400)

    @action(detail=False, methods=['get'], url_path='statistics/(?P<student_id>[^/.]+)')
    def statistics(self, request, student_id=None):
        grades = Grade.objects.filter(student_id=student_id)
        avg_score = grades.aggregate(average=Avg('score'))
        subject_stats = grades.values('subject').annotate(avg=Avg('score'), count=Count('id'))
        return Response({
            'average_score': avg_score['average'],
            "by_subject": subject_stats
        })


@api_view(['GET'])
def student_statistics(request):
    if not request.user.is_authenticated:
        return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

    serializer = StudentStatisticsSerializer(data=request.GET)
    if serializer.is_valid():
        student_id = serializer.validated_data['student_id']
        year = serializer.validated_data['year']
        month = serializer.validated_data['month']

        try:
            student = Student.objects.get(id=student_id)
        except Student.DoesNotExist:
            return Response({"error": "Student not found"}, status=404)

        grades = Grade.objects.filter(student_id=student_id, year=year, month=month)
        attendance = Attendance.objects.filter(student_id=student_id, date__year=year, date__month=month)

        grades_data = {g.subject: g.score for g in grades}
        total_days = attendance.count()
        present_days = attendance.filter(present=True).count()
        absent_days = total_days - present_days

        student_data = StudentSerializer(student).data

        return Response({
            "student": student_data,
            "grades": grades_data,
            "attendance": {
                "total_days": total_days,
                "present": present_days,
                "absent": absent_days
            }
        })

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def salary_attendance(request):
    if not request.user.is_authenticated:
        return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

    serializer = SalaryAttendanceSerializer(data=request.GET)
    if serializer.is_valid():
        employee_id = serializer.validated_data['employee_id']
        year = serializer.validated_data['year']
        month = serializer.validated_data['month']

        try:
            salary = Salary.objects.get(employee_id=employee_id, year=year, month=month)
        except Salary.DoesNotExist:
            salary = None

        attendance = EmployeeAttendance.objects.filter(employee_id=employee_id, date__year=year, date__month=month)
        total_days = attendance.count()
        present_days = attendance.filter(present=True).count()

        return Response({
            "salary": {
                "amount": salary.amount if salary else 0,
                "currency": "UZS"
            },
            "attendance": {
                "total_days": total_days,
                "present": present_days,
                "absent": total_days - present_days
            }
        })

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def mobile_access(request):
    token = request.headers.get('Authorization')
    if token == 'Bearer demo_token_123':
        return Response({"message": "Access granted"})
    return Response({"message": "Access denied"}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def obtain_token(request):
    username = request.data.get('username')
    password = request.data.get('password')

    try:
        user = User.objects.get(username=username)
        if user.check_password(password):
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            return Response({'error': 'Incorrect password'}, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
