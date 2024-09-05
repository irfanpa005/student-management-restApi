from django.forms import ValidationError
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Student
from .serializers import StudentSerializer
from django_filters import rest_framework as filters
from rest_framework.pagination import PageNumberPagination

# Create your views here.
class StudentFilter(filters.FilterSet):
    first_name = filters.CharFilter(lookup_expr='icontains')
    last_name = filters.CharFilter(lookup_expr='icontains')
    course = filters.CharFilter(lookup_expr='icontains')
    gpa = filters.RangeFilter()

    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'course', 'gpa']

class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'

class StudentsViewSet(viewsets.ModelViewSet):
    serializer_class = StudentSerializer
    queryset = Student.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = StudentFilter
    pagination_class = CustomPagination

    def list(self, request):
        queryset = self.get_queryset()
        paginated_query_set = self.paginate_queryset(queryset)
        serializer = StudentSerializer(paginated_query_set, many=True)
        return self.get_paginated_response({
            "students": serializer.data,
            "status": status.HTTP_200_OK
        })
    
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
