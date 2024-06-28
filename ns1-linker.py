import os
import requests
import json
import time
import sys

# Try to import from config_local first, fall back to config if not found
try:
    import config_local as config
except ImportError:
    import config

HEADERS = {
    "X-NSONE-Key": config.API_KEY,
    "Content-Type": "application/json"
}

def log_action(action):
    with open(config.LOG_FILE, "a") as log_file:
        log_file.write(action + "\n")

def get_zone_records(zone_name):
    url = f"https://api.nsone.net/v1/zones/{zone_name}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 404:
        print(f"Zone {zone_name} not found.")
        log_action(f"Zone {zone_name} not found.")
        return None
    else:
        print(f"Failed to fetch records for zone {zone_name}: {response.text}")
        log_action(f"Failed to fetch records for zone {zone_name}: {response.text}")
        return None

def delete_zone(zone_name):
    url = f"https://api.nsone.net/v1/zones/{zone_name}"
    response = requests.delete(url, headers=HEADERS)
    if response.status_code == 200:
        print(f"Zone {zone_name} deleted successfully.")
        log_action(f"Zone {zone_name} deleted successfully.")
    else:
        print(f"Failed to delete zone {zone_name}: {response.text}")
        log_action(f"Failed to delete zone {zone_name}: {response.text}")

def create_linked_zone(new_zone, primary_zone):
    url = f"https://api.nsone.net/v1/zones/{new_zone}"
    payload = {
        "zone": new_zone,
        "link": primary_zone
    }
    response = requests.put(url, headers=HEADERS, json=payload)
    if response.status_code == 200:
        print(f"Linked zone {new_zone} created successfully.")
        log_action(f"Linked zone {new_zone} created successfully.")
    else:
        print(f"Failed to create linked zone {new_zone}: {response.text}")
        log_action(f"Failed to create linked zone {new_zone}: {response.text}")

def get_all_zones():
    url = "https://api.nsone.net/v1/zones"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch zones: {response.text}")
        log_action(f"Failed to fetch zones: {response.text}")
        return []

def format_records(records):
    formatted = []
    for record in records:
        formatted.append(f"{record['type']} {record['domain']} {record['ttl']} {', '.join(record['short_answers'])}")
    return "\n".join(formatted)

def process_zones(file_path, primary_zone_name):
    if not os.path.exists(file_path):
        print(f"Error: The file '{file_path}' does not exist.")
        log_action(f"Error: The file '{file_path}' does not exist.")
        return

    primary_zone = get_zone_records(primary_zone_name)
    if not primary_zone:
        print(f"Primary zone {primary_zone_name} does not exist. Exiting script.")
        log_action(f"Primary zone {primary_zone_name} does not exist. Exiting script.")
        return

    with open(file_path, "r") as file:
        zones = file.readlines()

    all_zones = get_all_zones()
    all_zone_names = [z["zone"] for z in all_zones]

    for zone in zones:
        zone = zone.strip()
        if not zone:
            continue

        print(f"Processing zone: {zone}")
        log_action(f"Processing zone: {zone}")

        records = get_zone_records(zone)
        if records:
            if "link" in records and records["link"] == primary_zone_name:
                print(f"Zone {zone} is already linked to {primary_zone_name}. No action required.")
                log_action(f"Zone {zone} is already linked to {primary_zone_name}. No action required.")
                continue
            
            print(f"Records for zone {zone}:")
            print(format_records(records.get("records", [])))
            log_action(f"Records for zone {zone}:\n{format_records(records.get('records', []))}")

            question = f"Do you want to delete zone {zone} and create it as a linked zone? (Y/n): "
            confirm = input(question).strip().lower()
            log_action(f"User prompt: {question}")
            log_action(f"User response: {confirm}")

            if confirm == 'y':
                delete_zone(zone)
                create_linked_zone(zone, primary_zone_name)
            else:
                print(f"Skipped deletion of zone {zone}.")
                log_action(f"Skipped deletion of zone {zone}.")
        else:
            print(f"No records found or error fetching records for zone {zone}.")
            log_action(f"No records found or error fetching records for zone {zone}.")
            
            question = f"Do you want to link zone {zone} to {primary_zone_name}? (Y/n): "
            confirm = input(question).strip().lower()
            log_action(f"User prompt: {question}")
            log_action(f"User response: {confirm}")

            if confirm == 'y':
                create_linked_zone(zone, primary_zone_name)
            else:
                print(f"Skipped linking of zone {zone}.")
                log_action(f"Skipped linking of zone {zone}.")
        
        time.sleep(1)  # To avoid rate limiting

# Main execution
if len(sys.argv) > 1:
    primary_zone_name = sys.argv[1]
else:
    primary_zone_name = input("Enter the primary zone name: ").strip()

if len(sys.argv) > 2:
    file_path = sys.argv[2]
else:
    file_path = input("Enter the path to the file containing the list of zones: ").strip()

process_zones(file_path, primary_zone_name)
