import json
from django.test import TestCase
from django.urls import reverse
from django.conf import settings
from django.core.cache import cache
from order_processing.models import Order
from order_processing.tasks import process_order

class OrderProcessingTestCase(TestCase):

    def setUp(self):
        self.order_data = {
            "name": "John Doe",
            "email": "john.doe@example.com",
            "product": "Example Product"
        }

    def test_submit_order(self):
        response = self.client.post(reverse("submit_order"), data=self.order_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Order submitted for processing"})
        order = Order.objects.get(name=self.order_data["name"])
        self.assertIsNotNone(order)
        self.assertEqual(order.status, "pending")

    def test_check_order_status(self):
        response = self.client.post(reverse("submit_order"), data=self.order_data)
        self.assertEqual(response.status_code, 200)
        order = Order.objects.get(name=self.order_data["name"])
        self.assertIsNotNone(order)
        response = self.client.get(reverse("check_order_status"), data={"order_id": order.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"order_id": order.id, "status": "pending"})

    def test_process_order_task(self):
        order = Order.objects.create(
            name="John Doe",
            email="john.doe@example.com",
            product="Example Product",
            status="pending"
        )
        process_order.apply_async(args=[order.id], queue="order_processing")
        order.refresh_from_db()
        self.assertEqual(order.status, "processing")

    def test_handle_order_task_complete(self):
        order = Order.objects.create(
            name="John Doe",
            email="john.doe@example.com",
            product="Example Product",
            status="processing"
        )
        handle_order_task_complete(order.id, "completed")
        order.refresh_from_db()
        self.assertEqual(order.status, "completed")