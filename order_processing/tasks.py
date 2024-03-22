import requests
from celery import shared_task

@shared_task
def process_order(order_id):
    order = Order.objects.get(id=order_id)
    if order.status == "pending":
        response = requests.get(f"http://localhost:3000/orders/{order.id}")
        if response.status_code == 200:
            order.status = "processing"
            order.save()