import meraki  # Import the Meraki SDK
import os # Import os library
from dotenv import load_dotenv # import python-dotenv library
from tabulate import tabulate # import tabulate library

# Load environment variables from the .env file
load_dotenv('venv/.env')
API_KEY = os.getenv('MERAKI_API_KEY')  # Get the Meraki API key from environment variable

names = []

def meraki_session():
    # Create a Meraki dashboard API instance
    dashboard = meraki.DashboardAPI(api_key=API_KEY, suppress_logging=True)
    return dashboard

def required_user_input():
    name = input("Name for Organisation: ")  # Name of the organisation
    return name

def create_organisation(name):
    dashboard = meraki_session()
    dictoforgs = list_organisations()
    if name not in dictoforgs:
        try:
            dashboard.organizations.createOrganization(name)
            print (f"The Organisation, {name} was Successfully created")
        except meraki.APIError as error:
            print (error.status)
            print (error.reason)
            print (error.message)
    elif name in dictoforgs:
        print ("This organisation already exists, A new network will not be added")

def list_organisations():
    dashboard = meraki_session()
    try:
        organisations=dashboard.organizations.getOrganizations()
        dictofOrgs = {}
        for org in organisations:
            dictofOrgs[org['name']] = {"name":org['name'], "id":org['id']}
        return dictofOrgs
    except meraki.APIError as error:
        print (error.status)
        print (error.reason)
        print (error.message)

org_to_be_created = required_user_input()
create_organisation(org_to_be_created)