from django.urls import path
from . import views
urlpatterns = [
    path('generate/',views.GenerateExamAPIView.as_view()),
    path('correct/',views.CorrectExamAPIView.as_view()),
    path('marks/',views.RecordStudentMarkView.as_view()),
    path('download/',views.DownloadStudentMarksCsvView.as_view()),
    path('marks/<int:pk>',views.StudentMarkDetailView.as_view()),
    path('users/', views.UserListCreateView.as_view() ),
    path('users/<int:pk>/', views.UserRetrieveUpdateDestroyView.as_view()),

]
