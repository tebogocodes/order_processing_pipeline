from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache
from django.conf import settings
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
fromorder_processing.tasks import process_order

@csrf_exempt
def submit_order(request):
    if request.method == "POST":
        data = request.POST
        order = Order.objects.create(
            name=data.get("name"),
            email=data.get("email"),
            product=data.get("product")
        )
        cache.set(f"order:{order.id}", order.status)
        process_order.delay(order.id)
        return JsonResponse({"message": "Order submitted for processing"})

    return JsonResponse({"message": "Invalid request method"})

def check_order_status(request):
    if request.method == "GET":
        order_id = request.GET.get("order_id")
        order = Order.objects.get(id=order_id)
        status = cache.get(f"order:{order.id}")
        if status:
            return JsonResponse({"order_id": order_id, "status": status})
        else:
            return JsonResponse({"message": "Order status not found in cache"})

    return JsonResponse({"message": "Invalid request method"})

def handle_order_task_complete(order_id, status):
    order = Order.objects.get(id=order_id)
    order.status = status
    order.save()
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"order:{order_id}",
        {
            "type": "order_status_update",
            "order_id": order.id,
            "status": status,
        },
    )

def update_order_status_ws(request):
    if request.is_websocket():
        ws = request.websocket
        order_id = request.GET.get("order_id")
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_add)(f"order:{order_id}", ws)
        while ws.is_open:
            msg = async_to_sync(channel_layer.receive)(f"order:{order_id}")
            if msg:
                ws.send(msg)
        async_to_sync(channel_layer.group_discard)(f"order:{order_id}", ws)
    return HttpResponse()