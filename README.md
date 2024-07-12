# Meraki SDK Toolkit

A simple tool kit, including a PyVis topology builder. 
This toolset using the Meraki python allowing Creation, deletion and information gathering about your meraki networks.
Aimed at Service providers to quickly onboard new organisations and networks.  

## General Instructions

To use this tool kit the following steps are required. 

- Clone the "Meraki" repository
- Create a Virtual Environment
- Create a .env file for Secrets, Each tool may require these file to be updated
- Install requirements.txt file

To achive this. complete the following commands

    git clone https://github.com/MyMindsMadness/meraki.git
    cd meraki
    python3 -m venv venv
    touch venv/.env
    echo MERAKI_API_KEY="your_api_key" >> venv/.env 
    source venv/bin/active
    pip install -r requirements.txt

Each tool will have an individual README.md file that details any additional information required. 

