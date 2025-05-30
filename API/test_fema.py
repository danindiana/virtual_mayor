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
