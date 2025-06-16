from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter


from .views import (
    AttendanceViewSet, StudentViewSet, SalaryViewSet, ClassViewSet,
    GradeViewSet, mobile_access, student_statistics, salary_attendance
)

router = DefaultRouter()
router.register('attendance', AttendanceViewSet, basename='attendance')
router.register('student', StudentViewSet, basename='student')
router.register('salary', SalaryViewSet, basename='salary')
router.register('class', ClassViewSet, basename='class')
router.register('grade', GradeViewSet, basename='grade')


schema_view = get_schema_view(
    openapi.Info(
        title="CLOUDY API",
        default_version="v1",
        description="CLOUD API DOCUMENTATION"
    ),
    public=True,
    permission_classes=(AllowAny,),
)

urlpatterns = [

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),



    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('swagger.<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),


    path('students/statistics/', student_statistics, name='student-statistics'),
    path('employees/salary-attendance/', salary_attendance, name='salary-attendance'),
    path('mobile/access/', mobile_access, name='mobile-access'),
]


urlpatterns += router.urls
