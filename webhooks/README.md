# Webhooks 

The webhooks offer 3 different funtions

- webhook_get.py will retrieve all webhook names and IDs
- webhook_create.py will create a new webhook across all organisation networks
- webhook_delete.py will delete a selected webhook from all organisation networks

## Requirements

To use this tool the venv/.env file will need to have the following information...

- Organisation ID
- Meraki API key
- Webhook secret (creation only)

To achive this issue the following commands.

    echo ORGANISATION_ID="your_org_id" >> venv/.env
    echo MERAKI_API_KEY="your_api_key" >> venv/.env
    echo WEBHOOK_SHARED_SECRET="your_webhook_secret" >> venv/.env
