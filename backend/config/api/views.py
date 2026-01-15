from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.db import DatabaseError, IntegrityError

from .models import Employee
from .serializers import EmployeeSerializer

# ========================
# JWT AUTH VIEWS
# ========================

@api_view(['POST'])
@permission_classes([AllowAny])
def token_obtain_pair_view(request):
    try:
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({
                "success": False,
                "status_code": status.HTTP_400_BAD_REQUEST,
                "message": "Username and password are required",
                "error_type": "MissingFieldsError"
            }, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                "success": True,
                "status_code": status.HTTP_200_OK,
                "message": "Login successful",
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            }, status=status.HTTP_200_OK)

        return Response({
            "success": False,
            "status_code": status.HTTP_401_UNAUTHORIZED,
            "message": "Invalid credentials",
            "error_type": "AuthenticationError"
        }, status=status.HTTP_401_UNAUTHORIZED)

    except Exception as e:
        return Response({
            "success": False,
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": f"An unexpected error occurred: {str(e)}",
            "error_type": "ServerError"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([AllowAny])
def token_refresh_view(request):
    try:
        refresh_token = request.data.get('refresh')

        if not refresh_token:
            return Response({
                "success": False,
                "status_code": status.HTTP_400_BAD_REQUEST,
                "message": "Refresh token required",
                "error_type": "MissingFieldsError"
            }, status=status.HTTP_400_BAD_REQUEST)

        refresh = RefreshToken(refresh_token)
        return Response({
            "success": True,
            "status_code": status.HTTP_200_OK,
            "message": "Access token refreshed",
            "access": str(refresh.access_token)
        }, status=status.HTTP_200_OK)

    except Exception:
        return Response({
            "success": False,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": "Invalid or expired refresh token",
            "error_type": "TokenError"
        }, status=status.HTTP_400_BAD_REQUEST)


# ========================
# EMPLOYEE VIEWS
# ========================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def employee_list(request):
    try:
        employees = Employee.objects.all().order_by('-date_joined')

        department = request.GET.get('department')
        role = request.GET.get('role')

        if department:
            employees = employees.filter(department__iexact=department)
        if role:
            employees = employees.filter(role__iexact=role)

        paginator = PageNumberPagination()
        paginator.page_size = 10
        paginated_employees = paginator.paginate_queryset(employees, request)

        serializer = EmployeeSerializer(paginated_employees, many=True)

        return paginator.get_paginated_response({
            "success": True,
            "status_code": status.HTTP_200_OK,
            "message": "Employees retrieved successfully",
            "data": serializer.data
        })

    except DatabaseError as e:
        return Response({
            "success": False,
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": f"Database error: {str(e)}",
            "error_type": "DatabaseError"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    except Exception as e:
        return Response({
            "success": False,
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": f"An unexpected error occurred: {str(e)}",
            "error_type": "ServerError"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def employee_create(request):
    try:
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "status_code": status.HTTP_201_CREATED,
                "message": "Employee created successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({
            "success": False,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": "Validation error",
            "error_type": "ValidationError",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    except IntegrityError as e:
        return Response({
            "success": False,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": f"Database integrity error: {str(e)}",
            "error_type": "IntegrityError"
        }, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({
            "success": False,
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": f"An unexpected error occurred: {str(e)}",
            "error_type": "ServerError"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def employee_detail(request, pk):
    try:
        employee = Employee.objects.get(pk=pk)
        serializer = EmployeeSerializer(employee)
        return Response({
            "success": True,
            "status_code": status.HTTP_200_OK,
            "message": "Employee retrieved successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    except Employee.DoesNotExist:
        return Response({
            "success": False,
            "status_code": status.HTTP_404_NOT_FOUND,
            "message": "Employee not found",
            "error_type": "NotFoundError"
        }, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({
            "success": False,
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": f"An unexpected error occurred: {str(e)}",
            "error_type": "ServerError"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def employee_update(request, pk):
    try:
        employee = Employee.objects.get(pk=pk)
        serializer = EmployeeSerializer(employee, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "status_code": status.HTTP_200_OK,
                "message": "Employee updated successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)

        return Response({
            "success": False,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": "Validation error",
            "error_type": "ValidationError",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    except Employee.DoesNotExist:
        return Response({
            "success": False,
            "status_code": status.HTTP_404_NOT_FOUND,
            "message": "Employee not found",
            "error_type": "NotFoundError"
        }, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({
            "success": False,
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": f"An unexpected error occurred: {str(e)}",
            "error_type": "ServerError"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def employee_delete(request, pk):
    try:
        employee = Employee.objects.get(pk=pk)
        deleted_data = {"id": employee.id, "name": employee.name, "email": employee.email}
        employee.delete()
        return Response({
            "success": True,
            "status_code": status.HTTP_200_OK,
            "message": "Employee deleted successfully",
            "deleted_employee": deleted_data
        }, status=status.HTTP_200_OK)

    except Employee.DoesNotExist:
        return Response({
            "success": False,
            "status_code": status.HTTP_404_NOT_FOUND,
            "message": "Employee not found",
            "error_type": "NotFoundError"
        }, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({
            "success": False,
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": f"An unexpected error occurred: {str(e)}",
            "error_type": "ServerError"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ========================
# DEPARTMENTS AND ROLES
# ========================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def departments_list(request):
    try:
        departments = Employee.objects.values_list('department', flat=True).distinct().exclude(department__isnull=True).exclude(department='')
        return Response({
            "success": True,
            "status_code": status.HTTP_200_OK,
            "message": "Departments retrieved successfully",
            "data": list(departments)
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            "success": False,
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": f"An unexpected error occurred: {str(e)}",
            "error_type": "ServerError"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def roles_list(request):
    try:
        roles = Employee.objects.values_list('role', flat=True).distinct().exclude(role__isnull=True).exclude(role='')
        return Response({
            "success": True,
            "status_code": status.HTTP_200_OK,
            "message": "Roles retrieved successfully",
            "data": list(roles)
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            "success": False,
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": f"An unexpected error occurred: {str(e)}",
            "error_type": "ServerError"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
