from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

from rest_framework.test import APITestCase
from rest_framework import status

from .models import BlockedWebsite, FocusSession


# ==============================
# REGISTRATION
# ==============================

class RegistrationTests(APITestCase):

    def test_register_success(self):
        response = self.client.post(
            "/api/auth/register/",
            {
                "username": "newuser",
                "email": "newuser@example.com",
                "password": "strongpass123"
            }
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            User.objects.filter(username="newuser").exists()
        )

    def test_register_duplicate_username_fails(self):
        User.objects.create_user(
            username="existing",
            password="pass12345"
        )

        response = self.client.post(
            "/api/auth/register/",
            {
                "username": "existing",
                "email": "another@example.com",
                "password": "strongpass123"
            }
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_missing_fields_fails(self):
        response = self.client.post(
            "/api/auth/register/",
            {
                "username": "onlyusername"
            }
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_is_hashed_not_stored_in_plaintext(self):
        self.client.post(
            "/api/auth/register/",
            {
                "username": "secureuser",
                "email": "secure@example.com",
                "password": "strongpass123"
            }
        )

        user = User.objects.get(username="secureuser")

        # The stored hash must never equal the raw password
        self.assertNotEqual(user.password, "strongpass123")
        self.assertTrue(user.check_password("strongpass123"))


# ==============================
# LOGIN / JWT
# ==============================

class LoginTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="loginuser",
            password="strongpass123"
        )

    def test_login_success_returns_tokens(self):
        response = self.client.post(
            "/api/auth/login/",
            {
                "username": "loginuser",
                "password": "strongpass123"
            }
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_wrong_password_fails(self):
        response = self.client.post(
            "/api/auth/login/",
            {
                "username": "loginuser",
                "password": "wrongpassword"
            }
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_refresh_token_returns_new_access_token(self):
        login_response = self.client.post(
            "/api/auth/login/",
            {
                "username": "loginuser",
                "password": "strongpass123"
            }
        )

        refresh_token = login_response.data["refresh"]

        refresh_response = self.client.post(
            "/api/auth/refresh/",
            {"refresh": refresh_token}
        )

        self.assertEqual(refresh_response.status_code, status.HTTP_200_OK)
        self.assertIn("access", refresh_response.data)


# ==============================
# BLOCKED WEBSITES
# ==============================

class BlockedWebsiteTests(APITestCase):

    def setUp(self):
        self.user_a = User.objects.create_user(
            username="user_a",
            password="strongpass123"
        )

        self.user_b = User.objects.create_user(
            username="user_b",
            password="strongpass123"
        )

        self.client.force_authenticate(user=self.user_a)

    def test_websites_list_requires_authentication(self):
        self.client.force_authenticate(user=None)

        response = self.client.get("/api/websites/")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_add_website_success(self):
        response = self.client.post(
            "/api/websites/add/",
            {"domain": "facebook.com"}
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            BlockedWebsite.objects.filter(
                user=self.user_a,
                domain="facebook.com"
            ).exists()
        )

    def test_add_website_missing_domain_fails(self):
        response = self.client.post("/api/websites/add/", {})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_duplicate_active_website_fails(self):
        self.client.post("/api/websites/add/", {"domain": "facebook.com"})

        response = self.client.post(
            "/api/websites/add/",
            {"domain": "facebook.com"}
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_only_shows_own_and_global_websites(self):
        BlockedWebsite.objects.create(
            user=self.user_a,
            domain="own-site.com"
        )

        BlockedWebsite.objects.create(
            user=self.user_b,
            domain="other-users-site.com"
        )

        BlockedWebsite.objects.create(
            user=None,
            domain="global-site.com"
        )

        response = self.client.get("/api/websites/")
        domains = [item["domain"] for item in response.data]

        self.assertIn("own-site.com", domains)
        self.assertIn("global-site.com", domains)
        self.assertNotIn("other-users-site.com", domains)

    def test_remove_website_success(self):
        self.client.post("/api/websites/add/", {"domain": "facebook.com"})

        response = self.client.delete(
            "/api/websites/remove/",
            {"domain": "facebook.com"},
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        website = BlockedWebsite.objects.get(
            user=self.user_a,
            domain="facebook.com"
        )
        self.assertFalse(website.is_active)

    def test_remove_nonexistent_website_returns_404(self):
        response = self.client.delete(
            "/api/websites/remove/",
            {"domain": "doesnotexist.com"},
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_cannot_remove_another_users_website(self):
        # IDOR check: user_a tries to remove a website that
        # belongs to user_b. This must fail — a user should
        # never be able to modify another user's data.
        BlockedWebsite.objects.create(
            user=self.user_b,
            domain="user-b-site.com"
        )

        response = self.client.delete(
            "/api/websites/remove/",
            {"domain": "user-b-site.com"},
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # And user_b's website must still be active/untouched
        website = BlockedWebsite.objects.get(
            user=self.user_b,
            domain="user-b-site.com"
        )
        self.assertTrue(website.is_active)


# ==============================
# FOCUS SESSIONS
# ==============================

class FocusSessionTests(APITestCase):

    def setUp(self):
        self.user_a = User.objects.create_user(
            username="user_a",
            password="strongpass123"
        )

        self.user_b = User.objects.create_user(
            username="user_b",
            password="strongpass123"
        )

        self.client.force_authenticate(user=self.user_a)

    def test_start_session_success(self):
        response = self.client.post(
            "/api/focus/start/",
            {"duration": 25}
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            FocusSession.objects.filter(
                user=self.user_a,
                duration=25
            ).exists()
        )

    def test_start_session_missing_duration_fails(self):
        response = self.client.post("/api/focus/start/", {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_start_session_negative_duration_fails(self):
        response = self.client.post(
            "/api/focus/start/",
            {"duration": -5}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_start_session_non_numeric_duration_fails(self):
        response = self.client.post(
            "/api/focus/start/",
            {"duration": "not-a-number"}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_complete_session_success(self):
        session = FocusSession.objects.create(
            user=self.user_a,
            start_time=timezone.now(),
            duration=25,
            completed=False
        )

        response = self.client.post(f"/api/focus/{session.id}/complete/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        session.refresh_from_db()
        self.assertTrue(session.completed)
        self.assertIsNotNone(session.end_time)

    def test_complete_already_completed_session_fails(self):
        session = FocusSession.objects.create(
            user=self.user_a,
            start_time=timezone.now(),
            duration=25,
            completed=True,
            end_time=timezone.now()
        )

        response = self.client.post(f"/api/focus/{session.id}/complete/")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cannot_complete_another_users_session(self):
        # IDOR check: user_a tries to complete user_b's session.
        # This must fail with 404 — the session shouldn't even be
        # visible to user_a, let alone modifiable.
        session = FocusSession.objects.create(
            user=self.user_b,
            start_time=timezone.now(),
            duration=25,
            completed=False
        )

        response = self.client.post(f"/api/focus/{session.id}/complete/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        session.refresh_from_db()
        self.assertFalse(session.completed)

    def test_history_only_shows_own_sessions(self):
        FocusSession.objects.create(
            user=self.user_a,
            start_time=timezone.now(),
            duration=25,
            completed=True
        )

        FocusSession.objects.create(
            user=self.user_b,
            start_time=timezone.now(),
            duration=45,
            completed=True
        )

        response = self.client.get("/api/focus/history/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["duration"], 25)

    def test_focus_endpoints_require_authentication(self):
        self.client.force_authenticate(user=None)

        response = self.client.post("/api/focus/start/", {"duration": 25})

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)