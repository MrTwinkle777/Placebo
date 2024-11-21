import json

from django.http import JsonResponse
from django.views import View
from .models import Organization, Division, Position, Employee, Permission

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from .schemas import OrganizationSchema, DivisionSchema, EmployeeSchema, PermissionSchema, PositionSchema
from marshmallow import ValidationError


@method_decorator(csrf_exempt, name="dispatch")
class OrganizationsListView(View):
    def get(self, request, *args, **kwargs):
        organizations = Organization.objects.all()
        return JsonResponse(OrganizationSchema().dump(organizations, many=True),
                            safe=False)

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            organization_id = data.get("id")

            if organization_id:
                if Organization.objects.filter(pk=organization_id).exists():
                    return JsonResponse({"error": "An organization with this ID already exists."}, status=400)

            organization = OrganizationSchema().load(json.loads(request.body))
        except ValidationError as e:
            return JsonResponse(e.messages, status=400)

        return JsonResponse(OrganizationSchema().dump(organization), status=201)


@method_decorator(csrf_exempt, name="dispatch")
class OrganizationView(View):
    def dispatch(self, request, organization_id, *args, **kwargs):
        try:
            self.organization = Organization.objects.get(pk=organization_id)
        except Organization.DoesNotExist:
            return JsonResponse({"error": "No organization matches the given query"}, status=404)
        self.data = request.body and dict(json.loads(request.body), id=self.organization.id)
        return super(OrganizationView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return JsonResponse(OrganizationSchema().dump(self.organization))

    def put(self, request, *args, **kwargs):
        try:
            self.organization = OrganizationSchema().load(self.data)
        except ValidationError as e:
            return JsonResponse(e.messages, status=400)
        return JsonResponse(OrganizationSchema().dump(self.organization))

    def delete(self, request, *args, **kwargs):
        self.organization.delete()
        return JsonResponse({'message': f'{self.organization} deleted'})


@method_decorator(csrf_exempt, name="dispatch")
class DivisionsListView(View):
    def get(self, request, *args, **kwargs):
        divisions = Division.objects.all()
        return JsonResponse(DivisionSchema().dump(divisions, many=True), safe=False)

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            division_id = data.get("id")

            if division_id:
                if Division.objects.filter(pk=division_id).exists():
                    return JsonResponse({"error": "A division with this ID already exists."}, status=400)

            division = DivisionSchema().load(json.loads(request.body))
        except ValidationError as e:
            return JsonResponse(e.messages, status=400)

        return JsonResponse(OrganizationSchema().dump(division), status=201)


@method_decorator(csrf_exempt, name="dispatch")
class DivisionView(View):
    def dispatch(self, request, division_id, *args, **kwargs):
        try:
            self.division = Division.objects.get(pk=division_id)
        except Division.DoesNotExist:
            return JsonResponse({"error": "No division matches the given query"}, status=404)
        self.data = request.body and dict(json.loads(request.body), id=self.division.id)
        return super(DivisionView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return JsonResponse(DivisionSchema().dump(self.division))

    def put(self, request, *args, **kwargs):
        try:
            self.division = DivisionSchema().load(self.data, partial=True)
        except ValidationError as e:
            return JsonResponse(e.messages, status=400)
        return JsonResponse(DivisionSchema().dump(self.division))

    def delete(self, request, *args, **kwargs):
        self.division.delete()
        return JsonResponse({'message': f'{self.division} deleted'})


@method_decorator(csrf_exempt, name="dispatch")
class PositionsListView(View):
    def get(self, request, *args, **kwargs):
        positions = Position.objects.all()
        return JsonResponse(PositionSchema().dump(positions, many=True), safe=False)

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            position_id = data.get("id")

            if position_id:
                if Position.objects.filter(pk=position_id).exists():
                    return JsonResponse({"error": "A position with this ID already exists."}, status=400)

            position = PositionSchema().load(json.loads(request.body))
        except ValidationError as e:
            return JsonResponse(e.messages, status=400)

        return JsonResponse(OrganizationSchema().dump(position), status=201)


@method_decorator(csrf_exempt, name="dispatch")
class PositionView(View):
    def dispatch(self, request, position_id, *args, **kwargs):
        try:
            self.position = Position.objects.get(pk=position_id)
        except Position.DoesNotExist:
            return JsonResponse({"error": "No division matches the given query"}, status=404)
        self.data = request.body and dict(json.loads(request.body), id=self.position.id)
        return super(PositionView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return JsonResponse(PositionSchema().dump(self.position))

    def put(self, request, *args, **kwargs):
        try:
            self.position = PositionSchema().load(self.data, partial=True)
        except ValidationError as e:
            return JsonResponse(e.messages, status=400)
        return JsonResponse(PositionSchema().dump(self.position))

    def delete(self, request, *args, **kwargs):
        self.position.delete()
        return JsonResponse({'message': f'{self.position} deleted'})

@method_decorator(csrf_exempt, name="dispatch")
class EmployeesListView(View):
    def get(self, request, *args, **kwargs):
        employees = Employee.objects.all()
        return JsonResponse(EmployeeSchema().dump(employees, many=True), safe=False)

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            employee_id = data.get("id")

            if employee_id:
                if Employee.objects.filter(pk=employee_id).exists():
                    return JsonResponse({"error": "A position with this ID already exists."}, status=400)

            employee = EmployeeSchema().load(json.loads(request.body))
        except ValidationError as e:
            return JsonResponse(e.messages, status=400)

        return JsonResponse(EmployeeSchema().dump(employee), status=201)


@method_decorator(csrf_exempt, name="dispatch")
class EmployeeView(View):
    def dispatch(self, request, employee_id, *args, **kwargs):
        try:
            self.employee = Employee.objects.get(pk=employee_id)
        except Employee.DoesNotExist:
            return JsonResponse({"error": "No division matches the given query"}, status=404)
        self.data = request.body and dict(json.loads(request.body), id=self.employee.id)
        return super(EmployeeView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return JsonResponse(EmployeeSchema().dump(self.employee))

    def put(self, request, *args, **kwargs):
        try:
            self.employee = EmployeeSchema().load(self.data, partial=True)
        except ValidationError as e:
            return JsonResponse(e.messages, status=400)
        return JsonResponse(EmployeeSchema().dump(self.employee))

    def delete(self, request, *args, **kwargs):
        self.employee.delete()
        return JsonResponse({'message': f'{self.employee} deleted'})

@method_decorator(csrf_exempt, name="dispatch")
class PermissionsListView(View):
    def get(self, request, *args, **kwargs):
        permissions = Permission.objects.all()
        return JsonResponse(PermissionSchema().dump(permissions, many=True), safe=False)

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            permission_id = data.get("id")

            if permission_id:
                if Permission.objects.filter(pk=permission_id).exists():
                    return JsonResponse({"error": "A position with this ID already exists."}, status=400)

            permission = PermissionSchema().load(json.loads(request.body))
        except ValidationError as e:
            return JsonResponse(e.messages, status=400)

        return JsonResponse(PermissionSchema().dump(permission), status=201)


@method_decorator(csrf_exempt, name="dispatch")
class PermissionView(View):
    def dispatch(self, request, permission_id, *args, **kwargs):
        try:
            self.permission = Permission.objects.get(pk=permission_id)
        except Permission.DoesNotExist:
            return JsonResponse({"error": "No division matches the given query"}, status=404)
        self.data = request.body and dict(json.loads(request.body), id=self.permission.id)
        return super(PermissionView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return JsonResponse(PermissionSchema().dump(self.permission))

    def put(self, request, *args, **kwargs):
        try:
            self.permission = PermissionSchema().load(self.data, partial=True)
        except ValidationError as e:
            return JsonResponse(e.messages, status=400)
        return JsonResponse(PermissionSchema().dump(self.permission))

    def delete(self, request, *args, **kwargs):
        self.permission.delete()
        return JsonResponse({'message': f'{self.permission} deleted'})