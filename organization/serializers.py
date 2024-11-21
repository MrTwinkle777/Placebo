import json
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse


def serialize_object(obj):
    """Сериализация одного объекта"""
    return json.dumps(obj, cls=DjangoJSONEncoder)


def serialize_queryset(queryset):
    """Сериализация QuerySet"""
    return list(queryset.values())