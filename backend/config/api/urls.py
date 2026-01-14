from django.urls import path
from .views import (
    token_obtain_pair_view,
    token_refresh_view,
    employee_list,
    employee_create,
    employee_detail,
    employee_update,
    employee_delete
)

urlpatterns = [
    path('token/', token_obtain_pair_view, name='token_obtain_pair'),
    path('token/refresh/', token_refresh_view, name='token_refresh'),
    path('employees/', employee_list, name='employee-list'),
    path('employees/create/', employee_create, name='employee-create'),
    path('employees/<int:pk>/', employee_detail, name='employee-detail'),
    path('employees/<int:pk>/update/', employee_update, name='employee-update'),
    path('employees/<int:pk>/delete/', employee_delete, name='employee-delete'),
]
