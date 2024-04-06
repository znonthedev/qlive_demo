from django.urls import path
from rest_framework_nested import routers
from . import views
from .views import *

urlpatterns = [
    path('remunerations/', RemunerationListCreateView.as_view(), name='remuneration-list-create'),
    path('remunerations/<int:pk>/', RemunerationRetrieveUpdateDestroyView.as_view(), name='remuneration-retrieve-update-destroy'),
]

router = routers.DefaultRouter()
router.register("subject", views.SubjectViewSet)
router.register("teacher", TeacherViewSet, basename='teacher')
router.register("grade", GradeViewSet, basename='grade')


urlpatterns = router.urls + urlpatterns