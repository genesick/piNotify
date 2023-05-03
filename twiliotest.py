from twilio.rest import Client
from dotenv import load_dotenv
import os


class piNotifier:
    def __init__(self, message: list):
        self.received_message = str(message)
        self.load_variables()
        
    
    def load_variables(self):
        try:
            load_dotenv(dotenv_path=".env.local")
        except Exception as e:
            print("Failed to load .env.local file. The error message was: {e}", e)
            return
            
        self.twilio_account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
        self.twilio_auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
        
        self.twilio_number = os.environ.get("TWILIO_AUTH_TOKEN")
        self.twilio_pn = os.environ.get("TWILIO_PN")
        
        self.send_message(str(self.twilio_account_sid), str(self.twilio_auth_token))
        
        
    def send_message(self, twilio_account_sid:str, twilio_auth_token: str):
        client = Client(self.twilio_account_sid, self.twilio_auth_token)
        message = client.messages \
            .create(
            body= self.received_message,
            from_=str(self.twilio_number),
            to=str(self.twilio_pn)
            )


