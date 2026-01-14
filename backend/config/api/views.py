from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

from .models import Employee
from .serializers import EmployeeSerializer


# ========================
# JWT AUTH VIEWS
# ========================

@api_view(['POST'])
@permission_classes([AllowAny])
def token_obtain_pair_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)
    if user:
        refresh = RefreshToken.for_user(user)
        return Response({
            "success": True,
            "message": "Login successful",
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        }, status=status.HTTP_200_OK)

    return Response({
        "success": False,
        "message": "Invalid credentials"
    }, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([AllowAny])
def token_refresh_view(request):
    refresh_token = request.data.get('refresh')

    if not refresh_token:
        return Response({
            "success": False,
            "message": "Refresh token required"
        }, status=status.HTTP_400_BAD_REQUEST)

    try:
        refresh = RefreshToken(refresh_token)
        return Response({
            "success": True,
            "message": "Access token refreshed",
            "access": str(refresh.access_token)
        }, status=status.HTTP_200_OK)

    except Exception:
        return Response({
            "success": False,
            "message": "Invalid refresh token"
        }, status=status.HTTP_400_BAD_REQUEST)


# ========================
# EMPLOYEE VIEWS
# ========================
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def employee_list(request):
    employees = Employee.objects.all().order_by('-date_joined')

    department = request.GET.get('department')
    role = request.GET.get('role')

    if department:
        employees = employees.filter(department__iexact=department)
    if role:
        employees = employees.filter(role__iexact=role)

    paginator = PageNumberPagination()
    paginator.page_size = 3
    paginated_employees = paginator.paginate_queryset(employees, request)

    serializer = EmployeeSerializer(paginated_employees, many=True)

    return paginator.get_paginated_response({
        "success": True,
        "status_code": status.HTTP_200_OK,
        "message": "Employees retrieved successfully",
        "data": serializer.data
    })



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def employee_create(request):
    serializer = EmployeeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            "success": True,
            "message": "Employee created successfully",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)

    return Response({
        "success": False,
        "message": "Validation error",
        "errors": serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def employee_detail(request, pk):
    try:
        employee = Employee.objects.get(pk=pk)
    except Employee.DoesNotExist:
        return Response({
            "success": False,
            "message": "Employee not found"
        }, status=status.HTTP_404_NOT_FOUND)

    serializer = EmployeeSerializer(employee)
    return Response({
        "success": True,
        "message": "Employee retrieved successfully",
        "data": serializer.data
    }, status=status.HTTP_200_OK)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def employee_update(request, pk):
    try:
        employee = Employee.objects.get(pk=pk)
    except Employee.DoesNotExist:
        return Response({
            "success": False,
            "message": "Employee not found"
        }, status=status.HTTP_404_NOT_FOUND)

    serializer = EmployeeSerializer(
        employee,
        data=request.data,
        partial=True  # allows partial updates (email optional)
    )

    if serializer.is_valid():
        serializer.save()
        return Response({
            "success": True,
            "message": "Employee updated successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    return Response({
        "success": False,
        "message": "Validation error",
        "errors": serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def employee_delete(request, pk):
    try:
        employee = Employee.objects.get(pk=pk)
    except Employee.DoesNotExist:
        return Response({
            "success": False,
            "status_code": status.HTTP_404_NOT_FOUND,
            "message": "Employee not found"
        }, status=status.HTTP_404_NOT_FOUND)

    deleted_data = {
        "id": employee.id,
        "name": employee.name,
        "email": employee.email
    }

    employee.delete()

    return Response({
        "success": True,
        "status_code": status.HTTP_200_OK,
        "message": "Employee deleted successfully",
        "deleted_employee": deleted_data
    }, status=status.HTTP_200_OK)

