from rest_framework import serializers
from .models import Employee , Client, Project

class EmployeeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Employee
        fields='__all__'


class ClientSerilaizer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields ='__all__'


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"