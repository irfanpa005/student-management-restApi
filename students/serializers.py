from rest_framework import serializers
from .models import Student
import re

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'
    
    def validate_first_name(self, value):
        if not re.match("^[a-zA-Z\s\-]+$", value):
            raise serializers.ValidationError("Name shouldnot have special characters.")
        return value

    def validate_last_name(self, value):
        if not re.match("^[a-zA-Z\s\-]+$", value):
            raise serializers.ValidationError("Name shouldnot have special characters.")
        return value

    # Validate that gpa is between 0.0 and 4.0.
    def validate_gpa(self, value):
        if value < 0.0 or value > 4.0:
            raise serializers.ValidationError("GPA must be between 0.0 and 4.0")
        return value