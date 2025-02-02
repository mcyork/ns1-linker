
---

# NS1 Zone Management Script

This script allows you to manage DNS zones in NS1. It reads a list of zones from a file, fetches and displays their records, prompts for deletion, and recreates the zones as linked zones if confirmed. It also logs all actions and outputs for review.

## Why

You've been managing a ton of "defensive" domains individually. Defensive domains are those that you register to protect your brand or intellectual property, to prevent cybersquatting, or to ensure that similar or related domain names are not used by others in ways that could harm your reputation or cause confusion.

Managing these domains individually can be incredibly time-consuming and error-prone. Each domain may require separate updates, configurations, and monitoring, which can lead to inconsistencies and potential oversights.

By using this script, you can streamline the management process. The script allows you to:

- **Centralize Management**: Link all your defensive domains to a primary zone, making it easier to manage DNS settings from a single point of control.
- **Ensure Consistency**: Automatically apply consistent DNS configurations across all linked domains, reducing the risk of errors.
- **Save Time**: Automate repetitive tasks such as fetching records, prompting for deletions, and creating linked zones, freeing up your time for more strategic activities.
- **Log Actions**: Maintain a log of all actions performed, providing a clear audit trail for compliance and review.

This approach not only improves efficiency but also enhances the security and reliability of your domain management practices.

## Prerequisites

1. Python 3.x
2. `requests` library

Install the `requests` library if you haven't already:

```bash
pip install requests
```

## Configuration

Create a `config.py` file in the same directory as the script with the following content:

```python
API_KEY = "YOUR_API_KEY"
LOG_FILE = "ns1_actions.log"
```

Replace `"YOUR_API_KEY"` with your actual NS1 API key.

## Usage

### Command Line Arguments

You can provide the primary zone name and the path to the file containing the list of zones as command line arguments:

```bash
python ns1-linker.py mcyork.com zones.txt
```

If you don't provide the arguments, the script will prompt you to enter them:

```bash
python ns1-linker.py
```

### Example Zones File

Create a file named `zones.txt` with the list of zones you want to manage. For example:

```
esoup.net
invoices.org
```

### Running the Script

To run the script, use the following command:

```bash
python ns1-linker.py mcyork.com zones.txt
```

Replace `mcyork.com` with your actual primary zone and `zones.txt` with the path to your zones file.

### Example Output

Here's an example of the script output during a test run:

```bash
% python ns1-linker.py park.mcyork.com zones.txt
Processing zone: zip.mcyork.com
Records for zone zip.mcyork.com:
TXT link-me-babe.zip.mcyork.com 3600 totally link me now!
NS zip.mcyork.com 3600 dns1.p04.nsone.net, dns2.p04.nsone.net, dns3.p04.nsone.net, dns4.p04.nsone.net
Do you want to delete zone zip.mcyork.com and create it as a linked zone? (Y/n): y 
Zone zip.mcyork.com deleted successfully.
Linked zone zip.mcyork.com created successfully.
```

## Script Functionality

1. **Fetching Zone Records**: The script retrieves all DNS records for each zone listed in `zones.txt`.
2. **Prompt for Deletion**: For each zone, it displays the records and prompts you to confirm deletion (or skips if already linked).
3. **Deleting Zones**: If confirmed, it deletes the zone.
4. **Creating Linked Zones**: It then recreates the zone as a linked zone to the primary zone.
5. **Logging**: All actions and outputs are logged to a file specified in `config.LOG_FILE`.

### Example Workflow

1. **Initial Setup**:
   - Ensure you have the `config.py` file with your API key.
   - Create a `zones.txt` file with the list of zones you want to manage.

2. **Running the Script**:
   - Run the script from the command line.
   - The script will fetch records for each zone, display them, and prompt for deletion.

3. **Example Prompts**:
   - The script will display records for each zone and ask if you want to delete and recreate it as a linked zone:
     ```
     Records for zone zip.mcyork.com:
     TXT link-me-babe.zip.mcyork.com 3600 totally link me now!
     NS zip.mcyork.com 3600 dns1.p04.nsone.net, dns2.p04.nsone.net, dns3.p04.nsone.net, dns4.p04.nsone.net
     Do you want to delete zone zip.mcyork.com and create it as a linked zone? (Y/n):
     ```

## Notes

- The script pauses for 1 second between API calls to avoid rate limiting.
- If a zone is already linked (to any zone) it will be skipped.
- Ensure you have proper permissions and a valid API key to interact with the NS1 API.

## License

This script is provided as-is without any warranties. Use it at your own risk.

---