from sinch_sdk import SinchClient, WebhookServer
from sinch_sdk.exceptions import BadRequestError

# Usar el cliente
client = SinchClient()

try:
    # Crear contacto
    contact = client.create_contact("John", "+1234567890")
    
    # Enviar mensaje
    message = client.send_message("+1111111111", contact.id, "Hello!")
    
except BadRequestError as e:
    print(f"Error: {e}")

# Usar el webhook (bonus)
server = WebhookServer(secret="mySecret")
server.run()