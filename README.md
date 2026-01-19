# Phone Number Tracker

A powerful command-line tool for gathering intelligence on phone numbers including geolocation, carrier information, and interactive map visualization.

## Features

- **Phone Number Validation** - Verify if numbers are valid and properly formatted
- **Carrier Detection** - Identify the mobile/telecom carrier
- **Geolocation** - Approximate location based on carrier registration area
- **Number Type Detection** - Identify if number is mobile, landline, VoIP, etc.
- **Interactive Maps** - Generate HTML maps with markers showing approximate location
- **Color-Coded Terminal Output** - Beautiful, easy-to-read information display
- **Export Capabilities** - Save maps for later reference

## Important Notice

This tool provides **approximate location based on carrier registration area**, not real-time GPS tracking. The location represents where the phone number is registered, not the current position of the device.

## Installation

### Prerequisites

- Python 3.6 or higher
- pip package manager
- Internet connection

### Step 1: Clone or Download

```bash
git clone <repository-url>
cd phone-tracker
```

### Step 2: Install Dependencies

**For Parrot OS / Kali Linux / Debian-based systems:**

```bash
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

**Alternative (system-wide with override):**

```bash
pip3 install -r requirements.txt --break-system-packages
```

**Or install individually:**

```bash
pip3 install phonenumbers folium opencage --break-system-packages
```

### Step 3: Get OpenCage API Key

1. Visit [OpenCage Geocoding API](https://opencagedata.com/api)
2. Sign up for a free account
3. Copy your API key
4. Free tier includes 2,500 requests/day

### Step 4: Make Script Executable

```bash
chmod +x phoneinfo.py
```

### Step 5: (Optional) Add to PATH

```bash
sudo cp phoneinfo.py /usr/local/bin/phoneinfo
```

##  Usage

### Important: Activate Virtual Environment

If you installed using venv, activate it first:

```bash
source venv/bin/activate
```

### Basic Usage

```bash
python3 phoneinfo.py +254712345678 -k YOUR_API_KEY
```

### Using Environment Variable

Set your API key as an environment variable:

```bash
export OPENCAGE_API_KEY="your_api_key_here"
python3 phonetrack.py +254712345678
```

Add to `.bashrc` or `.zshrc` for permanent setup:

```bash
echo 'export OPENCAGE_API_KEY="your_api_key_here"' >> ~/.bashrc
source ~/.bashrc
```

### Command-Line Options

```
positional arguments:
  number                Phone number with country code (e.g., +254712345678)

optional arguments:
  -h, --help            Show help message and exit
  -k, --api-key         OpenCage Geocoding API key
  -o, --open            Open generated map in browser automatically
  -q, --quiet           Suppress banner display
```

## Examples

### Example 1: Basic lookup
```bash
python3 phonetrack.py +1234567890 -k YOUR_API_KEY
```

### Example 2: Auto-open map in browser
```bash
python3 phonetrack.py +447911123456 -k YOUR_API_KEY --open
```

### Example 3: Using environment variable
```bash
export OPENCAGE_API_KEY="your_key"
python3 phonetrack.py +254701234567
```

### Example 4: Quiet mode (no banner)
```bash
python3 phonetrack.py +33612345678 -k YOUR_API_KEY -q
```

## Output Information

The tool provides the following information:

- **Phone Number** - Full international format
- **Country Code** - International dialing code
- **National Number** - Number without country code
- **Number Type** - Mobile, Fixed Line, VoIP, etc.
- **Location** - Approximate geographic location
- **Carrier** - Telecommunications provider
- **Coordinates** - Latitude and longitude (if available)
- **Timestamp** - Date and time of lookup

## Map Files

Generated maps are saved as HTML files with the naming convention:
```
phone_map_YYYYMMDD_HHMMSS.html
```

Maps include:
- Interactive markers with full information popup
- Dark theme for better visibility
- Highlighted circle showing approximate area
- Zoom and pan capabilities

## Troubleshooting

### "No module named 'phonenumbers'"
```bash
pip3 install phonenumbers
```

### "No module named 'folium'"
```bash
pip3 install folium
```

### "No module named 'opencage'"
```bash
pip3 install opencage
```

### "OpenCage API key required"
Make sure you have:
1. Obtained an API key from opencagedata.com
2. Either passed it with `-k` flag or set the environment variable

### "Invalid phone number format"
Ensure the number:
- Starts with `+` followed by country code
- Contains only digits after the `+`
- Is a valid phone number format

### Map doesn't open automatically
Use the `--open` or `-o` flag, and ensure you have a default web browser configured.

## Dependencies

```
phonenumbers>=8.13.0
folium>=0.14.0
opencage>=2.2.0
```

## Supported Countries

The tool supports phone numbers from all countries that have assigned international dialing codes. Some examples:

- **United States/Canada**: +1
- **United Kingdom**: +44
- **Kenya**: +254
- **India**: +91
- **Australia**: +61
- **Germany**: +49
- **France**: +33
- **China**: +86

## Legal & Ethical Use

This tool is for **educational and legitimate purposes only**:

**Acceptable uses:**
- Verifying your own phone numbers
- Testing phone number validation systems
- Educational research on telecommunications
- Legitimate investigative purposes with proper authorization

**Unacceptable uses:**
- Stalking or harassment
- Unauthorized surveillance
- Privacy violations
- Any illegal activities

**Always respect privacy laws and regulations in your jurisdiction.**

## Privacy & Security

- No data is stored or logged by this tool
- All lookups are performed in real-time
- API keys should be kept confidential
- Generated maps are stored locally only

## Contributing

Contributions are welcome! Areas for improvement:
- Additional data sources
- Enhanced map visualizations
- Batch processing capabilities
- Export to JSON/CSV formats

## License

This tool is provided as-is for educational purposes. Use responsibly and in accordance with local laws and regulations.

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Verify all dependencies are installed
3. Ensure your API key is valid and has remaining quota
4. Check your internet connection

## Updates

To update dependencies:
```bash
pip3 install --upgrade phonenumbers folium opencage
```

---

**Disclaimer**: This tool provides approximate location data based on carrier registration information, not real-time GPS tracking. Location accuracy varies by country and carrier. Always use this tool ethically and legally.
