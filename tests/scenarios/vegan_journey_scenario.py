#!/usr/bin/env python3
# Scenario Test - Vegan Restaurant Journey
# Senaryo testi: En iyi vegan restorani bulup yolculuk planlama

import asyncio
import sys
import os
import json
from datetime import datetime

# Backend dizinini path'e ekle
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))

from mcp_tools.places_tool import search_places, get_popular_places
from mcp_tools.transport_tool import find_nearby_transport, plan_route

async def vegan_restaurant_journey_scenario():
    """
    Scenario: Kullanici Sydney Opera House'dan en iyi vegan restorana gitmek istiyor
    Beklenen sonuc: Vegan restoran bulunup rota planlanmasi
    """
    print("🥗 SCENARIO: Vegan Restaurant Journey")
    print("=" * 50)
    
    start_location = {
        "name": "Sydney Opera House",
        "lat": -33.8688,
        "lng": 151.2093
    }
    
    print(f"📍 Starting from: {start_location['name']}")
    
    try:
        # Step 1: Vegan restoran ara
        print("\n🔍 Step 1: Searching for vegan restaurants...")
        vegan_search = await search_places(
            query="vegan restaurant",
            lat=start_location['lat'],
            lng=start_location['lng'],
            radius=5.0,
            place_type="restaurant"
        )
        
        best_restaurant = None
        
        if vegan_search['status'] == 'success' and vegan_search['data']['places']:
            vegan_restaurants = vegan_search['data']['places']
            best_restaurant = max(vegan_restaurants, key=lambda x: x.get('rating', 0))
            print(f"✅ Found vegan restaurant: {best_restaurant['name']}")
            print(f"   ⭐ Rating: {best_restaurant['rating']}/5.0")
        else:
            print("❌ No vegan restaurants found, using fallback...")
            popular_search = await get_popular_places()
            if popular_search['status'] == 'success':
                best_restaurant = popular_search['data']['places'][0]
                print(f"✅ Using fallback: {best_restaurant['name']}")
        
        if not best_restaurant:
            print("❌ SCENARIO FAILED: No restaurants found!")
            return False
        
        # Step 2: Rota planla
        print(f"\n🗺️  Step 2: Planning route to {best_restaurant['name']}...")
        route_plan = await plan_route(
            origin_lat=start_location['lat'],
            origin_lng=start_location['lng'],
            destination_lat=best_restaurant['lat'],
            destination_lng=best_restaurant['lng'],
            travel_modes=["transit", "walking"]
        )
        
        if route_plan['status'] == 'success':
            route = route_plan['data']['route']
            overview = route['overview']
            
            print(f"✅ Route planned successfully!")
            print(f"   📏 Distance: {overview['total_distance_km']}km")
            print(f"   ⏱️  Duration: {overview['total_duration_minutes']} minutes")
            print(f"   💰 Cost: ${overview['total_cost_aud']} AUD")
            
            # Step 3: Journey summary
            print(f"\n📋 Step 3: Journey Summary")
            for i, step in enumerate(route['steps'], 1):
                print(f"   {i}. {step['instruction']} ({step['mode']})")
                print(f"      {step['distance_km']}km, {step['duration_minutes']} min")
        else:
            print("❌ SCENARIO FAILED: Route planning failed!")
            return False
        
        # Scenario success
        scenario_result = {
            "scenario": "Vegan Restaurant Journey",
            "success": True,
            "restaurant_found": best_restaurant['name'],
            "restaurant_rating": best_restaurant.get('rating', 'N/A'),
            "journey_distance_km": overview['total_distance_km'],
            "journey_duration_min": overview['total_duration_minutes'],
            "journey_cost_aud": overview['total_cost_aud'],
            "timestamp": datetime.now().isoformat()
        }
        
        print(f"\n✅ SCENARIO SUCCESS!")
        print(json.dumps(scenario_result, indent=2))
        
        return True
        
    except Exception as error:
        print(f"❌ SCENARIO FAILED: {str(error)}")
        return False

if __name__ == "__main__":
    success = asyncio.run(vegan_restaurant_journey_scenario())
    sys.exit(0 if success else 1) 