# maztozi_blackout

A Python tool to check, parse, and save scheduled and unscheduled power outage information for Mazandaran province, Iran, from the official website (https://khamooshi.maztozi.ir/).

## Features
- Fetches power outage data for a specified city and area.
- Parses and extracts outage details (date, start/end time, region, description).
- Searches for specific outages by keywords.
- Saves outage data to CSV files.
- Optionally saves the raw HTML response for further analysis.
- Logging for all steps and errors.

## Requirements
Install dependencies using pip:

```bash
pip install -r requierements.txt
```

## Usage
Run the script directly:

```bash
python main.py
```

By default, it will:
- Search for outages in the default city and area (city_code='990090345', area_code='61').
- Look for outages containing the keywords '53- شهاب نیا' or '۵۳- شهاب نیا'.
- Save the results to a timestamped CSV file and the raw HTML response to a file.

### Example Output
- `power_outages_YYYYMMDD_HHMMSS.csv`: CSV file with columns: `date`, `start_time`, `end_time`, `region`, `description`.
- `raw_response_YYYYMMDD_HHMMSS.html`: Raw HTML response from the server.

## Customization
You can modify the script to:
- Change the city or area code in `search_outages()`.
- Change the search keywords in the `search_terms` list.
- Use the class methods independently for more advanced workflows.

## Example: Using the Class in Your Code
```python
from main import PowerOutageChecker
checker = PowerOutageChecker()
html = checker.search_outages(city_code='990090345', area_code='61')
outages = checker.parse_outages(html)
checker.save_to_csv(outages, 'my_outages.csv')
```

## License
MIT License