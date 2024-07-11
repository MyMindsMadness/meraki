import meraki  # Import the Meraki SDK
import os # Import os library
from dotenv import load_dotenv, set_key # import python-dotenv library
from tabulate import tabulate # import tabulate library
import inquirer

# Load environment variables from the .env file
load_dotenv('venv/.env')
API_KEY = os.getenv('MERAKI_API_KEY')  # Get the Meraki API key from environment variable
ORGANISATION_ID = os.getenv('ORGANISATION_ID') # Get the Organisation ID from environment variable

def meraki_session():
    # Create a Meraki dashboard API instance
    dashboard = meraki.DashboardAPI(api_key=API_KEY, suppress_logging=True)
    return dashboard

def organisation_networks(dashboard):
    try:
        response = dashboard.organizations.getOrganizationNetworks(ORGANISATION_ID, total_pages='all')
        dictofnetworks = {}
        for network in response:
            #network_name = network["name"]
            dictofnetworks[network["name"]] = {"name":network["name"], 
                                            "id":network["id"],
                                            "products":network["productTypes"],
                                            "timezone":network["timeZone"],
                                            "tags":network["tags"],
                                            "url":network["url"]
                                            }
        network_table_print(dictofnetworks)
        return dictofnetworks
    except meraki.APIError as error:
        print (error.status)
        print (error.reason)
        print (error.message)

def network_inquiry(dict_of_networks):
    # Create a list of organistation names
    network_name_list = []

    # Create a list prompt for the user to select a network
    for net in dict_of_networks:
        network_name_list.append(net)
    questions = [
    inquirer.List('choice', 
                  message="Select an option:", 
                  choices=network_name_list),
    ]

    # Prompt the user and get the selected network
    answers = inquirer.prompt(questions)
    selected_option = answers['choice']

    # If the selected option is in the dictionary, return the network ID
    if selected_option in dict_of_networks:
        select = dict_of_networks[selected_option]
        return select["id"]

def network_table_print(dict):
    for key, value in dict.items():
        value['url'] = value['url'][:30]
        #value["id"] = value['id'][:25]
    table_data = [[key, value['id'], ', '.join(value['products']), 
                   value['timezone']] for key, value in dict.items()]
    print(tabulate(table_data, headers=["Name", "ID", "Products", "Timezone"], tablefmt="grid"))

def overwrite_net_string_in_env(net_id):
    set_key("venv/.env", "NETWORK_ID", net_id)

dashboard = meraki_session()
net_dict = organisation_networks(dashboard)
net_id_to_select = network_inquiry(net_dict)
overwrite_net_string_in_env(net_id_to_select)
