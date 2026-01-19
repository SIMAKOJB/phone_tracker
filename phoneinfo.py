#!/usr/bin/env python3

import argparse
import os
import sys
import webbrowser
from datetime import datetime

import folium
import phonenumbers
from phonenumbers import carrier, geocoder
from opencage.geocoder import OpenCageGeocode


class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    MAGENTA = '\033[95m'
    END = '\033[0m'
    BOLD = '\033[1m'


def print_banner():
    banner = f"""
{Colors.CYAN}{Colors.BOLD}
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║              📱  PHONE NUMBER TRACKER  📱                 ║
    ║                                                           ║
    ║           Geolocation & Carrier Intelligence              ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
{Colors.END}
    """
    print(banner)


def colored(text, color, bold=False):
    prefix = color
    if bold:
        prefix += Colors.BOLD
    return f"{prefix}{text}{Colors.END}"


def get_phone_info(phone_str, api_key):
    try:
        parsed = phonenumbers.parse(phone_str)
    except phonenumbers.NumberParseException as e:
        print(colored(f"\n[✗] Error parsing number: {e}\n", Colors.RED, bold=True))
        sys.exit(1)

    if not phonenumbers.is_valid_number(parsed):
        print(colored("\n[✗] Invalid or unsupported phone number format\n", Colors.RED, bold=True))
        sys.exit(1)

    print(colored("\n[✓] Valid number detected", Colors.GREEN))
    print(colored("[+] Gathering information...\n", Colors.YELLOW))

    location = geocoder.description_for_number(parsed, "en") or "Unknown location"
    carrier_name = carrier.name_for_number(parsed, "en") or "Unknown carrier"
    country_code = f"+{parsed.country_code}"
    national_number = parsed.national_number
    
    number_type = phonenumbers.number_type(parsed)
    type_map = {
        0: "Fixed Line",
        1: "Mobile",
        2: "Fixed Line or Mobile",
        3: "Toll Free",
        4: "Premium Rate",
        5: "Shared Cost",
        6: "VoIP",
        7: "Personal Number",
        8: "Pager",
        9: "UAN",
        10: "Voicemail",
        99: "Unknown"
    }
    phone_type = type_map.get(number_type, "Unknown")

    lat, lng = None, None
    try:
        geoclient = OpenCageGeocode(api_key)
        results = geoclient.geocode(location)
        if results and len(results) > 0:
            lat = results[0]['geometry']['lat']
            lng = results[0]['geometry']['lng']
            print(colored("[✓] Geocoding successful", Colors.GREEN))
        else:
            print(colored("[!] Could not geocode the location description", Colors.YELLOW))
    except Exception as e:
        print(colored(f"[!] Geocoding failed: {e}", Colors.YELLOW))

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print("\n" + colored("═" * 70, Colors.CYAN))
    print(colored("                    PHONE NUMBER INFORMATION", Colors.CYAN, bold=True))
    print(colored("═" * 70, Colors.CYAN))
    print(f"  {colored('Phone Number:', Colors.BLUE, bold=True)}  {colored(phone_str, Colors.GREEN)}")
    print(f"  {colored('Country Code:', Colors.BLUE, bold=True)}  {colored(country_code, Colors.GREEN)}")
    print(f"  {colored('National Number:', Colors.BLUE, bold=True)} {colored(str(national_number), Colors.GREEN)}")
    print(f"  {colored('Number Type:', Colors.BLUE, bold=True)}   {colored(phone_type, Colors.GREEN)}")
    print(f"  {colored('Location:', Colors.BLUE, bold=True)}      {colored(location, Colors.GREEN)}")
    print(f"  {colored('Carrier:', Colors.BLUE, bold=True)}       {colored(carrier_name, Colors.GREEN)}")
    
    if lat is not None and lng is not None:
        print(f"  {colored('Coordinates:', Colors.BLUE, bold=True)}   {colored(f'{lat:.6f}, {lng:.6f}', Colors.MAGENTA)}")
    
    print(f"  {colored('Timestamp:', Colors.BLUE, bold=True)}     {colored(now, Colors.YELLOW)}")
    print(colored("═" * 70, Colors.CYAN) + "\n")

    result = {
        "number": phone_str,
        "location": location,
        "carrier": carrier_name,
        "type": phone_type,
        "timestamp": now
    }

    if lat is not None and lng is not None:
        result["latitude"] = lat
        result["longitude"] = lng

        map_file = f"phone_map_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"

        m = folium.Map(location=[lat, lng], zoom_start=11, tiles="CartoDB dark_matter")
        
        folium.Marker(
            [lat, lng],
            popup=folium.Popup(
                f"<div style='font-family: monospace;'>"
                f"<b style='color: #00ff00;'>Phone Number:</b> {phone_str}<br>"
                f"<b style='color: #00ff00;'>Location:</b> {location}<br>"
                f"<b style='color: #00ff00;'>Carrier:</b> {carrier_name}<br>"
                f"<b style='color: #00ff00;'>Type:</b> {phone_type}<br>"
                f"<b style='color: #00ff00;'>Coordinates:</b> {lat:.6f}, {lng:.6f}<br>"
                f"<b style='color: #00ff00;'>Timestamp:</b> {now}"
                f"</div>",
                max_width=400
            ),
            tooltip=f"{location} - {carrier_name}",
            icon=folium.Icon(color="red", icon="phone", prefix="fa")
        ).add_to(m)

        folium.CircleMarker(
            [lat, lng],
            radius=15,
            color="#FF0000",
            fill=True,
            fill_color="#FF0000",
            fill_opacity=0.3,
            weight=2
        ).add_to(m)

        m.save(map_file)
        result["map_file"] = map_file
        print(colored(f"[✓] Map generated → {map_file}", Colors.GREEN, bold=True))

    return result


def main():
    parser = argparse.ArgumentParser(
        description="Phone Number Tracker - Geolocation & Carrier Intelligence",
        epilog="Note: Location shows carrier registration area, not real-time GPS tracking."
    )
    parser.add_argument("number", nargs="?", help="Phone number with country code (e.g., +254712345678)")
    parser.add_argument("-k", "--api-key", help="OpenCage Geocoding API key (or set OPENCAGE_API_KEY env var)")
    parser.add_argument("-o", "--open", action="store_true", help="Open generated map in browser automatically")
    parser.add_argument("-q", "--quiet", action="store_true", help="Suppress banner")

    args = parser.parse_args()

    if not args.quiet:
        print_banner()

    if not args.number:
        print(colored("[!] No phone number provided\n", Colors.RED, bold=True))
        print(f"{colored('Usage:', Colors.CYAN, bold=True)} phonetrack.py +254712345678 -k YOUR_API_KEY")
        print(f"{colored('Example:', Colors.CYAN, bold=True)} phonetrack.py +1234567890 --open\n")
        sys.exit(1)

    api_key = args.api_key or os.getenv("OPENCAGE_API_KEY")
    if not api_key:
        print(colored("\n[✗] OpenCage API key required", Colors.RED, bold=True))
        print(colored("    Get your free API key at: https://opencagedata.com/api", Colors.YELLOW))
        print(colored("    Usage: --api-key YOUR_KEY or export OPENCAGE_API_KEY=YOUR_KEY\n", Colors.YELLOW))
        sys.exit(1)

    if not args.number.startswith("+"):
        args.number = "+" + args.number

    result = get_phone_info(args.number, api_key)

    if "map_file" in result and args.open:
        full_path = os.path.abspath(result["map_file"])
        webbrowser.open(f"file://{full_path}")
        print(colored(f"[✓] Opening map in browser...\n", Colors.GREEN))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(colored("\n\n[!] Operation cancelled by user\n", Colors.YELLOW))
        sys.exit(0)
    except Exception as e:
        print(colored(f"\n[✗] Unexpected error: {e}\n", Colors.RED, bold=True))
        sys.exit(1)
