from google_auth_oauthlib.flow import InstalledAppFlow
import os

def authenticate_and_generate_token():
    client_secrets_file = 'credentials.json'  # Path to your credentials.json file
    scopes = ['https://www.googleapis.com/auth/gmail.readonly']

    print("Starting authentication...")

    # Initialize the flow for OAuth
    flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
    
    # Run the local server for OAuth authentication
    creds = flow.run_local_server(port=8088, open_browser=True)  # Adjust port if needed
    
    print("Authentication successful!")

    # Check if creds are valid
    if creds:
        print("Credentials generated successfully.")
    else:
        print("No credentials found.")

    # Save the credentials to token.json
    try:
        with open('token.json', 'w') as token_file:
            token_file.write(creds.to_json())
        print("Token saved to 'token.json'")
    except Exception as e:
        print(f"Error saving token: {e}")

    return creds is not None
