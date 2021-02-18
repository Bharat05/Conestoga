import os
import dialogflow_v2 as dialogflow
from google.api_core.exceptions import InvalidArgument

# defining parameters
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/Kala/Downloads/faq-chatbot_private_key.json"
DIALOGFLOW_PROJECT_ID = 'faq-chatbot-hvho'
DIALOGFLOW_LANGUAGE_CODE = 'en'
SESSION_ID = '1'


def dialog(our_query):
        # dialog('query') --> 'ChatBotResponse'

    # session variables
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)

    # Our query
    our_input = dialogflow.types.TextInput(
        text=our_query, language_code=DIALOGFLOW_LANGUAGE_CODE)
    query = dialogflow.types.QueryInput(text=our_input)

    # try response of raise exceptions
    try:
        response = session_client.detect_intent(
            session=session, query_input=query)
    except InvalidArgument:
        raise

    return response.query_result.fulfillment_text


our_query = 'scion owner'
print(our_query)
botresponse = dialog(our_query)
print(botresponse)
