import json
import argparse
from datetime import datetime, timedelta
import pytz
import logging
import sys
import csv

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def parse_geo_location(geo):
    if geo and geo.startswith("geo:"):
        try:
            lat, lon = geo[4:].split(',')
            return float(lat), float(lon)
        except (ValueError, IndexError):
            logging.warning(f"Invalid geo location format: {geo}")
    return None, None

def transform_data(data, target_timezone):
    transformed_data = []
    target_tz = pytz.timezone(target_timezone)

    for entry in data:
        try:
            if 'visit' in entry:
                lat, lon = parse_geo_location(entry['visit']['topCandidate'].get('placeLocation'))
                date = convert_to_timezone(entry['startTime'], target_tz)
                semantic_type = entry['visit']['topCandidate'].get('semanticType')
                transformed_data.append({
                    'date': date,
                    'type': semantic_type if semantic_type else 'Unknown',
                    'latitude': lat,
                    'longitude': lon
                })

            if 'activity' in entry:
                start_lat, start_lon = parse_geo_location(entry['activity'].get('start'))
                end_lat, end_lon = parse_geo_location(entry['activity'].get('end'))
                start_date = convert_to_timezone(entry['startTime'], target_tz)
                end_date = convert_to_timezone(entry['endTime'], target_tz)
                activity_type = entry['activity']['topCandidate'].get('type')
                transformed_data.append({
                    'date': start_date,
                    'type': activity_type if activity_type else 'Unknown',
                    'latitude': start_lat,
                    'longitude': start_lon
                })
                transformed_data.append({
                    'date': end_date,
                    'type': activity_type if activity_type else 'Unknown',
                    'latitude': end_lat,
                    'longitude': end_lon
                })

            if 'timelinePath' in entry:
                start_time = datetime.fromisoformat(entry['startTime'].replace("Z", "+00:00"))
                start_time = start_time.astimezone(target_tz)
                for point in entry['timelinePath']:
                    offset = int(point['durationMinutesOffsetFromStartTime'])
                    time_at_point = start_time + timedelta(minutes=offset)
                    lat, lon = parse_geo_location(point['point'])
                    transformed_data.append({
                        'date': time_at_point.strftime('%Y-%m-%d %H:%M:%S'),
                        'type': 'Unknown',
                        'latitude': lat,
                        'longitude': lon
                    })
        except KeyError as e:
            logging.warning(f"Missing key in entry: {e}")
        except Exception as e:
            logging.error(f"Error processing entry: {e}")

    transformed_data.sort(key=lambda x: x['date'])
    # Remove rows with type = 'Searched Address'
    transformed_data = [row for row in transformed_data if row['type'] != 'Searched Address']
    return transformed_data

def convert_to_timezone(time_str, target_tz):
    try:
        dt = datetime.fromisoformat(time_str)
        dt = dt.astimezone(target_tz)
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    except ValueError as e:
        logging.warning(f"Invalid time format: {time_str}")
        return time_str

def save_to_csv(data, output_file):
    fieldnames = ['date', 'type', 'latitude', 'longitude']
    try:
        with open(output_file, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        logging.info(f"Transformed data saved to {output_file}")
    except IOError as e:
        logging.error(f"Error saving data to CSV: {e}")

def list_timezones():
    print("Available timezones:")
    for tz in pytz.all_timezones:
        print(tz)

def main():
    parser = argparse.ArgumentParser(usage="\n\ntimeline_convert.py location-history.json output-data.csv timezone\n"
                                           "    location-history.json: Location data retrieved from Google Timeline\n"
                                           "    output-data.csv: Output file name and path\n"
                                           "    timezone: Timezone to standardize time stamps.")
    parser.add_argument('input_file', type=str, nargs='?', default=None)
    parser.add_argument('output_file', type=str, nargs='?', default=None)
    parser.add_argument('timezone', type=str, nargs='?', default=None)
    parser.add_argument('--timezones', action='store_true', help='List all available timezones')

    args = parser.parse_args()

    if args.timezones:
        list_timezones()
        sys.exit(0)

    if not args.input_file or not args.output_file or not args.timezone:
        parser.print_help()
        sys.exit(1)

    try:
        with open(args.input_file, 'r') as file:
            data = json.load(file)
        logging.info(f"Loaded data from {args.input_file}")
    except Exception as e:
        logging.error(f"Error loading data: {e}")
        return

    transformed_data = transform_data(data, args.timezone)
    save_to_csv(transformed_data, args.output_file)

if __name__ == '__main__':
    main()
