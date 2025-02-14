import pandas as pd
import folium
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import time
import os

def main():
    print("Starting store visualization...")
    
    # Check if CSV exists
    if not os.path.exists('test.csv'):
        print("Error: test.csv not found in current directory!")
        return

    # Read the CSV file
    try:
        df = pd.read_csv('test.csv')
        print(f"Successfully loaded {len(df)} stores from CSV")
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return

    # Initialize geocoder
    geolocator = Nominatim(user_agent="my_bionetz_app")
    
    # Create a map centered on Switzerland
    m = folium.Map(location=[46.8182, 8.2275], zoom_start=8)
    
    # Counter for successful geocoding
    success_count = 0
    
    print("Starting to geocode addresses...")
    
    # Add markers for each store
    for idx, row in df.iterrows():
        # Clean up address by removing extra spaces and quotes
        address = row['Adresse'].strip().strip('"').strip()
        name = row['Name'].strip().strip('"').strip()
        
        # Create full address
        full_address = f"{address}, Switzerland"
        
        print(f"Processing ({idx+1}/{len(df)}): {name}")
        
        # Try to geocode with retry
        for attempt in range(3):
            try:
                location = geolocator.geocode(full_address)
                if location:
                    folium.Marker(
                        [location.latitude, location.longitude],
                        popup=name,
                        tooltip=name
                    ).add_to(m)
                    success_count += 1
                    break
                time.sleep(1)  # Be nice to the geocoding service
            except GeocoderTimedOut:
                if attempt == 2:  # Last attempt
                    print(f"Failed to geocode: {name}")
                time.sleep(2)  # Wait longer between retries
            except Exception as e:
                print(f"Error processing {name}: {e}")
                break

    # Save the map
    try:
        output_file = 'store_locations.html'
        m.save(output_file)
        print(f"\nSuccessfully created map with {success_count} locations")
        print(f"Map saved as: {os.path.abspath(output_file)}")
    except Exception as e:
        print(f"Error saving map: {e}")

if __name__ == "__main__":
    main()
