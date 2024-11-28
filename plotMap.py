import folium
from datetime import datetime, timedelta, timezone


COLOUR_SCHEME = {
    '31': 'blue',
    '26': 'green',
    '75' : 'red',
    '1' : 'yellow',
    '114' : 'pink'
}

def get_marker_colour(service_number):
    return COLOUR_SCHEME.get(service_number, 'gray')


def create_map(locations, output_file_prefix = "vehicle_locations_map.html"):
    one_hour_ago = datetime.now(timezone.utc) - timedelta(hours=1)
    recent_locations = [
        loc for loc in locations
        if datetime.fromisoformat(loc['recorded_at_time'].replace('Z', '+00:00')) > one_hour_ago
    ]

    if not recent_locations:
        print("No locations provided to plot on the map")
        return
    
    # Calculate average lat + long for centering map:
    avg_lat = sum(location['latitude'] for location in recent_locations) / len(locations)
    avg_lon = sum(location['longitude'] for location in recent_locations) / len(locations)

    cbg_lat = '52.1951'
    cbg_long = '0.1313'

    # Create a map centered at the average location
    m = folium.Map(location=[cbg_lat, cbg_long], zoom_start=12)

    # Add markers to the map
    for location in recent_locations:
        popup_content = (f"Service Number: {location['service_number']}<br>"
            f"Recorded At: {location['recorded_at_time']}<br>"
            f"Vehicle Ref: {location['vehicle_ref']}<br>"
            #f"Origin: {location['origin']}<br>"
            #f"Destination: {location['destination']}<br>"
            #f"Direction: {location['direction']}"
            )


        folium.Marker(
            location=[location['latitude'], location['longitude']],
            popup=f"Service Number: {location['service_number']}<br>Recorded At: {location['recorded_at_time']}<br>Vehicle Ref: {location['vehicle_ref']}",
            icon=folium.Icon(icon="info-sign")
        ).add_to(m)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"{output_file_prefix}_{timestamp}.html"

    # Save the map to an HTML file
    
    m.save(output_file)

    print(f"Map with vehicle locations has been saved to '{output_file}'")
