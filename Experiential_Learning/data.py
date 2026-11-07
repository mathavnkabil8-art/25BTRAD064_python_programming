# transit_data.py - Isolated Topographical Database Configuration

# 🗺️ Multi-Modal Hub Graph Matrix
TRANSIT_GRAPH = {
    "Hostel_Block": {
        "Campus_Gate": [
            {"mode": "Walking", "time": 12, "cost": 0, "carbon": 0.0},
            {"mode": "E-Shuttle", "time": 4, "cost": 10, "carbon": 0.1}
        ]
    },
    "Campus_Gate": {
        "Tech_Park_Metro": [
            {"mode": "Auto_Rickshaw", "time": 15, "cost": 60, "carbon": 1.2},
            {"mode": "Public_Bus", "time": 25, "cost": 15, "carbon": 0.5},
            {"mode": "Premium_Cab", "time": 12, "cost": 180, "carbon": 2.0}
        ]
    },
    "Tech_Park_Metro": {
        "City_Center": [
            {"mode": "Metro_Train", "time": 20, "cost": 40, "carbon": 0.2}
        ]
    }
}

# 🚦 Traffic Parameters Configuration
RUSH_HOURS = [(8, 10), (17, 19)]  # Morning (8-10 AM) and Evening (5-7 PM) windows
ROAD_VEHICLES = ["Auto_Rickshaw", "Premium_Cab", "Public_Bus"]
CONGESTION_MULTIPLIER = 1.5
