#!/usr/bin/env python3
"""
Real-time Journey Tracking Scenario Test
Kullanicinin otobuste yolculugu sirasinda gercek zamanli takip ve uyari sistemi
"""

import asyncio
import sys
import os
from pathlib import Path

# Backend path'i ekle
backend_path = Path(__file__).parent.parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from mcp_tools.notification_tool import start_journey_tracking, update_journey_location, stop_journey_tracking

async def test_real_time_journey_tracking():
    """Gercek zamanli yolculuk takibi senaryosu"""
    
    print("🚌 Real-time Journey Tracking Test")
    print("=" * 50)
    
    # 1. Yolculuk planini olustur
    journey_plan = {
        "destination": "Bondi Junction",
        "transport_type": "bus",
        "route": "380 to Bondi Beach",
        "steps": [
            {
                "step_id": 1,
                "transport_type": "bus",
                "route_name": "380 to Bondi Beach",
                "stops": [
                    {"name": "Circular Quay", "lat": -33.8610, "lng": 151.2105, "stop_sequence": 1},
                    {"name": "Museum Station", "lat": -33.8738, "lng": 151.2127, "stop_sequence": 2},
                    {"name": "Hyde Park", "lat": -33.8688, "lng": 151.2093, "stop_sequence": 3},
                    {"name": "Kings Cross", "lat": -33.8737, "lng": 151.2221, "stop_sequence": 4},
                    {"name": "Bondi Junction", "lat": -33.8915, "lng": 151.2477, "stop_sequence": 5}
                ],
                "destination_stop": {"name": "Bondi Junction", "lat": -33.8915, "lng": 151.2477}
            }
        ]
    }
    
    tracking_options = {
        "alert_distance_meters": 300,  # 300 metre yakinlik uyarisi
        "stops_ahead_warning": 2,      # 2 durak onceden uyar
        "gps_update_interval": 10      # 10 saniye GPS guncelleme
    }
    
    # 2. Yolculuk takibini baslat
    print("📍 Starting journey tracking...")
    tracking_result = await start_journey_tracking(
        user_token="user_tourist_123",
        journey_plan=journey_plan,
        tracking_options=tracking_options
    )
    
    if tracking_result["status"] != "success":
        print(f"❌ Failed to start tracking: {tracking_result}")
        return
    
    session_id = tracking_result["data"]["tracking_session"]["session_id"]
    print(f"✅ Journey tracking started - Session: {session_id}")
    print(f"🎯 Destination: {journey_plan['destination']}")
    print(f"🚌 Route: {journey_plan['route']}")
    
    # 3. Simule GPS konumlarini gonder (otobuste yolculuk)
    print("\n🛰️ Simulating GPS updates during bus journey...")
    
    # Simulated GPS coordinates along the bus route
    gps_updates = [
        {"lat": -33.8610, "lng": 151.2105, "location": "Starting at Circular Quay"},
        {"lat": -33.8650, "lng": 151.2110, "location": "Moving towards Museum Station"},
        {"lat": -33.8700, "lng": 151.2120, "location": "Approaching Museum Station"},
        {"lat": -33.8738, "lng": 151.2127, "location": "At Museum Station"},
        {"lat": -33.8720, "lng": 151.2100, "location": "Moving towards Hyde Park"},
        {"lat": -33.8688, "lng": 151.2093, "location": "At Hyde Park"},
        {"lat": -33.8710, "lng": 151.2150, "location": "Moving towards Kings Cross"},
        {"lat": -33.8737, "lng": 151.2221, "location": "At Kings Cross"},
        {"lat": -33.8800, "lng": 151.2300, "location": "Moving towards Bondi Junction"},
        {"lat": -33.8850, "lng": 151.2400, "location": "Approaching Bondi Junction"},
        {"lat": -33.8915, "lng": 151.2477, "location": "Arriving at Bondi Junction"}
    ]
    
    for i, gps_point in enumerate(gps_updates):
        print(f"\n📍 GPS Update {i+1}: {gps_point['location']}")
        print(f"   Coordinates: {gps_point['lat']}, {gps_point['lng']}")
        
        # GPS konumunu guncelle
        location_result = await update_journey_location(
            session_id=session_id,
            current_location={
                "lat": gps_point["lat"],
                "lng": gps_point["lng"],
                "accuracy": 10,
                "timestamp": f"2024-01-01T10:{10+i:02d}:00Z"
            },
            movement_data={
                "speed_kmh": 25,
                "direction": "northeast",
                "in_vehicle": True
            }
        )
        
        if location_result["status"] == "success":
            data = location_result["data"]
            print(f"   ✅ Location updated successfully")
            print(f"   📏 Distance to destination: {data.get('distance_to_destination', 0):.0f}m")
            
            # Tetiklenen uyarilari goster
            triggered_alerts = data.get("triggered_alerts", [])
            if triggered_alerts:
                print(f"   🚨 ALERTS TRIGGERED: {len(triggered_alerts)}")
                for alert in triggered_alerts:
                    if alert.get("notification_sent"):
                        print(f"      📱 NOTIFICATION: {alert['message']}")
                        print(f"      📍 Stop: {alert['stop_name']} ({alert['distance_meters']}m away)")
            else:
                print(f"   ℹ️  No alerts triggered")
                
        else:
            print(f"   ❌ Location update failed: {location_result}")
        
        # Kisa bekleme (gercek senaryoda bu GPS update interval'i olur)
        await asyncio.sleep(0.5)
    
    # 4. Yolculuk takibini durdur
    print(f"\n🛑 Stopping journey tracking...")
    stop_result = await stop_journey_tracking(session_id)
    
    if stop_result["status"] == "success":
        print(f"✅ Journey tracking stopped successfully")
        print(f"📊 Alerts sent: {stop_result['data']['alerts_sent_count']}")
    else:
        print(f"❌ Failed to stop tracking: {stop_result}")
    
    print("\n" + "=" * 50)
    print("🎯 Real-time Journey Tracking Test Completed!")
    
    return {
        "tracking_started": tracking_result["status"] == "success",
        "session_id": session_id,
        "gps_updates_processed": len(gps_updates),
        "tracking_stopped": stop_result["status"] == "success"
    }

async def test_multiple_alerts_scenario():
    """Coklu uyari senaryosu - hedef duraga yaklasirken uyarilar"""
    
    print("\n🎯 Multiple Alerts Scenario Test")
    print("=" * 50)
    
    # Bondi Junction'a giden kisa bir yolculuk
    journey_plan = {
        "destination": "Bondi Junction",
        "steps": [
            {
                "step_id": 1,
                "transport_type": "bus",
                "stops": [
                    {"name": "Kings Cross", "lat": -33.8737, "lng": 151.2221, "stop_sequence": 1},
                    {"name": "Bondi Junction", "lat": -33.8915, "lng": 151.2477, "stop_sequence": 2}
                ],
                "destination_stop": {"name": "Bondi Junction", "lat": -33.8915, "lng": 151.2477}
            }
        ]
    }
    
    # Daha hassas uyari ayarlari
    tracking_options = {
        "alert_distance_meters": 500,  # 500 metre uyari mesafesi
        "stops_ahead_warning": 1,      # 1 durak onceden uyar
        "gps_update_interval": 5
    }
    
    # Takibi baslat
    tracking_result = await start_journey_tracking(
        user_token="user_alert_test_456",
        journey_plan=journey_plan,
        tracking_options=tracking_options
    )
    
    session_id = tracking_result["data"]["tracking_session"]["session_id"]
    print(f"📍 Alert test tracking started - Session: {session_id}")
    
    # Hedef duraga yaklasan GPS noktalari
    approaching_points = [
        {"lat": -33.8800, "lng": 151.2300, "distance_desc": "1500m away"},
        {"lat": -33.8850, "lng": 151.2400, "distance_desc": "800m away"},
        {"lat": -33.8880, "lng": 151.2450, "distance_desc": "400m away - ALERT ZONE"},
        {"lat": -33.8900, "lng": 151.2470, "distance_desc": "200m away - FINAL ALERT"},
        {"lat": -33.8915, "lng": 151.2477, "distance_desc": "Arrived at destination"}
    ]
    
    total_alerts = 0
    
    for i, point in enumerate(approaching_points):
        print(f"\n📍 Position {i+1}: {point['distance_desc']}")
        
        location_result = await update_journey_location(
            session_id=session_id,
            current_location={
                "lat": point["lat"],
                "lng": point["lng"],
                "accuracy": 5
            }
        )
        
        if location_result["status"] == "success":
            triggered_alerts = location_result["data"].get("triggered_alerts", [])
            total_alerts += len(triggered_alerts)
            
            if triggered_alerts:
                print(f"   🚨 {len(triggered_alerts)} ALERT(S) TRIGGERED!")
                for alert in triggered_alerts:
                    print(f"      📱 {alert['message']}")
            else:
                print(f"   ℹ️  No alerts (distance: {location_result['data']['distance_to_destination']:.0f}m)")
        
        await asyncio.sleep(0.3)
    
    # Takibi durdur
    await stop_journey_tracking(session_id)
    
    print(f"\n📊 Total alerts sent during approach: {total_alerts}")
    print("✅ Multiple alerts scenario completed!")
    
    return total_alerts

async def main():
    """Ana test fonksiyonu"""
    print("🚀 Starting Real-time Journey Tracking Tests")
    print("=" * 60)
    
    try:
        # Test 1: Tam yolculuk takibi
        result1 = await test_real_time_journey_tracking()
        
        # Test 2: Coklu uyari senaryosu
        alerts_count = await test_multiple_alerts_scenario()
        
        # Sonuclari ozetle
        print(f"\n📋 TEST SUMMARY")
        print("=" * 30)
        print(f"✅ Journey tracking: {'PASSED' if result1['tracking_started'] else 'FAILED'}")
        print(f"✅ GPS updates: {result1['gps_updates_processed']} processed")
        print(f"✅ Multiple alerts: {alerts_count} alerts triggered")
        print(f"✅ Session cleanup: {'PASSED' if result1['tracking_stopped'] else 'FAILED'}")
        
        print(f"\n🎉 All real-time journey tracking tests completed successfully!")
        
    except Exception as error:
        print(f"❌ Test failed with error: {str(error)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main()) 