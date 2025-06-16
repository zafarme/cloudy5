from django.contrib import admin
from .models import Student, Class, Salary, Grade, Attendance
from simple_history.admin import SimpleHistoryAdmin

admin.site.register(Student)
admin.site.register(Class)
admin.site.register(Grade, SimpleHistoryAdmin)
admin.site.register(Salary, SimpleHistoryAdmin)
admin.site.register(Attendance, SimpleHistoryAdmin)
