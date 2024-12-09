import requests
from typing import Dict, Any, Optional, List
from .models import Contact, Message
from .exceptions import SinchError, AuthenticationError, NotFoundError, ValidationError

class SinchClient:
   """
   Client for interacting with the Sinch API.
   """
   
   def __init__(
       self,
       api_key: str,
       base_url: str = "http://localhost:3000"
   ):
       """Initialize Sinch client with API key and optional base URL."""
       self.base_url = base_url.rstrip("/")
       self.session = requests.Session()
       self.session.headers.update({
           "Authorization": f"Bearer {api_key}",
           "Content-Type": "application/json",
       })

   def _request(self, method: str, endpoint: str, data: Optional[Dict[str, Any]] = None, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
       """Make HTTP request to API with error handling."""
       url = f"{self.base_url}/{endpoint.lstrip('/')}"
       
       try:
           response = self.session.request(method=method, url=url, json=data, params=params)
           
           if response.status_code == 401:
               raise AuthenticationError("Invalid API key")
           elif response.status_code == 404:
               raise NotFoundError(f"Resource not found: {endpoint}")
           elif response.status_code == 400:
               raise ValidationError(response.json().get("error", "Validation failed"))
           
           response.raise_for_status()
           
           if response.status_code == 204:
               return {}
           
           return response.json()
           
       except requests.exceptions.RequestException as e:
           raise SinchError(f"Request failed: {str(e)}")

   def create_contact(self, name: str, phone: str) -> Contact:
       """Create a contact with name and phone number."""
       data = {"name": name, "phone": phone}
       response = self._request("POST", "/contacts", data=data)
       return Contact(**response)
   
   def get_contact(self, contact_id: str) -> Contact:
       """Get a contact by ID."""
       response = self._request("GET", f"/contacts/{contact_id}")
       return Contact(**response)
   
   def list_contacts(self, page_index: Optional[int] = None, max_items: Optional[int] = None) -> Dict[str, Any]:
       """List contacts with optional pagination."""
       params = {}
       if page_index is not None:
           params["pageIndex"] = page_index
       if max_items is not None:
           params["max"] = max_items
       return self._request("GET", "/contacts", params=params)
   
   def update_contact(self, contact_id: str, **kwargs) -> Contact:
       """Update a contact by ID with provided fields."""
       response = self._request("PATCH", f"/contacts/{contact_id}", data=kwargs)
       return Contact(**response)
   
   def delete_contact(self, contact_id: str) -> None:
       """Delete a contact by ID."""
       self._request("DELETE", f"/contacts/{contact_id}")

   def send_message(self, from_: str, to: Dict[str, Any], content: str) -> Message:
       """Send a message from one contact to another."""
       data = {
           "from": from_,
           "to": to,
           "content": content
       }
       response = self._request("POST", "/messages", data=data)
       return Message(**response)
   
   def get_message(self, message_id: str) -> Message:
       """Get a message by ID."""
       response = self._request("GET", f"/messages/{message_id}")
       return Message(**response)
   
   def list_messages(self, page: Optional[int] = None, limit: Optional[int] = None) -> Dict[str, Any]:
       """List messages with optional pagination."""
       params = {}
       if page is not None:
           params["page"] = page
       if limit is not None:
           params["limit"] = limit
       return self._request("GET", "/messages", params=params)