import meraki  # Import the Meraki SDK
import os # Import os library
from dotenv import load_dotenv # import python-dotenv library
import inquirer
from prompt_toolkit import prompt
from prompt_toolkit.completion import Completer, Completion


# Load environment variables from the .env file
load_dotenv('venv/.env')
API_KEY = os.getenv('MERAKI_API_KEY')  # Get the Meraki API key from environment variable
ORGANISATION_ID = os.getenv('ORGANISATION_ID') # Get the Organisation ID from environment variable
WEBHOOK_SECRET = os.getenv('WEBHOOK_SHARED_SECRET')  # Get the webhook shared secret from environment variable

class SubstringCompleter(Completer):
    def __init__(self, words):
        self.words = words

    def get_completions(self, document, complete_event):
        word = document.text_before_cursor
        for w in self.words:
            if word.lower() in w.lower():
                yield Completion(w, start_position=-len(word))

def meraki_session():
    # Create a Meraki dashboard API instance
    dashboard = meraki.DashboardAPI(api_key=API_KEY, suppress_logging=True)
    return dashboard

def print_banner(text, symbol="#"):
    banner_length = len(text) + 20
    print("\n")
    print(symbol * banner_length)
    print(symbol, " " * 7, text, " " * 7, symbol)
    print(symbol * banner_length)
    print("\n")

def product_selector():
    products = ["appliance", 
                "switch", 
                "Wireless", 
                "camera",
                "cellularGateway",
                "sensor",
                "systemsManager"]
    question = [
        inquirer.Checkbox(
            "Products", 
            message="What products will the Organisation Support? (Space to Select, Enter to continue):", 
            choices=products
        ),
    ]
    selected_products = inquirer.prompt(question)
    return selected_products["Products"] 

def timezone_selection():
    tz_identifiers = [
        'America/New_York',
        'America/Los_Angeles',
        'America/Chicago',
        'America/Denver',
        'America/Toronto',
        'Europe/London',
        'Europe/Paris',
        'Asia/Tokyo',
        'Asia/Shanghai',
        'Asia/Kolkata',
        'Australia/Sydney',
        'America/Sao_Paulo',
        'Africa/Johannesburg',
        'Europe/Moscow',
        'Pacific/Auckland',
        'America/Mexico_City',
        'Asia/Dubai',
        'Asia/Singapore',
        'Europe/Berlin',
        'Africa/Cairo'
    ]

    completer = SubstringCompleter(tz_identifiers)
    user_input = prompt("Please start typing and Select Location/City: ", completer=completer)
    return user_input

def create_network(dashboard):
    name = input("What is the name of the Network? ")
    print_banner("Network Product Selection")
    selected_products = product_selector()
    print_banner("Network Time Zone Selection")
    selected_timezone = timezone_selection()
    try:
        dashboard.organizations.createOrganizationNetwork(
        ORGANISATION_ID, name, selected_products,timeZone=selected_timezone)
        print (f"{name} network created")
    except meraki.APIError as error:
        print (error.status)
        print (error.reason)
        print (error.message)

dashboard = meraki_session()
create_network(dashboard)
