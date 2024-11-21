from marshmallow import Schema, ValidationError, fields, validate, validates
from marshmallow.decorators import post_load

from .models import Organization, Division, Position, Employee, Permission

class OrganizationSchema(Schema):
    class Meta(object):
        model = Organization

    id = fields.Integer()
    name = fields.String(validate=validate.Length(max=255))
    description = fields.String()

    @post_load
    def update_or_create(self, data, *args, **kwargs):
        organization_id = data.pop("id", None)
        organization, _ = Organization.objects.update_or_create(id=organization_id, defaults=data)
        return organization


class DivisionSchema(Schema):
    class Meta(object):
        model = Division

    id = fields.Integer()
    name = fields.String(validate=validate.Length(max=255))
    organization = fields.Nested(OrganizationSchema, dump_only=True)
    organization_id = fields.Integer(required=True, load_only=True)
    parent = fields.Nested('self', allow_none=True)
    parent_id = fields.Integer(load_only=True)
    positions = fields.Method("get_positions")
    positions_ids = fields.List(fields.Integer(), required=False, load_only=True)

    def get_positions(self, obj):
        return PositionSchema(many=True).dump(obj.positions.all())

    @validates("parent_id")
    def validate_parent_id(self, parent_id=None):
        if parent_id:
            try:
                self.parent = Division.objects.get(id=parent_id)
            except Division.DoesNotExist:
                raise ValidationError("Invalid parent id.")

    @validates("organization_id")
    def validate_organization_id(self, organization_id):
        try:
            self.organization = Organization.objects.get(id=organization_id)
        except Organization.DoesNotExist:
            raise ValidationError("Invalid organization id.")

    @post_load
    def update_or_create(self, data, *args, **kwargs):
        division_id = data.pop("id", None)
        positions_ids = data.pop("positions_ids", None)

        if positions_ids is not None:
            positions = Position.objects.filter(id__in=positions_ids)
            if positions.count() != len(positions_ids):
                raise ValidationError(
                    {"positions_ids": "Some provided Position IDs do not exist."}
                )
        else:
            positions = []

        division, _ = Division.objects.update_or_create(
            id=division_id, defaults=data
        )
        division.positions.set(positions)

        return division

class EmployeeSchema(Schema):
    class Meta(object):
        model = Employee

    id = fields.Integer()
    first_name = fields.String(validate=validate.Length(max=255))
    last_name = fields.String(validate=validate.Length(max=255))
    positions = fields.Method("get_positions")
    positions_ids = fields.List(fields.Integer(), required=False, load_only=True)

    def get_positions(self, obj):
        return PositionSchema(many=True).dump(obj.positions.all())

    @post_load
    def update_or_create(self, data, *args, **kwargs):
        employee_id = data.pop("id", None)
        positions_ids = data.pop("positions_ids", None)

        if positions_ids is not None:
            positions = Position.objects.filter(id__in=positions_ids)
            if positions.count() != len(positions_ids):
                raise ValidationError(
                    {"positions_ids": "Some provided Position IDs do not exist."}
                )
        else:
            positions = []

        employee, _ = Employee.objects.update_or_create(
            id=employee_id, defaults=data
        )
        employee.positions.set(positions)

        return employee


class PermissionSchema(Schema):
    class Meta(object):
        model = Permission

    id = fields.Integer()
    name = fields.String(validate=validate.Length(max=255))
    description = fields.String()
    positions = fields.Method("get_positions")
    positions_ids = fields.List(fields.Integer(), required=False, load_only=True)

    def get_positions(self, obj):
        return PositionSchema(many=True).dump(obj.positions.all())

    @post_load
    def update_or_create(self, data, *args, **kwargs):
        permission_id = data.pop("id", None)
        positions_ids = data.pop("positions_ids", None)

        if positions_ids is not None:
            positions = Position.objects.filter(id__in=positions_ids)
            if positions.count() != len(positions_ids):
                raise ValidationError(
                    {"positions_ids": "Some provided Position IDs do not exist."}
                )
        else:
            positions = []

        permission, _ = Permission.objects.update_or_create(
            id=permission_id, defaults=data
        )
        permission.positions.set(positions)

        return permission

class PositionSchema(Schema):
    class Meta(object):
        model = Position

    id = fields.Integer()
    name = fields.String(validate=validate.Length(max=255))

    @post_load
    def update_or_create(self, data, *args, **kwargs):
        position_id = data.pop("id", None)

        position, _ = Position.objects.update_or_create(
            id=position_id, defaults=data
        )

        return position