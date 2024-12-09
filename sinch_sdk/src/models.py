from dataclasses import dataclass

@dataclass
class Contact:
    id: str
    name: str
    phone: str

@dataclass 
class Message:
    id: str
    from_: str
    to: Contact
    content: str
    status: str