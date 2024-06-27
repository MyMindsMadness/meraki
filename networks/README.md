# Webhooks 

The webhooks offer 3 different funtions

- networks_get.py will retrieve all organisation network names, IDs, Products and TimeZone and print to a nice table
- networks_create.py will create a new network within an organisation
- networks_delete.py will delete a selected network from the organisation

## Requirements

To use this tool the venv/.env file will need to have the following information...

- Organisation ID
- Meraki API key

To achive this issue the following commands.

    echo ORGANISATION_ID="your_org_id" >> venv/.env
    echo MERAKI_API_KEY="your_api_key" >> venv/.env

