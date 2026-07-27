import requests

def test_predictions():
    # 1. Test model info
    info_resp = requests.get("http://localhost:8000/api/v1/predictions/model/info")
    print("Model Info Response:", info_resp.status_code)
    print(info_resp.json())
    
    # 2. Test prediction
    payload = {
      "supplier": "Supplier_A",
      "origin": "New York",
      "destination": "Los Angeles",
      "transport_mode": "Road",
      "distance_km": 4000,
      "shipping_cost": 4500,
      "weather_condition": "Storm",
      "traffic_level": "Severe",
      "order_priority": "Low",
      "expected_delivery_days": 5
    }
    
    pred_resp = requests.post("http://localhost:8000/api/v1/predictions/predict", json=payload)
    print("\nPrediction Response:", pred_resp.status_code)
    print(pred_resp.json())

if __name__ == "__main__":
    test_predictions()
