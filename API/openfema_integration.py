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
