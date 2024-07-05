from django.urls import path

from . import views

urlpatterns = [
    path("profile/", views.ProfileUserView.as_view()),

    path("organization/", views.OrganizationView.as_view()),
    path("organization/<int:pk>/", views.OrganizationDetailView.as_view()),
    path("organization/<int:org_id>/user/", views.OrganizationUserListView.as_view()),

    path('professor/workshop/', views.ProfessorWorkshopView.as_view()),
    path('professor/', views.StudentProfessorView.as_view()),

    path('student/workshop/', views.StudentWorkShopView.as_view()),
    path('student/all_workshop/', views.StudentNotInWorkshopView.as_view()),

    path('workshop/', views.WorkshopView.as_view()),
    path('workshop/<int:pk>/', views.WorkshopDetailView.as_view()),

    path('workshop/<int:workshop_pk>/user/', views.LoginWorkshopView.as_view()),
    path('workshop/<int:workshop_pk>/user/<int:pk>/', views.LoginWorkshopDetailView.as_view()),
]