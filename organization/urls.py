from django.urls import path
from .views import OrganizationsListView, OrganizationView, DivisionsListView, DivisionView, PositionsListView, \
    PositionView, EmployeesListView, EmployeeView, PermissionsListView, PermissionView

urlpatterns = [
    path('organizations/', OrganizationsListView.as_view(), name='organization_list'),
    path('organizations/<int:organization_id>/', OrganizationView.as_view(), name='organization'),
    path('divisions/', DivisionsListView.as_view(), name='division_list'),
    path('divisions/<int:division_id>/', DivisionView.as_view(), name='division'),
    path('positions/', PositionsListView.as_view(), name='position_list'),
    path('positions/<int:position_id>/', PositionView.as_view(), name='position'),
    path('employees/', EmployeesListView.as_view(), name='employee_list'),
    path('employees/<int:employee_id>/', EmployeeView.as_view(), name='employee'),
    path('permissions/', PermissionsListView.as_view(), name='permission_list'),
    path('permissions/<int:permission_id>/', PermissionView.as_view(), name='permission'),
]