from django.contrib import admin
from django.urls import path, include
from main import views

app_name = "main"

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.employee, name="employee"),
    path("register/", views.register,name="register"),
    path("login/", views.login_request, name="login"),
    path("logout/", views.logout_request, name="logout"),
    path("profile/", views.profile, name="profile"),
    path("edit_profile/", views.edit_profile, name="edit_profile"),
    path("about/", views.about, name="about"),
    path("change_password/", views.change_password, name="change_password"),
    path("add_employee/", views.add_employee, name="add_employee"),
    path("delete_employee/<int:id>/", views.delete_employee, name="delete_employee"),
    path("edit_employee/<int:id>/", views.edit_employee, name="edit_employee"),
    path("detail_employee/<int:id>/", views.detail_employee, name="detail_employee"),
]