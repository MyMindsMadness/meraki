# Organisations 

The Organisations Tool offers 4 different funtions

- organisation_get.py will retrieve all organisation organisation names, and IDs
- organisation_create.py will create a new organisation
- organisation_delete.py will delete a selected organisation
- organisation_select.py will promt for selection of network and place/replace the ORGANISATION_ID within the .env file

## Requirements

To use this tool the venv/.env file will need to have the following information...

- Meraki API key

To achive this issue the following commands.

    echo MERAKI_API_KEY="your_api_key" >> venv/.env