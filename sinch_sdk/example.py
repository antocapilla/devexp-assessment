from sinch_sdk import SinchClient

client = SinchClient(api_key="there-is-no-key")

print("Listing existing conatcts...")
contacts = client.list_contacts()
if contacts.get('contactsList'):
   print(f"Found {len(contacts['contactsList'])} contacts")
   for contact in contacts['contactsList']:
       print(f"- Contact: {contact['name']} ({contact['phone']}) - ID: {contact['id']}")
       print("  Deleting contact...")
       client.delete_contact(contact['id'])
else:
   print("No existing contacts")

print("\nCreating new contact...")
contact = client.create_contact(
   name="John",
   phone="+34666777888"
)
print(f"Contact created with ID: {contact.id}")

print("\nEnviando mensaje...")
message = client.send_message(
   from_="+34666777888",
   to={"id": contact.id},
   content="Hello!"
)
print(f"Message sent with ID: {message.id}")

print("\nVerifying status of message...")
message_details = client.get_message(message.id)
print(f"Status of message: {message_details.status}")