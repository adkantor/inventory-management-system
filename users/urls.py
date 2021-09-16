from django.urls import path

from .views import (
    EmployeeListView, EmployeeDetailView, 
    EmployeeCreateView,
    EmployeeUpdateView, EmployeeDeleteView
)

urlpatterns = [
    path('', EmployeeListView.as_view(), name='employee_list'),
    path('<int:pk>', EmployeeDetailView.as_view(), name='employee_detail'),
    path('new/', EmployeeCreateView.as_view(), name='employee_create'),
    path('<int:pk>/edit/', EmployeeUpdateView.as_view(), name='employee_edit'),
    path('<int:pk>/delete/', EmployeeDeleteView.as_view(), name='employee_delete'),
]