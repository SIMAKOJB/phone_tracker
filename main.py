#!/usr/bin/env python3
import phonenumbers
from phonenumbers import geocoder, carrier
from opencage.geocoder import OpenCageGeocode
import folium
from datetime import datetime
import sys
import time
import os

# Color codes for terminal
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def clear_screen():
    """Clear terminal screen"""
    os.system('clear' if os.name != 'nt' else 'cls')

def print_banner():
    """Print animated banner"""
    banner = f"""
{Colors.CYAN}{Colors.BOLD}
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║        📱 PHONE NUMBER LOCATION TRACKER 📍                ║
║                                                           ║
║           Real-Time Geolocation System                    ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
{Colors.END}
    """
    for line in banner.split('\n'):
        print(line)
        time.sleep(0.05)

def animated_print(text, color=Colors.GREEN, delay=0.03):
    """Print text with typing animation"""
    for char in text:
        sys.stdout.write(color + char + Colors.END)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def loading_animation(text="Processing", duration=2):
    """Show loading animation"""
    animation = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        sys.stdout.write(f"\r{Colors.YELLOW}{animation[i % len(animation)]} {text}...{Colors.END}")
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1
    sys.stdout.write("\r" + " " * (len(text) + 10) + "\r")
    sys.stdout.flush()

def progress_bar(current, total, bar_length=40):
    """Display progress bar"""
    progress = current / total
    block = int(bar_length * progress)
    bar = "█" * block + "░" * (bar_length - block)
    percent = progress * 100
    sys.stdout.write(f"\r{Colors.CYAN}[{bar}] {percent:.1f}%{Colors.END}")
    sys.stdout.flush()

def print_box(title, content, color=Colors.GREEN):
    """Print content in a box"""
    width = max(len(title), max(len(line) for line in content)) + 4
    print(f"\n{color}╔{'═' * width}╗")
    print(f"║ {title.center(width - 2)} ║")
    print(f"╠{'═' * width}╣")
    for line in content:
        print(f"║ {line.ljust(width - 2)} ║")
    print(f"╚{'═' * width}╝{Colors.END}\n")

def get_phone_location(phone_number, api_key):
    """
    Track phone number location with animations
    
    Args:
        phone_number (str): Phone number with country code
        api_key (str): OpenCage Geocoder API key
    
    Returns:
        dict: Location information
    """
    try:
        # Step 1: Parsing
        print(f"\n{Colors.YELLOW}[1/4]{Colors.END} Parsing phone number...")
        for i in range(1, 6):
            progress_bar(i, 5)
            time.sleep(0.1)
        print()
        
        parsed_number = phonenumbers.parse(phone_number)
        
        # Validate
        if not phonenumbers.is_valid_number(parsed_number):
            return {"error": "Invalid phone number"}
        
        print(f"{Colors.GREEN}✓ Phone number parsed successfully{Colors.END}")
        time.sleep(0.3)
        
        # Step 2: Getting location
        print(f"\n{Colors.YELLOW}[2/4]{Colors.END} Retrieving location data...")
        loading_animation("Analyzing", 1.5)
        
        location = geocoder.description_for_number(parsed_number, "en")
        if not location:
            location = "Unknown Location"
        
        carrier_name = carrier.name_for_number(parsed_number, "en")
        if not carrier_name:
            carrier_name = "Unknown Carrier"
        
        print(f"{Colors.GREEN}✓ Location data retrieved{Colors.END}")
        time.sleep(0.3)
        
        # Step 3: Geocoding
        print(f"\n{Colors.YELLOW}[3/4]{Colors.END} Geocoding coordinates...")
        loading_animation("Mapping", 1.5)
        
        geocoder_client = OpenCageGeocode(api_key)
        results = geocoder_client.geocode(location)
        
        if not results:
            return {
                "error": "Could not geocode location",
                "location": location,
                "carrier": carrier_name
            }
        
        lat = results[0]['geometry']['lat']
        lng = results[0]['geometry']['lng']
        
        print(f"{Colors.GREEN}✓ Coordinates obtained{Colors.END}")
        time.sleep(0.3)
        
        # Step 4: Creating map
        print(f"\n{Colors.YELLOW}[4/4]{Colors.END} Generating map...")
        for i in range(1, 6):
            progress_bar(i, 5)
            time.sleep(0.2)
        print()
        
        my_map = folium.Map(location=[lat, lng], zoom_start=10)
        
        popup_text = f"""
        <b>📱 Phone Location Tracker</b><br><br>
        <b>Location:</b> {location}<br>
        <b>Carrier:</b> {carrier_name}<br>
        <b>Coordinates:</b> {lat}, {lng}<br>
        <b>Time:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """
        
        folium.Marker(
            [lat, lng],
            popup=folium.Popup(popup_text, max_width=300),
            tooltip=location,
            icon=folium.Icon(color='red', icon='phone', prefix='fa')
        ).add_to(my_map)
        
        folium.Circle(
            [lat, lng],
            radius=5000,
            color='#FF4444',
            fill=True,
            fillOpacity=0.2,
            popup='Approximate Area'
        ).add_to(my_map)
        
        filename = f"location_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        my_map.save(filename)
        
        print(f"{Colors.GREEN}✓ Map generated successfully{Colors.END}\n")
        time.sleep(0.3)
        
        # Display results in a box
        results_content = [
            f"Phone Number : {phone_number}",
            f"Location     : {location}",
            f"Carrier      : {carrier_name}",
            f"Latitude     : {lat}",
            f"Longitude    : {lng}",
            f"Map File     : {filename}",
            f"Timestamp    : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        ]
        
        print_box("🎯 TRACKING RESULTS", results_content, Colors.GREEN)
        
        return {
            "location": location,
            "carrier": carrier_name,
            "latitude": lat,
            "longitude": lng,
            "map_file": filename,
            "timestamp": datetime.now().isoformat()
        }
        
    except phonenumbers.NumberParseException as e:
        return {"error": f"Error parsing number: {str(e)}"}
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}

def show_menu():
    """Display animated menu"""
    menu = f"""
{Colors.CYAN}┌─────────────────────────────────────────┐
│              MAIN MENU                  │
├─────────────────────────────────────────┤
│  1. Track Phone Number                  │
│  2. View Instructions                   │
│  3. About                               │
│  4. Exit                                │
└─────────────────────────────────────────┘{Colors.END}
    """
    print(menu)

def show_instructions():
    """Show usage instructions"""
    instructions = [
        "Enter phone number with country code",
        "Example: +1234567890 (USA)",
        "Example: +447911123456 (UK)",
        "Example: +254712345678 (Kenya)",
        "",
        "Country codes: +1 (US/CA), +44 (UK),",
        "+254 (KE), +91 (IN), +86 (CN), etc."
    ]
    print_box("📖 INSTRUCTIONS", instructions, Colors.BLUE)

def show_about():
    """Show about information"""
    about = [
        "Phone Number Location Tracker v2.0",
        "Optimized for Termux & Linux",
        "",
        "Features:",
        "• Real-time phone tracking",
        "• Carrier identification",
        "• Interactive map generation",
        "• Animated terminal interface",
        "",
        "Note: Location is approximate based",
        "on carrier registration data."
    ]
    print_box("ℹ️  ABOUT", about, Colors.BLUE)

def main():
    """Main function with animated interface"""
    
    API_KEY = 'b18b218fd043493ba212ace3f523a9b1'
    
    while True:
        clear_screen()
        print_banner()
        show_menu()
        
        choice = input(f"\n{Colors.BOLD}Enter your choice [1-4]: {Colors.END}").strip()
        
        if choice == '1':
            clear_screen()
            print_banner()
            animated_print("🔍 Starting Phone Number Tracker...", Colors.CYAN, 0.02)
            time.sleep(0.5)
            
            phone_number = input(f"\n{Colors.BOLD}📱 Enter phone number (e.g., +1234567890): {Colors.END}").strip()
            
            if not phone_number:
                animated_print("❌ No phone number entered!", Colors.RED)
                input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.END}")
                continue
            
            if not phone_number.startswith('+'):
                animated_print("⚠️  Adding '+' prefix to number...", Colors.YELLOW, 0.02)
                phone_number = '+' + phone_number
                time.sleep(0.5)
            
            result = get_phone_location(phone_number, API_KEY)
            
            if "error" in result:
                animated_print(f"❌ Error: {result['error']}", Colors.RED)
            else:
                animated_print(f"✅ Tracking completed successfully!", Colors.GREEN, 0.02)
                animated_print(f"📂 Map saved: {result['map_file']}", Colors.CYAN, 0.02)
            
            input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.END}")
            
        elif choice == '2':
            clear_screen()
            print_banner()
            show_instructions()
            input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.END}")
            
        elif choice == '3':
            clear_screen()
            print_banner()
            show_about()
            input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.END}")
            
        elif choice == '4':
            clear_screen()
            animated_print("👋 Thank you for using Phone Tracker!", Colors.CYAN, 0.03)
            animated_print("🚀 Exiting...", Colors.YELLOW, 0.03)
            time.sleep(1)
            sys.exit(0)
            
        else:
            animated_print("❌ Invalid choice! Please select 1-4", Colors.RED)
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Program interrupted by user. Exiting...{Colors.END}")
        sys.exit(0)
