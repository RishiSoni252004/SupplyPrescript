import pandas as pd
import numpy as np
import random
import os

def generate_mock_data(num_records=5000, output_path="backend/data/shipments.csv"):
    np.random.seed(42)
    random.seed(42)

    suppliers = [f"Supplier_{char}" for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"]
    origins = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose"]
    destinations = ["Miami", "Atlanta", "Denver", "Seattle", "Boston", "Detroit", "Nashville", "Portland", "Las Vegas", "Orlando"]
    transport_modes = ["Air", "Sea", "Road", "Rail"]
    weather_conditions = ["Clear", "Rain", "Snow", "Storm", "Fog"]
    traffic_levels = ["Low", "Moderate", "High", "Severe"]
    order_priorities = ["Low", "Medium", "High", "Critical"]

    data = {
        "shipment_id": [f"SHP-{i:06d}" for i in range(1, num_records + 1)],
        "supplier": [random.choice(suppliers) for _ in range(num_records)],
        "origin": [random.choice(origins) for _ in range(num_records)],
        "destination": [random.choice(destinations) for _ in range(num_records)],
        "transport_mode": [random.choice(transport_modes) for _ in range(num_records)],
        "distance_km": np.random.randint(100, 5000, size=num_records),
        "shipping_cost": np.random.uniform(50, 10000, size=num_records).round(2),
        "weather_condition": np.random.choice(weather_conditions, size=num_records, p=[0.5, 0.2, 0.1, 0.1, 0.1]),
        "traffic_level": np.random.choice(traffic_levels, size=num_records, p=[0.4, 0.3, 0.2, 0.1]),
        "order_priority": [random.choice(order_priorities) for _ in range(num_records)],
        "expected_delivery_days": np.random.randint(1, 15, size=num_records),
    }

    df = pd.DataFrame(data)

    # Introduce some correlations to make the ML model learn something useful
    # Delay probability increases if:
    # - transport mode is Road/Rail and distance is high
    # - weather is Storm/Snow
    # - traffic is High/Severe
    
    def calculate_actual_delivery(row):
        delay_chance = 0.1 # base chance
        
        if row["weather_condition"] in ["Storm", "Snow"]:
            delay_chance += 0.4
        elif row["weather_condition"] in ["Rain", "Fog"]:
            delay_chance += 0.1
            
        if row["traffic_level"] in ["High", "Severe"]:
            delay_chance += 0.3
            
        if row["transport_mode"] in ["Road", "Rail"] and row["distance_km"] > 2000:
            delay_chance += 0.2
            
        if row["order_priority"] in ["Critical", "High"]:
            delay_chance -= 0.1 # prioritized handling
            
        is_delayed = random.random() < delay_chance
        
        if is_delayed:
            delay_days = random.randint(1, 7)
            actual_days = row["expected_delivery_days"] + delay_days
        else:
            actual_days = row["expected_delivery_days"] - random.randint(0, min(2, row["expected_delivery_days"] - 1))
            
        return max(1, actual_days)

    df["actual_delivery_days"] = df.apply(calculate_actual_delivery, axis=1)
    df["delayed"] = (df["actual_delivery_days"] > df["expected_delivery_days"]).astype(int)

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    df.to_csv(output_path, index=False)
    print(f"Generated {num_records} mock records and saved to {output_path}")

if __name__ == "__main__":
    # Get absolute path relative to the script location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    backend_dir = os.path.dirname(script_dir)
    output_csv_path = os.path.join(backend_dir, "data", "shipments.csv")
    generate_mock_data(output_path=output_csv_path)
