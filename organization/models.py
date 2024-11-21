from django.db import models
from marshmallow import ValidationError


# Create your models here.
class Organization(models.Model):
    """Модель организаии"""
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Position(models.Model):
    """Модель должности"""
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Division(models.Model):
    """Модель подразделения"""
    name = models.CharField(max_length=255)
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='subdivisions',
        on_delete=models.SET_NULL,
    )

    organization = models.ForeignKey(
        'Organization',
        on_delete=models.CASCADE,
        related_name='divisions'
    )

    positions = models.ManyToManyField(
        Position,
        related_name='divisons',
        blank=True
    )

    def clean(self):
        # Проверка на самоссылку
        if self.parent and self.parent.id == self.id:
            raise ValidationError({"parent": "Division cannot be its own parent."})
        super().clean()

    def __str__(self):
        return self.name

class Employee(models.Model):
    """Модель сотрудника"""
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    positions = models.ManyToManyField(
        Position,
        related_name='employees',
        blank=True
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Permission(models.Model):
    """Модель прав"""
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    positions = models.ManyToManyField(
        Position,
        related_name='permissions',
        blank=True
    )

    def __str__(self):
        return self.name