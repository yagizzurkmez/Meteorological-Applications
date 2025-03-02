
ROOT="https://data.ecmwf.int/forecasts"  # Replace with the actual root URL
DEST_DIR="/Volumes/YagizHDD/Meteorological-Applications/DATA/AIFS"

# Create the destination directory if it doesn't exist
mkdir -p "$DEST_DIR"

# Define the first and last hours
first_hour="00"  # First hour (00h)
last_hour="48"  # Last hour (48h)

for i in $(seq 0 6 48); do  # Loop from 0 to n  with a step size of 6
    # Format hour correctly as two digits, e.g., 00, 06, 12, etc.

    hour=$i
    
    # Construct the URL
    url="${ROOT}/20250228/00z/aifs-single/0p25/oper/20250228000000-${hour}h-oper-fc.grib2"
    
    # Download the file using curl and save it to the specified directory
    curl -o "$DEST_DIR/$(basename $url)" "$url"
done

# Merging the downloaded files into one using 'cat' 
cat $DEST_DIR/20250228000000-*.grib2 > "$DEST_DIR/merged_20250228000000_${first_hour}_to_${last_hour}.grib2"

echo "Merged GRIB files "
