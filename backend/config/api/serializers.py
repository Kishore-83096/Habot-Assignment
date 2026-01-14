from rest_framework import serializers
from .models import Employee

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'name', 'email', 'department', 'role', 'date_joined']
        read_only_fields = ['id', 'date_joined']  # auto-generated fields
