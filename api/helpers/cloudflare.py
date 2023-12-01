import logging

import requests
from django.conf import settings

from api.helpers.exceptions import AnsibleError

logger = logging.getLogger('ansible')


def delete_cloudflare_dns(hostname):
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + settings.CLOUDFLARE_GENERAL_TOKEN
    }

    url = f"https://api.cloudflare.com/client/v4/zones/{settings.ZONEID}/dns_records"

    # Get the DNS records for the specified hostname
    response = requests.get(url, headers=headers)
    data = response.json()

    if response.status_code == 200 and data["success"]:
        dns_records = data["result"]

        for record in dns_records:
            record_name = record["name"]
            
            # Check if the record's name matches the hostname provided
            if record_name == hostname:
                record_id = record["id"]

                # Delete the DNS record
                logger.info(f'deleting dns record with id {record_id}')
                delete_url = f"https://api.cloudflare.com/client/v4/zones/{settings.ZONEID}/dns_records/{record_id}"
                delete_response = requests.delete(delete_url, headers=headers)

                if delete_response.status_code != 200:
                    logger.error(f'Error deleting dns record {delete_response.text}')
                    raise AnsibleError(f'Failed to delete DNS record for {hostname}')
                break
    else:
        raise AnsibleError(f'Failed to fetch DNS records for {hostname}')


