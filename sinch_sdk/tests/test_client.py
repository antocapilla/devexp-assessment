import unittest
from unittest.mock import patch, Mock
from src.client import SinchClient
from src.models import Contact, Message
from src.exceptions import BadRequestError, NotFoundError

class TestSinchClient(unittest.TestCase):
    def setUp(self):
        self.client = SinchClient()
        self.contact_data = {
            "id": "123",
            "name": "John Doe",
            "phone": "+1234567890"
        }
        self.message_data = {
            "id": "msg1",
            "from": "+1111111111",
            "to": self.contact_data,
            "content": "Hello",
            "status": "queued"
        }

    @patch('requests.Session.post')
    def test_create_contact(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.content = True
        mock_response.json.return_value = self.contact_data
        mock_post.return_value = mock_response

        contact = self.client.create_contact(
            name=self.contact_data["name"],
            phone=self.contact_data["phone"]
        )
        self.assertEqual(contact.id, "123")

    @patch('requests.Session.get')
    def test_list_contacts(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = True
        mock_response.json.return_value = {
            "contactsList": [self.contact_data],
            "pageNumber": 0,
            "pageSize": 10
        }
        mock_get.return_value = mock_response

        contacts = self.client.list_contacts()
        self.assertEqual(len(contacts), 1)