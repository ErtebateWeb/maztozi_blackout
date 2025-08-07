# maztozi_blackout

A Python tool to check, parse, and save scheduled and unscheduled power outage information for Mazandaran province, Iran, from the official website (https://khamooshi.maztozi.ir/).

## Features
- Fetches power outage data for a specified city and area.
- Parses and extracts outage details (date, start/end time, region, description).
- Searches for specific outages by keywords.
- Saves outage data to CSV files.
- Optionally saves the raw HTML response for further analysis.
- Logging for all steps and errors.
- **NEW: Telegram Bot** - Provides blackout information to users via Telegram

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

## New Feature: Interactive Search
You can now run the script and choose to enter a custom city code, area code, and search term interactively. The script will fetch and display only the related blackout data.

When you run:

```bash
python main.py
```

You will be prompted:
- To choose between default or custom search mode
- To enter city code, area code, and an optional search term (if you choose custom)

Example:
```
Choose mode: (1) Default check, (2) Custom search [1/2]: 2
Enter city code (default: 990090345): 990090345
Enter area code (default: 61): 61
Enter search term (optional): شهاب نیا
```

The script will then display and save only the outages matching your search.

## Telegram Bot Setup

### Quick Start
1. Run the setup script:
```bash
python setup_bot.py
```

2. Follow the prompts to configure your bot token

3. Run the bot:
```bash
python telegram_bot.py
```

### Manual Setup
1. Create a Telegram bot via @BotFather
2. Get your bot token
3. Set environment variable:
```bash
export TELEGRAM_BOT_TOKEN="your_bot_token_here"
```
4. Install dependencies:
```bash
pip install -r requierements.txt
```
5. Run the bot:
```bash
python telegram_bot.py
```

### Bot Features
- **Interactive Search**: Users can search for outages by area or keywords
- **Quick Commands**: `/start`, `/help`, `/search`, `/areas`, `/latest`
- **Smart Filtering**: Automatically detects areas and filters results
- **Multi-area Support**: Supports Sari, Amol, Babol, Qaem Shahr, Nowshahr
- **Persian Language**: Full Persian interface and support

### Bot Commands
- `/start` - Welcome message and main menu
- `/help` - Complete help guide
- `/search [area] [keyword]` - Search for outages
- `/areas` - List available areas
- `/latest` - Show latest outages

### Example Usage
```
User: /search ساری شهاب نیا
Bot: 🔍 در حال جستجو برای: ساری شهاب نیا
     [Results with outage details]

User: ساری
Bot: 🔍 در حال جستجو برای: ساری
     [All outages in Sari area]
```

## License
MIT License