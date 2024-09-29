import africastalking

# Initialize Africastalking with your credentials
username = "sandbox"
api_key = "atsk_ec0d97def76be50a44b66a97d990563b1fbee9259163a4d281b44a060eac6168575a8606"
africastalking.initialize(username, api_key)

# Create an instance of the SMS service
sms = africastalking.SMS

def send_sms(message: str, phone_numbers: list):
    try:
        # Send SMS to the provided list of phone numbers
        response = sms.send(message, phone_numbers)
        
        # Log the response for each recipient
        for recipient in response['SMSMessageData']['Recipients']:
            print(f"Sent SMS to {recipient['number']}: {recipient['status']} (Cost: {recipient['cost']})")
        
        return response
    except Exception as e:
        print(f"Error sending SMS: {e}")
        raise
