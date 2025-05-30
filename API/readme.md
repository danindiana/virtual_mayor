<div align="center">
  <img src="https://github.com/user-attachments/assets/50125cae-b489-4611-b9dd-868043f71e45" alt="OpenFEMA Integration Thumbnail" width="400"/>
</div>


To integrate OpenFEMA API with the virtual_mayor project, we'll create a Python-based solution that fetches disaster data from FEMA and processes it for use in the virtual assistant. Here's how to implement this:

1. Create openfema_integration.py in the /API Directory
This module will handle FEMA data fetching and processing:

python
# API/openfema_integration.py
import requests
import pandas as pd
from datetime import datetime

class FEMAIntegration:
    BASE_URL = "https://www.fema.gov/api/open/v1"
    
    def __init__(self, dataset="DisasterDeclarationsSummaries"):
        self.dataset = dataset
    
    def fetch_data(self, filters=None, limit=1000):
        """Fetch data from OpenFEMA API with optional filters"""
        url = f"{self.BASE_URL}/{self.dataset}"
        params = {"$top": limit}
        
        if filters:
            params.update(filters)
            
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching FEMA data: {e}")
            return None
    
    def get_active_disasters(self, days=30):
        """Get recent disasters within the last X days"""
        date_filter = datetime.now().strftime("%Y-%m-%d")
        filters = {
            "$filter": f"declarationDate ge '{date_filter}'",
            "$orderby": "declarationDate desc"
        }
        return self.fetch_data(filters=filters)
    
    def format_for_virtual_mayor(self, raw_data):
        """Transform FEMA data into virtual_mayor compatible format"""
        if not raw_data:
            return []
            
        disasters = []
        for item in raw_data:
            disasters.append({
                "id": item.get("disasterNumber"),
                "title": f"{item.get('incidentType')} in {item.get('state')}",
                "date": item.get("declarationDate"),
                "description": f"FEMA Declaration DR-{item.get('disasterNumber')}",
                "severity": "high" if item.get("ihProgramDeclared") else "medium"
            })
        return disasters
2. Update the Virtual Mayor API (app.py)
Modify the existing API to include FEMA data:

python
# API/app.py (add these updates)
from flask import Flask, jsonify
from openfema_integration import FEMAIntegration

app = Flask(__name__)
fema = FEMAIntegration()

@app.route('/api/disasters', methods=['GET'])
def get_disasters():
    raw_data = fema.get_active_disasters(days=30)
    processed_data = fema.format_for_virtual_mayor(raw_data)
    return jsonify({"disasters": processed_data})

# ... (keep existing routes)
3. Create a Test Script
python
# API/test_fema.py
from openfema_integration import FEMAIntegration

if __name__ == "__main__":
    fema = FEMAIntegration()
    
    # Test data fetch
    print("Testing FEMA Integration...")
    disasters = fema.get_active_disasters(days=7)
    print(f"Found {len(disasters)} recent disasters")
    
    # Test formatting
    formatted = fema.format_for_virtual_mayor(disasters)
    print("Sample formatted entry:", formatted[0] if formatted else None)
4. Update Requirements.txt
Add these dependencies:

requests>=2.28.0
pandas>=1.5.0
python-dateutil>=2.8.0
Key Features Implemented
Modular Integration: Separate FEMA logic from core application

Data Transformation: Converts raw FEMA data into virtual_mayor's expected format

Error Handling: Graceful API failure handling

Filter Support: Built-in date filtering for recent disasters

Usage Examples
Direct Python Usage:

python
from openfema_integration import FEMAIntegration
fema = FEMAIntegration("WebDisasterDeclarations")
print(fema.fetch_data(limit=5))
Via API Endpoint:

bash
curl http://localhost:5000/api/disasters
Sample Output:

json
{
  "disasters": [
    {
      "id": "DR-4750",
      "title": "Hurricane in Florida",
      "date": "2023-09-28",
      "description": "FEMA Declaration DR-4750",
      "severity": "high"
    }
  ]
}
Recommended Enhancements
Caching: Add Redis/Memcached to cache FEMA data (avoid rate limits)

Async Support: Use aiohttp for non-blocking requests

Geospatial Filtering: Filter disasters by location proximity

Webhooks: Add FEMA webhook support for real-time updates
