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

Clone the reposity
    Place 'location-history.json' into the root directory.

To use the script, run the following command:

    python timeline_convert.py location-history.json output.csv timezone
> Ensure  `location-history.json` is in the same directory as the script!

Arguments

    location-history.json: The input JSON file containing location data exported from Google Timeline.

    output.csv: The output file name and path where the data will be saved.

    timezone: The timezone to standardize the timestamps to.

> List available timezones with `python timeline_convert.py --timezones`

Optional Arguments

    --timezones: List all available timezones.

Example

    python timeline_convert.py location-history.json output.csv US/Eastern

This command will convert the location-history.json file, standardize all timestamps to 'America/New_York' timezone, and save the transformed data to output.csv.


