from typing import List, Dict, Union
import requests
from .models import Contact, Message
from .exceptions import BadRequestError, UnauthorizedError, NotFoundError

class SinchClient:
    def __init__(self, api_key: str = "there-is-no-key", base_url: str = "http://localhost:3000"):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers["Authorization"] = f"Bearer {api_key}"

    def _make_request(self, method: str, url: str, **kwargs):
        response = self.session.request(method, url, **kwargs)
        response_json = response.json() if response.content else {}
        
        if response.status_code == 400:
            raise BadRequestError(response_json.get("error", "Bad request"))
        if response.status_code == 401:
            raise UnauthorizedError(response_json.get("message", "Unauthorized"))
        if response.status_code == 404:
            raise NotFoundError(response_json.get("message", "Not found"))
        
        response.raise_for_status()
        return response_json

    def create_contact(self, name: str, phone: str) -> Contact:
        data = self._make_request(
            "POST",
            f"{self.base_url}/contacts",
            json={"name": name, "phone": phone}
        )
        return Contact(**data)

    def get_contact(self, contact_id: str) -> Contact:
        data = self._make_request("GET", f"{self.base_url}/contacts/{contact_id}")
        return Contact(**data)

    def list_contacts(self, page_index: int = 0, max: int = 10) -> List[Contact]:
        data = self._make_request(
            "GET",
            f"{self.base_url}/contacts",
            params={"pageIndex": page_index, "max": max}
        )
        contacts = data.get("contactsList", [])
        return [Contact(**contact) for contact in contacts]

    def send_message(self, from_: str, to: Union[str, Dict[str, str]], content: str) -> Message:
        if isinstance(to, str):
            to_data = {"id": to}
        else:
            to_data = {"name": to["name"], "phone": to["phone"]}
        
        data = self._make_request(
            "POST",
            f"{self.base_url}/messages",
            json={
                "from": from_,
                "to": to_data,
                "content": content
            }
        )
        
        if isinstance(data["to"], dict):
            data["to"] = Contact(**data["to"])
        
        if "from" in data:
            data["from_"] = data.pop("from")
        
        return Message(**data)