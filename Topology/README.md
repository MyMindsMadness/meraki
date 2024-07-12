# Topology 

The Topology Tool offers a single function 

- Build a Topological view of the network!

## Requirements

To use this tool the venv/.env file will need to have the following information...

- Meraki API key
- Organanisation ID
- Network ID

To achive the API key issue the following commands.

    echo MERAKI_API_KEY="your_api_key" >> venv/.env

If you need to select the organisation or network run the followning scrips first. 

    organisations/organisations_select.py
    networks/network_select.py

The above scripts will dynamically add the values you select in to you environment.