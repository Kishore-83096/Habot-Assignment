from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Employee


class EmployeeAPITestCase(APITestCase):

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username="testuser", password="Test@123")

        # Generate JWT token
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

        # Authenticate client
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

        # API URLs
        self.login_url = "/api/token/"
        self.refresh_url = "/api/token/refresh/"
        self.employee_list_url = "/api/employees/"
        self.employee_create_url = "/api/employees/create/"

    # ----------------------
    # JWT AUTH TESTS
    # ----------------------
    def test_login_success(self):
        response = self.client.post(self.login_url, {"username": "testuser", "password": "Test@123"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["success"])
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_invalid_credentials(self):
        response = self.client.post(self.login_url, {"username": "testuser", "password": "wrongpass"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse(response.data["success"])

    def test_refresh_without_token(self):
        response = self.client.post(self.refresh_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data["success"])

    # ----------------------
    # EMPLOYEE CREATION TESTS
    # ----------------------
    def test_create_employee_success(self):
        payload = {"name": "Alice", "email": "alice@test.com", "department": "HR", "role": "Manager"}
        response = self.client.post(self.employee_create_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data["success"])
        self.assertEqual(Employee.objects.count(), 1)

    def test_create_employee_duplicate_email(self):
        Employee.objects.create(name="Alice", email="alice@test.com")
        payload = {"name": "Alice 2", "email": "alice@test.com"}
        response = self.client.post(self.employee_create_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data["success"])
        self.assertIn("email", response.data["errors"])

    # ----------------------
    # EMPLOYEE LIST TESTS
    # ----------------------
    def test_employee_list_pagination(self):
        for i in range(4):
            Employee.objects.create(name=f"Emp{i+1}", email=f"e{i+1}@test.com")
        response = self.client.get(self.employee_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["results"]["success"])
        self.assertEqual(len(response.data["results"]["data"]), 3)  # page_size=3

    def test_employee_filter_department(self):
        Employee.objects.create(name="HR Emp", email="hr@test.com", department="HR")
        Employee.objects.create(name="Tech Emp", email="tech@test.com", department="Engineering")
        response = self.client.get(self.employee_list_url + "?department=HR")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]["data"]), 1)

    # ----------------------
    # EMPLOYEE DETAIL TESTS
    # ----------------------
    def test_employee_detail_success(self):
        emp = Employee.objects.create(name="Bob", email="bob@test.com")
        response = self.client.get(f"/api/employees/{emp.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["success"])

    def test_employee_detail_not_found(self):
        response = self.client.get("/api/employees/999/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertFalse(response.data["success"])

    # ----------------------
    # EMPLOYEE UPDATE TESTS
    # ----------------------
    def test_employee_update_partial(self):
        emp = Employee.objects.create(name="Old Name", email="old@test.com")
        response = self.client.patch(f"/api/employees/{emp.id}/update/", {"department": "Finance"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        emp.refresh_from_db()
        self.assertEqual(emp.department, "Finance")

    def test_employee_update_not_found(self):
        response = self.client.patch("/api/employees/999/update/", {"name": "New"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # ----------------------
    # EMPLOYEE DELETE TESTS
    # ----------------------
    def test_employee_delete_success(self):
        emp = Employee.objects.create(name="Delete Me", email="delete@test.com")
        response = self.client.delete(f"/api/employees/{emp.id}/delete/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["success"])
        self.assertEqual(Employee.objects.count(), 0)

    def test_employee_delete_not_found(self):
        response = self.client.delete("/api/employees/999/delete/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertFalse(response.data["success"])

    # ----------------------
    # UNAUTHORIZED ACCESS TEST
    # ----------------------
    def test_unauthorized_access(self):
        self.client.credentials()  # Remove token
        response = self.client.get(self.employee_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
