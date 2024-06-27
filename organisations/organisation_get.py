import meraki  # Import the Meraki SDK
import os # Import os library
from dotenv import load_dotenv # import python-dotenv library
from tabulate import tabulate # import tabulate library


# Load environment variables from the .env file
load_dotenv('venv/.env')
API_KEY = os.getenv('MERAKI_API_KEY')  # Get the Meraki API key from environment variable


def meraki_session():
    # Create a Meraki dashboard API instance
    dashboard = meraki.DashboardAPI(api_key=API_KEY, suppress_logging=True)
    return dashboard

def list_organisations():
    dashboard = meraki_session()
    try:
        organisations=dashboard.organizations.getOrganizations()
        dictofOrgs = {}
        for org in organisations:
            #orgname = org['name']
            #orgid = org['id']
            dictofOrgs[org['name']] = {"name":org['name'], "id":org['id']}
        organisation_table_print(dictofOrgs)
        #return dictofOrgs #, organisations
    except meraki.APIError as error:
        print (error.status)
        print (error.reason)
        print (error.message)

def organisation_table_print(data):
    # Create a list of lists containing network details
    table_data = [[key, value['id']] for key, value in data.items()]
    
    # Print the network details in a tabular format
    print(tabulate(table_data, headers=["Name", "ID"], tablefmt="grid"))

list_organisations()