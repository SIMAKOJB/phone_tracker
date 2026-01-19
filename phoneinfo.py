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
    END = '\033[0m'
    BOLD = '\033[1m'


def colored(text, color, bold=False, no_color=False):
    if no_color:
        return text
    prefix = color
    if bold:
        prefix += Colors.BOLD
    return f"{prefix}{text}{Colors.END}"


def get_phone_info(phone_str, api_key, no_color=False):
    c = lambda t, col, b=False: t if no_color else get_colored(t, col, b)

    try:
        parsed = phonenumbers.parse(phone_str)
    except phonenumbers.NumberParseException as e:
        print(c(f"Error parsing number: {e}", Colors.RED))
        sys.exit(1)

    if not phonenumbers.is_valid_number(parsed):
        print(c("Invalid or unsupported phone number format", Colors.RED))
        sys.exit(1)

    location = geocoder.description_for_number(parsed, "en") or "Unknown location"
    carrier_name = carrier.name_for_number(parsed, "en") or "Unknown carrier"

    try:
        geoclient = OpenCageGeocode(api_key)
        results = geoclient.geocode(location)
        if not results:
            print(c("Could not geocode the location description", Colors.YELLOW))
            lat, lng = None, None
        else:
            lat = results[0]['geometry']['lat']
            lng = results[0]['geometry']['lng']
    except Exception as e:
        print(c(f"Geocoding failed: {e}", Colors.RED))
        lat, lng = None, None

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print("\n" + c("═" * 60, Colors.CYAN))
    print(c("  PHONE NUMBER INFORMATION", Colors.CYAN, bold=True))
    print(c("═" * 60, Colors.CYAN))
    print(f"  Number     : {c(phone_str, Colors.GREEN)}")
    print(f"  Location   : {c(location, Colors.GREEN)}")
    print(f"  Carrier    : {c(carrier_name, Colors.GREEN)}")
    if lat is not None and lng is not None:
        print(f"  Coordinates: {c(f'{lat:.6f}, {lng:.6f}', Colors.GREEN)}")
    print(f"  Timestamp  : {c(now, Colors.YELLOW)}")
    print(c("═" * 60, Colors.CYAN) + "\n")

    result = {
        "number": phone_str,
        "location": location,
        "carrier": carrier_name,
        "timestamp": now
    }

    if lat is not None and lng is not None:
        result["latitude"] = lat
        result["longitude"] = lng

        map_file = f"phone_loc_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"

        m = folium.Map(location=[lat, lng], zoom_start=11, tiles="CartoDB positron")
        folium.Marker(
            [lat, lng],
            popup=folium.Popup(
                f"<b>Number:</b> {phone_str}<br>"
                f"<b>Location:</b> {location}<br>"
                f"<b>Carrier:</b> {carrier_name}<br>"
                f"<b>Coords:</b> {lat:.6f}, {lng:.6f}<br>"
                f"<b>Time:</b> {now}",
                max_width=350
            ),
            tooltip=location,
            icon=folium.Icon(color="red", icon="phone", prefix="fa")
        ).add_to(m)

        folium.CircleMarker(
            [lat, lng],
            radius=12,
            color="#FF4444",
            fill=True,
            fill_opacity=0.2
        ).add_to(m)

        m.save(map_file)
        result["map_file"] = map_file
        print(c(f"Map saved → {map_file}", Colors.GREEN))

    return result


def main():
    parser = argparse.ArgumentParser(
        description="Simple phone number information & approximate geolocation tool",
        epilog="Note: Location is approximate (carrier registration area), not real-time GPS."
    )
    parser.add_argument("number", nargs="?", help="Phone number with country code (e.g. +254712345678)")
    parser.add_argument("--api-key", required=False, help="OpenCage Geocoding API key (or set OPENCAGE_API_KEY env var)")
    parser.add_argument("--open", action="store_true", help="Automatically open generated map in browser")
    parser.add_argument("--no-color", action="store_true", help="Disable colored output")

    args = parser.parse_args()

    if not args.number:
        print("No phone number provided.")
        print("Usage example:  python3 phoneinfo.py +254712345678 --api-key YOUR_KEY")
        sys.exit(1)

    api_key = args.api_key or os.getenv("OPENCAGE_API_KEY")
    if not api_key:
        print("Error: OpenCage API key is required.")
        print("Pass it with --api-key or set environment variable OPENCAGE_API_KEY")
        sys.exit(1)

    if not args.number.startswith("+"):
        args.number = "+" + args.number

    result = get_phone_info(args.number, api_key, args.no_color)

    if "map_file" in result and args.open:
        full_path = os.path.abspath(result["map_file"])
        webbrowser.open(f"file://{full_path}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted. Exiting.")
        sys.exit(0)
    except Exception as e:
        print(f"\nUnexpected error: {e}", file=sys.stderr)
        sys.exit(1)
