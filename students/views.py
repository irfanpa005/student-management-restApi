from django.forms import ValidationError
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Student
from .serializers import StudentSerializer

# Create your views here.

class StudentsViewSet(viewsets.ModelViewSet):
    serializer_class = StudentSerializer
    queryset = Student.objects.all()

def create(self, request, *args, **kwargs):
    try:
        response = super().create(request, *args, **kwargs)
        return Response({
            "message": "Student added successfully",
            "status": status.HTTP_201_CREATED,
            "data": response.data
        }, status=status.HTTP_201_CREATED)
    except ValidationError as e:
        # Handle unique email error
        if 'email' in e.detail:
            return Response({
                "message": "Failed to add student",
                "status": status.HTTP_400_BAD_REQUEST,
                "error": "A student with this email already exists."
            }, status=status.HTTP_400_BAD_REQUEST)
        return Response({
            "message": "Failed to add student",
            "status": status.HTTP_400_BAD_REQUEST,
            "errors": e.detail
        }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({
            "message": "An error occurred while adding the student",
            "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "error": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def update(self, request, *args, **kwargs):
        try:
            response = super().update(request, *args, **kwargs)
            return Response({
                "message": "Student updated successfully",
                "status": status.HTTP_200_OK,
                "data": response.data
            }, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({
                "message": "Failed to update student",
                "status": status.HTTP_400_BAD_REQUEST,
                "errors": e.detail
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "message": "An error occurred while updating the student",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, *args, **kwargs):
        try:
            # Call the parent class's destroy method
            super().destroy(request, *args, **kwargs)
            return Response({
                "message": "Student removed successfully",
                "status": status.HTTP_204_NO_CONTENT,
            }, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({
                "message": "An error occurred while removing the student",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
