#!/usr/bin/env python3
"""
Claude Integration Scenario Test
Claude'un sistem prompt'lari ile nasil calistigini gosteren senaryo testi
"""

import asyncio
import sys
import os
from pathlib import Path

# Backend path'i ekle
backend_path = Path(__file__).parent.parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from claude_integration.system_prompts import (
    get_system_prompt,
    get_turkish_tourist_prompt,
    get_food_explorer_prompt,
    get_emergency_prompt
)

async def test_tourist_conversation_scenarios():
    """Farkli turist senaryolarini test et"""
    
    print("🎭 Claude Integration - Tourist Conversation Scenarios")
    print("=" * 70)
    
    scenarios = [
        {
            "name": "English First-Time Visitor",
            "user_type": "english_tourist",
            "prompt_func": lambda: get_system_prompt(language="english", scenario="first_time_visitor"),
            "expected_features": ["Opera House", "Opal card", "ENGLISH CONVERSATION"]
        },
        {
            "name": "Turkish Food Explorer", 
            "user_type": "turkish_food_lover",
            "prompt_func": lambda: get_system_prompt(language="turkish", scenario="food_explorer"),
            "expected_features": ["TÜRKÇE", "FOOD EXPLORER", "halal"]
        },
        {
            "name": "Budget Traveler",
            "user_type": "budget_conscious",
            "prompt_func": lambda: get_system_prompt(scenario="budget_traveler"),
            "expected_features": ["BUDGET TRAVELER", "free", "public transport"]
        },
        {
            "name": "Family with Kids",
            "user_type": "family_group",
            "prompt_func": lambda: get_system_prompt(scenario="family_with_kids"),
            "expected_features": ["FAMILY", "Taronga Zoo", "stroller-friendly"]
        },
        {
            "name": "Business Traveler",
            "user_type": "business_person",
            "prompt_func": lambda: get_system_prompt(scenario="business_traveler"),
            "expected_features": ["BUSINESS", "CBD", "efficient"]
        }
    ]
    
    test_results = []
    
    for scenario in scenarios:
        print(f"\n🎯 Testing: {scenario['name']}")
        print("-" * 50)
        
        try:
            # Prompt'u olustur
            prompt = scenario["prompt_func"]()
            
            # Temel kontroller
            assert len(prompt) > 1000, "Prompt too short"
            assert "Sydney Guide" in prompt, "Missing Sydney Guide identity"
            assert "MCP tools" in prompt, "Missing MCP tools mention"
            
            # Scenario-specific kontroller
            missing_features = []
            for feature in scenario["expected_features"]:
                if feature not in prompt:
                    missing_features.append(feature)
            
            if missing_features:
                print(f"⚠️  Missing features: {missing_features}")
                test_results.append((scenario["name"], False, f"Missing: {missing_features}"))
            else:
                print(f"✅ All expected features present")
                test_results.append((scenario["name"], True, "All features present"))
            
            # Prompt istatistikleri
            print(f"📊 Prompt stats:")
            print(f"   Length: {len(prompt)} characters")
            print(f"   Words: ~{len(prompt.split())} words")
            print(f"   Lines: {len(prompt.split(chr(10)))} lines")
            
            # Ilk 150 karakter goster
            print(f"📝 Preview: {prompt[:150]}...")
            
        except Exception as error:
            print(f"❌ Error: {str(error)}")
            test_results.append((scenario["name"], False, f"Error: {str(error)}"))
    
    return test_results

async def test_emergency_scenarios():
    """Acil durum senaryolarini test et"""
    
    print(f"\n🚨 Emergency Scenarios Test")
    print("=" * 50)
    
    emergency_types = [
        ("lost_tourist", "Lost Tourist Protocol"),
        ("transport_disruption", "Transport Disruption Protocol"),
        ("weather_emergency", "Weather Emergency Protocol")
    ]
    
    emergency_results = []
    
    for emergency_type, expected_protocol in emergency_types:
        print(f"\n🆘 Testing: {emergency_type}")
        print("-" * 30)
        
        try:
            # Emergency prompt olustur
            emergency_prompt = get_emergency_prompt(emergency_type)
            
            # Emergency protocol en basta olmali
            if not emergency_prompt.startswith(expected_protocol.upper()):
                print(f"⚠️  Emergency protocol not at start")
                emergency_results.append((emergency_type, False, "Protocol not prioritized"))
            else:
                print(f"✅ Emergency protocol properly prioritized")
                emergency_results.append((emergency_type, True, "Protocol prioritized correctly"))
            
            # Emergency-specific kontroller
            if emergency_type == "lost_tourist":
                assert "Stay calm" in emergency_prompt
                assert "current location" in emergency_prompt
                assert "landmarks" in emergency_prompt
            elif emergency_type == "transport_disruption":
                assert "alternative routes" in emergency_prompt
                assert "inconvenience" in emergency_prompt
            elif emergency_type == "weather_emergency":
                assert "safety" in emergency_prompt.lower()
                assert "shelter" in emergency_prompt.lower()
            
            print(f"📊 Emergency prompt length: {len(emergency_prompt)} characters")
            
        except Exception as error:
            print(f"❌ Error: {str(error)}")
            emergency_results.append((emergency_type, False, f"Error: {str(error)}"))
    
    return emergency_results

async def test_language_adaptation():
    """Dil adaptasyonu senaryolarini test et"""
    
    print(f"\n🌍 Language Adaptation Test")
    print("=" * 40)
    
    languages = [
        ("english", "ENGLISH CONVERSATION", "conversational English"),
        ("turkish", "TÜRKÇE KONUŞMA", "halal yemek"),
        ("chinese", "CHINESE CONVERSATION", "respectful"),
        ("japanese", "JAPANESE CONVERSATION", "politeness")
    ]
    
    language_results = []
    
    for lang_code, expected_section, expected_content in languages:
        print(f"\n🗣️  Testing: {lang_code}")
        print("-" * 25)
        
        try:
            # Dil-spesifik prompt olustur
            lang_prompt = get_system_prompt(language=lang_code)
            
            # Dil-spesifik bolum var mi?
            if expected_section not in lang_prompt:
                print(f"⚠️  Missing language section: {expected_section}")
                language_results.append((lang_code, False, f"Missing section: {expected_section}"))
            else:
                print(f"✅ Language section found: {expected_section}")
                
                # Dil-spesifik icerik var mi?
                if expected_content not in lang_prompt:
                    print(f"⚠️  Missing expected content: {expected_content}")
                    language_results.append((lang_code, False, f"Missing content: {expected_content}"))
                else:
                    print(f"✅ Expected content found: {expected_content}")
                    language_results.append((lang_code, True, "All language features present"))
            
        except Exception as error:
            print(f"❌ Error: {str(error)}")
            language_results.append((lang_code, False, f"Error: {str(error)}"))
    
    return language_results

async def test_mcp_tool_integration():
    """MCP tool entegrasyonu test et"""
    
    print(f"\n🛠️  MCP Tool Integration Test")
    print("=" * 40)
    
    # Temel prompt'ta MCP tool'lari kontrol et
    basic_prompt = get_system_prompt()
    
    expected_mcp_capabilities = [
        "Real-time location tracking",
        "Restaurant and attraction recommendations", 
        "Public transport route planning",
        "Journey tracking with proximity alerts",
        "Push notifications",
        "Distance calculations"
    ]
    
    expected_permissions = [
        "To help you better, may I access your current location?",
        "Would you like me to track your journey",
        "Can I send you alerts"
    ]
    
    mcp_results = []
    
    print("🔧 Checking MCP capabilities...")
    missing_capabilities = []
    for capability in expected_mcp_capabilities:
        if capability not in basic_prompt:
            missing_capabilities.append(capability)
    
    if missing_capabilities:
        print(f"⚠️  Missing MCP capabilities: {missing_capabilities}")
        mcp_results.append(("MCP Capabilities", False, f"Missing: {missing_capabilities}"))
    else:
        print(f"✅ All MCP capabilities mentioned")
        mcp_results.append(("MCP Capabilities", True, "All capabilities present"))
    
    print("🔒 Checking permission protocols...")
    missing_permissions = []
    for permission in expected_permissions:
        if permission not in basic_prompt:
            missing_permissions.append(permission)
    
    if missing_permissions:
        print(f"⚠️  Missing permission protocols: {missing_permissions}")
        mcp_results.append(("Permission Protocols", False, f"Missing: {missing_permissions}"))
    else:
        print(f"✅ All permission protocols defined")
        mcp_results.append(("Permission Protocols", True, "All protocols present"))
    
    return mcp_results

async def main():
    """Ana senaryo test fonksiyonu"""
    
    print("🚀 Claude Integration - Complete Scenario Test Suite")
    print("=" * 80)
    
    all_results = []
    
    try:
        # Test 1: Tourist conversation scenarios
        tourist_results = await test_tourist_conversation_scenarios()
        all_results.extend([("Tourist Scenario", name, success, details) for name, success, details in tourist_results])
        
        # Test 2: Emergency scenarios
        emergency_results = await test_emergency_scenarios()
        all_results.extend([("Emergency Scenario", name, success, details) for name, success, details in emergency_results])
        
        # Test 3: Language adaptation
        language_results = await test_language_adaptation()
        all_results.extend([("Language Test", name, success, details) for name, success, details in language_results])
        
        # Test 4: MCP tool integration
        mcp_results = await test_mcp_tool_integration()
        all_results.extend([("MCP Integration", name, success, details) for name, success, details in mcp_results])
        
        # Sonuclari ozetle
        print(f"\n{'='*80}")
        print("📊 CLAUDE INTEGRATION TEST SUMMARY")
        print(f"{'='*80}")
        
        passed = 0
        failed = 0
        
        for test_type, test_name, success, details in all_results:
            status = "✅ PASS" if success else "❌ FAIL"
            print(f"{status} | {test_type:18} | {test_name:25} | {details}")
            
            if success:
                passed += 1
            else:
                failed += 1
        
        print(f"\n📈 Overall Results:")
        print(f"   ✅ Passed: {passed}")
        print(f"   ❌ Failed: {failed}")
        print(f"   📊 Total:  {passed + failed}")
        print(f"   🎯 Success Rate: {(passed/(passed+failed)*100):.1f}%")
        
        if failed == 0:
            print(f"\n🎉 ALL CLAUDE INTEGRATION TESTS PASSED!")
            print(f"🚀 Claude is ready to assist Sydney tourists!")
        else:
            print(f"\n⚠️  Some tests failed. Review system prompts before deployment.")
        
        return failed == 0
        
    except Exception as error:
        print(f"💥 Test suite failed with error: {str(error)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1) 