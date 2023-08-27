from yowsup.layers import YowLayerEvent
from yowsup.layers.protocol_messages import TextMessageProtocolEntity
from yowsup.stacks import YowStack, YowStackBuilder
from yowsup.layers.auth import YowAuthenticationProtocolLayer
from yowsup.layers.coder import YowCoderLayer
from yowsup.layers.network import YowNetworkLayer
from yowsup.common import YowConstants
import json

# Read Yowsup configuration from file
with open('config.json', 'r') as config_file:
    yowsup_config = json.load(config_file)

# Create Yowsup stack
stack_builder = YowStackBuilder()
stack = stack_builder\
    .pushDefaultLayers()\
    .push(YowAuthenticationProtocolLayer, yowsup_config)\
    .push(YowCoderLayer)\
    .push(YowNetworkLayer)\
    .build()

# Start the Yowsup stack
stack.start()

# Send a WhatsApp message
def send_whatsapp_message(recipient, message):
    message_entity = TextMessageProtocolEntity(message, to=recipient)
    stack.broadcastEvent(YowLayerEvent(message_entity, YowConstants.EVENT_STATE_CONNECT))

# Replace with actual recipient number and message content
recipient_number = '916204556171'
message_content = 'Hello from Yowsup!'

send_whatsapp_message(recipient_number, message_content)

# Keep the script running
try:
    while True:
        pass
except KeyboardInterrupt:
    stack.stop()
