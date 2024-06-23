# Google Timeline Location Data Json Converter

> This script is used convert the new `location-history.json` from Google Timelines mobile export into a standardized csv ready for external analysis.

The output file contains the following columns:

| Column    | Description                                  |
|-----------|----------------------------------------------|
| date      | The standardized timestamp.                  |
| type      | The type of location (e.g., 'Home', 'walking', etc.). |
| latitude  | The latitude of the location.                |
| longitude | The longitude of the location.               |

## Features
- Converts all formats of location data in the json into a single latitude and longitude column.
- Standardizes timestamps to a specified timezone.
- Cleans the data and saves it to a csv file.

## Requirements
**location-history.json**: This is can be downloaded from the Google Maps mobile app.
1. Open the Google Maps app on your phone.
2. Tap on the menu icon (top right corner) and select "Settings".
3. Scroll down to "Location History" and tap on "Download".
4. Select "JSON" as the file format and tap "Download".
5. Place the file in the same directory as the script.

**Install pytz for timezone handling:**

- `pip install pytz`


## Usage

To use the script, run the following command:

    python timeline_convert.py location-history.json output-data.csv timezone

Arguments

    location-history.json: The input JSON file containing location data retrieved from Google Timeline.
    output-data.csv: The output file name and path where the transformed data will be saved.
    timezone: The timezone to standardize the timestamps. Use a valid timezone string from the pytz library.

Optional Arguments

    --timezones: List all available timezones.

Example

sh

python timeline_convert.py location-history.json output-data.csv 'America/New_York'

This command will convert the location-history.json file, standardize all timestamps to 'America/New_York' timezone, and save the transformed data to output-data.csv.
Logging

The script includes logging to provide information about the process and any issues encountered. Logging levels include:

    INFO: General information about the process.
    WARNING: Warnings about potential issues (e.g., invalid geo location format).
    ERROR: Errors that prevent the script from completing successfully.

Example Output

The CSV file will contain the following columns:

    date: The standardized timestamp.
    type: The type of location (e.g., 'Inferred Home', 'walking', etc.).
    latitude: The latitude of the location.
    longitude: The longitude of the location.

Notes

    Ensure that the input JSON file is correctly formatted and contains valid data.
    The timezone must be a valid string recognized by the pytz library.

License

This project is licensed under the MIT License.