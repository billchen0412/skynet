import json
import os

import requests

ZONE_ID = os.getenv("ZONE_ID")
RECORD_ID = os.getenv("RECORD_ID")
API_TOKEN = os.getenv("API_TOKEN")
DNS_NAME = os.getenv("DNS_NAME")


def get_public_ip():
    return requests.get("https://api.ipify.org").text.strip()


def update_dns(ip):
    url = (
        f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records/{RECORD_ID}"
    )
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json",
    }
    data = {"type": "A", "name": DNS_NAME, "content": ip, "ttl": 120, "proxied": False}
    response = requests.put(url, headers=headers, data=json.dumps(data))
    print(
        f"[Cloudflare] Updating {DNS_NAME} to {ip} → {response.status_code}, {response.json()}"
    )


if __name__ == "__main__":
    ip = get_public_ip()
    update_dns(ip)
