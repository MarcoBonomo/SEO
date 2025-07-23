import requests
from datetime import datetime

def get_first_archive_date(url):
    """Get the earliest archived date from Wayback Machine"""
    api_url = f"http://archive.org/wayback/available?url={url}"
    
    try:
        response = requests.get(api_url)
        data = response.json()
        
        if data['archived_snapshots']:
            # Get the closest snapshot (usually the earliest)
            snapshot = data['archived_snapshots']['closest']
            timestamp = snapshot['timestamp']
            
            # Convert timestamp to readable date
            date_obj = datetime.strptime(timestamp, '%Y%m%d%H%M%S')
            return date_obj.strftime('%Y-%m-%d')
        else:
            return "No archived snapshots found"
    
    except Exception as e:
        return f"Error: {e}"

def get_all_snapshots(url, year=None):
    """Get all available snapshots for a URL"""
    if year:
        api_url = f"http://web.archive.org/cdx/search/cdx?url={url}&output=json&fl=timestamp&filter=statuscode:200&collapse=digest&from={year}"
    else:
        api_url = f"http://web.archive.org/cdx/search/cdx?url={url}&output=json&fl=timestamp&filter=statuscode:200&collapse=digest"
    
    try:
        response = requests.get(api_url)
        data = response.json()
        
        if len(data) > 1:  # First row is headers
            timestamps = [row[0] for row in data[1:]]  # Skip header row
            dates = [datetime.strptime(ts, '%Y%m%d%H%M%S').strftime('%Y-%m-%d %H:%M:%S') for ts in timestamps]
            return sorted(dates)
        else:
            return []
    
    except Exception as e:
        return f"Error: {e}"

# The URL you want to check
url = "https://www.oncrawl.com/technical-seo/data-driven-seo-using-oncrawl-api-python/"

print(f"Analyzing URL: {url}")
print("=" * 80)

# Get the first archived date
first_date = get_first_archive_date(url)
print(f"First archived date: {first_date}")

# Get all snapshots
print("\nGetting all snapshots...")
snapshots = get_all_snapshots(url)

if snapshots and isinstance(snapshots, list):
    print(f"Total snapshots found: {len(snapshots)}")
    print(f"Earliest snapshot: {snapshots[0]}")
    print(f"Latest snapshot: {snapshots[-1]}")
    
    # Show first 10 snapshots
    print(f"\nFirst 10 snapshots:")
    for i, snapshot in enumerate(snapshots[:10]):
        print(f"  {i+1}. {snapshot}")
    
    if len(snapshots) > 10:
        print(f"  ... and {len(snapshots) - 10} more snapshots")
        
elif isinstance(snapshots, str):
    print(f"Error getting snapshots: {snapshots}")
else:
    print("No snapshots found")

