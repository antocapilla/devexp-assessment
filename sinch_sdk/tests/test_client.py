import pytest
import responses
from sinch_sdk import SinchClient, AuthenticationError
from sinch_sdk.models import Contact, Message

@responses.activate
def test_create_contact(client):
    contact_data = {
        "id": "123",
        "name": "John Doe",
        "phone": "+1234567890"
    }
    
    responses.add(
        responses.POST,
        "http://localhost:3000/contacts",
        json=contact_data,
        status=201
    )
    
    contact = client.create_contact(
        name="John Doe",
        phone="+1234567890"
    )
    
    assert isinstance(contact, Contact)
    assert contact.id == "123"
    assert contact.name == "John Doe"
    assert contact.phone == "+1234567890"

@responses.activate
def test_send_message(client):
    message_data = {
        "id": "456",
        "from": "+1987654321",
        "to": {"id": "123"},
        "content": "Hello!",
        "status": "queued",
        "created_at": "2024-01-01T12:00:00Z"
    }
    
    responses.add(
        responses.POST,
        "http://localhost:3000/messages",
        json=message_data,
        status=201
    )
    
    message = client.send_message(
        from_="+1987654321",
        to={"id": "123"},
        content="Hello!"
    )
    
    assert isinstance(message, Message)
    assert message.id == "456"
    assert message.status == "queued"