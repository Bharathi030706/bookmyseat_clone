from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

def notify_seat_change(theater_id, seat_data):
    """
    Broadcast seat availability updates to all WebSocket clients
    connected to the given theater.
    seat_data: list of dicts like [{'id': 12, 'is_booked': True}, ...]
    """
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"theater_{theater_id}",
        {
            'type': 'seat_update',
            'seats': seat_data,
        }
    )
