import meraki  # Import the Meraki SDK
import os # Import os library
from dotenv import load_dotenv, set_key # import python-dotenv library
from tabulate import tabulate # import tabulate library
import inquirer


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
        return dictofOrgs #, organisations
    except meraki.APIError as error:
        print (error.status)
        print (error.reason)
        print (error.message)

def organisation_inquiry(dict_of_organisations):
    # Create a list of organistation names
    organisation_name_list = []

    # Create a list prompt for the user to select a network
    for org in dict_of_organisations:
        organisation_name_list.append(org)
    questions = [
    inquirer.List('choice', 
                  message="Select an option:", 
                  choices=organisation_name_list),
    ]

    # Prompt the user and get the selected network
    answers = inquirer.prompt(questions)
    selected_option = answers['choice']

    # If the selected option is in the dictionary, return the network ID
    if selected_option in dict_of_organisations:
        select = dict_of_organisations[selected_option]
        return select["id"]

def organisation_table_print(data):
    # Create a list of lists containing network details
    table_data = [[key, value['id']] for key, value in data.items()]
    
    # Print the network details in a tabular format
    print(tabulate(table_data, headers=["Name", "ID"], tablefmt="grid"))

def overwrite_org_string_in_env(org_id):
    set_key("venv/.env", "ORGANISATION_ID", org_id)

org_dict = list_organisations()
org_id_to_select = organisation_inquiry(org_dict)
overwrite_org_string_in_env(org_id_to_select)
