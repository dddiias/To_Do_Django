from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from tasks.models import Task


class TaskFlowTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="u1", password="Secret123!")
        self.client.force_authenticate(user=self.user)

    def test_create_list_filter_update_delete(self):
        # create 2 tasks
        r1 = self.client.post("/api/tasks/", {
            "title": "T1",
            "status": "pending",
            "due_date": "2025-08-15"
        }, format="json")
        self.assertEqual(r1.status_code, status.HTTP_201_CREATED)
        t1_id = r1.data["id"]

        r2 = self.client.post("/api/tasks/", {
            "title": "T2",
            "status": "done",
            "due_date": "2025-08-18"
        }, format="json")
        self.assertEqual(r2.status_code, status.HTTP_201_CREATED)

        # list all
        r_list = self.client.get("/api/tasks/")
        self.assertEqual(r_list.status_code, status.HTTP_200_OK)
        self.assertEqual(r_list.data["count"], 2)

        # filter by status
        r_f_status = self.client.get("/api/tasks/?status=pending")
        self.assertEqual(r_f_status.data["count"], 1)
        self.assertEqual(r_f_status.data["results"][0]["title"], "T1")

        # filter by due_date exact
        r_due_on = self.client.get("/api/tasks/?due_on=2025-08-15")
        self.assertEqual(r_due_on.data["count"], 1)

        # filter by due_date range
        r_due_range = self.client.get("/api/tasks/?due_from=2025-08-16&due_to=2025-08-20")
        self.assertEqual(r_due_range.data["count"], 1)
        self.assertEqual(r_due_range.data["results"][0]["title"], "T2")

        # patch status
        r_patch = self.client.patch(f"/api/tasks/{t1_id}/", {"status": "archived"}, format="json")
        self.assertEqual(r_patch.status_code, status.HTTP_200_OK)
        self.assertEqual(r_patch.data["status"], "archived")

        # delete
        r_del = self.client.delete(f"/api/tasks/{t1_id}/")
        self.assertEqual(r_del.status_code, status.HTTP_204_NO_CONTENT)

    def test_owner_scope(self):
        """
        Другой пользователь не должен видеть мои задачи.
        """
        me_task = Task.objects.create(owner=self.user, title="Mine", status="pending")
        # второй пользователь
        other = User.objects.create_user(username="u2", password="Secret123!")
        self.client.force_authenticate(user=other)
        r = self.client.get("/api/tasks/")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["count"], 0)
