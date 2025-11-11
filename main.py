import phonenumbers
from phonenumbers import geocoder, carrier
from opencage.geocoder import OpenCageGeocode
import folium
from datetime import datetime

def get_phone_location(phone_number, api_key):
    """
    Track phone number location in real-time
    
    Args:
        phone_number (str): Phone number with country code (e.g., '+1234567890')
        api_key (str): OpenCage Geocoder API key
    
    Returns:
        dict: Location information including coordinates
    """
    try:
        # Parse phone number
        parsed_number = phonenumbers.parse(phone_number)
        
        # Validate phone number
        if not phonenumbers.is_valid_number(parsed_number):
            return {"error": "Invalid phone number"}
        
        # Get location description
        location = geocoder.description_for_number(parsed_number, "en")
        if not location:
            location = "Unknown Location"
        
        # Get carrier information
        carrier_name = carrier.name_for_number(parsed_number, "en")
        if not carrier_name:
            carrier_name = "Unknown Carrier"
        
        print(f"\n{'='*50}")
        print(f"Phone Number: {phone_number}")
        print(f"Location: {location}")
        print(f"Carrier: {carrier_name}")
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*50}\n")
        
        # Geocode the location
        geocoder_client = OpenCageGeocode(api_key)
        results = geocoder_client.geocode(location)
        
        if not results:
            return {
                "error": "Could not geocode location",
                "location": location,
                "carrier": carrier_name
            }
        
        # Extract coordinates
        lat = results[0]['geometry']['lat']
        lng = results[0]['geometry']['lng']
        
        print(f"Coordinates: {lat}, {lng}")
        
        # Create map
        my_map = folium.Map(location=[lat, lng], zoom_start=10)
        
        # Add marker with detailed popup
        popup_text = f"""
        <b>Phone Location</b><br>
        Location: {location}<br>
        Carrier: {carrier_name}<br>
        Coordinates: {lat}, {lng}<br>
        Time: {datetime.now().strftime('%H:%M:%S')}
        """
        
        folium.Marker(
            [lat, lng],
            popup=folium.Popup(popup_text, max_width=300),
            tooltip=location,
            icon=folium.Icon(color='red', icon='info-sign')
        ).add_to(my_map)
        
        # Add circle to show approximate area
        folium.Circle(
            [lat, lng],
            radius=5000,
            color='blue',
            fill=True,
            fillOpacity=0.2
        ).add_to(my_map)
        
        # Save map with timestamp
        filename = f"location_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        my_map.save(filename)
        print(f"Map saved as: {filename}\n")
        
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


def main():
    """Main function for real-time phone tracking"""
    
    # Your OpenCage API key
    API_KEY = 'b18b218fd043493ba212ace3f523a9b1'
    
    print("=" * 50)
    print("Real-Time Phone Number Location Tracker")
    print("=" * 50)
    
    while True:
        # Get phone number from user
        phone_number = input("\nEnter phone number (with country code, e.g., +1234567890) or 'quit' to exit: ").strip()
        
        if phone_number.lower() in ['quit', 'exit', 'q']:
            print("Exiting tracker...")
            break
        
        if not phone_number:
            print("Please enter a valid phone number.")
            continue
        
        # Ensure number starts with '+'
        if not phone_number.startswith('+'):
            print("Warning: Phone number should start with '+' and country code")
            phone_number = '+' + phone_number
        
        # Track the phone number
        result = get_phone_location(phone_number, API_KEY)
        
        if "error" in result:
            print(f"\n❌ Error: {result['error']}\n")
        else:
            print(f"✅ Location tracked successfully!")
            print(f"   Open {result['map_file']} to view the map\n")


if __name__ == "__main__":
    main()
