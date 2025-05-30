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
