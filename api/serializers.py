from rest_framework import serializers
from main.models import Student, Grade, Class, Attendance, Salary


class HistorySerializer(serializers.ModelSerializer):
    history_user = serializers.StringRelatedField()
    history_date = serializers.DateTimeField()
    history_change_reason = serializers.CharField()

    class Meta:
        fields = '__all__'






class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'


class StudentStatisticsSerializer(serializers.ModelSerializer):
    student_id = serializers.IntegerField()
    year = serializers.IntegerField()
    month = serializers.IntegerField()


class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = '__all__'

    def validate(self, data):
        if self.instance:
            raise  serializers.ValidationError('Редактировать оченку запрешено.')
        return data


class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = '__all__'

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'

class SalarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Salary
        fields = '__all__'