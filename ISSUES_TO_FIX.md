# 🔧 SYDNEY GUIDE - FIX EDİLMESİ GEREKEN SORUNLAR

_Updated: January 2025 - Real API Session Findings_

## 🚀 **REAL API ENABLEMENT SESSION SUMMARY**

### **✅ ACHIEVEMENTS THIS SESSION:**

- **MOCK_MODE=false** successfully enabled
- **Google APIs working** (Places, Directions, Geocoding)
- **Chat interface tested** with real user feedback
- **Critical NSW Transport gap discovered**

### **🚨 MAJOR DISCOVERY: NSW Transport API NOT IMPLEMENTED**

Despite having API key in .env, code line 387-388 shows:

```python
# Note: NSW Transport API integration would go here
# For now, fall back to mock data since NSW API is complex
logger.info("NSW Transport API integration in progress, using mock data")
```

## 🚨 **KRİTİK SORUN: Warren Road Otobüs Durağı (USER TESTED)**

### **Real User Chat Session:**

```
🗣️ User: "73 warren road marrickville bu adresi kullanarak bak"
🎭 System: "Meeks Road durağına ~2 dakika yürüyüş" (YANLIŞ!)
🗣️ User: "yalniz bir sorun var 73 warren road meeks duragina uzak warren road uzerinde basla duraklar olmalii"
🗣️ User: "boyle bir otobus yok dostum eminmisin gercek dataya ulastigina"
🎭 Claude: "Dürüst olmak gerekirse... gerçek zamanlı veri erişimim sandığım kadar kapsamlı değil"
```

**ROOT CAUSE:** NSW Transport API completely fake despite API key configured!

---

## 🚨 **MAJOR ISSUES**

### **1. Transport Data Tamamen Yanlış**

- ❌ **NSW Transport API kullanılmıyor** (mock data)
- ❌ **Otobüs durakları yanlış lokasyonlarda**
- ❌ **Gerçek zamanlı bilgiler fake**
- ❌ **Route planning unreliable**

**FIX NEEDED:**

```python
# mcp_tools/transport_tool.py
# - Real NSW Transport API integration
# - TripPlanner API calls
# - Real bus stop locations
# - Real-time arrivals
```

### **2. Google Places API Mock Mode**

- ❌ **Restoran önerileri mock** (Golden Lotus Vegan gerçek mi?)
- ❌ **Mesafe hesaplamaları tahmin**
- ❌ **Address validation eksik**

**FIX NEEDED:**

```python
# mcp_tools/places_tool.py
# MOCK_MODE=false olsa bile real API calls yapılmıyor
# Google Places API integration missing
```

### **3. MCP WebSocket Instability**

```
ERROR:__main__:MCP WebSocket error: (<CloseCode.ABNORMAL_CLOSURE: 1006>, '')
INFO:__main__:mcp_websocket_connection_closed
```

- ❌ **Connection drops randomly**
- ❌ **No reconnection logic**
- ❌ **Tools become unavailable**

### **4. Intent Detection Problems**

```
🧠 Detected intent: general_exploration
🔧 Recommended tools: []  ← BOŞ!
```

- ❌ **Tool recommendation failing**
- ❌ **"journey_planning" intent detected ama tools boş**
- ❌ **Context loss between messages**

---

## 📊 **DATA ACCURACY ISSUES**

### **5. Fake Real-Time Claims**

Sistem "real-time data" diyor ama:

- ❌ Otobüs süreleri: "7 dakika içinde geliyor" (fake)
- ❌ Restaurant info: Detailed ama mock
- ❌ Journey tracking: "Başlatıldı" ama çalışmıyor

### **6. Address Parsing Zayıf**

"73 warren road marrickville" → Wrong bus stop suggestions

- Geocoding accuracy poor
- Australian address format problems
- Suburb recognition issues

---

## 🔧 **IMMEDIATE ACTION ITEMS**

### **PHASE 1: Critical Data Fixes**

1. **NSW Transport API** gerçek integration
2. **Google Places API** real calls enable
3. **WebSocket connection** stability fix
4. **Address geocoding** accuracy improvement

### **PHASE 2: UX Improvements**

5. **Turkish language** consistency
6. **Intent detection** logic improvement
7. **Tool recommendation** system fix
8. **Context retention** between messages

### **PHASE 3: Features**

9. **Real journey tracking** implementation
10. **Push notifications** system
11. **Mobile app** development
12. **User preferences** persistence

---

## 📱 **SPECIFIC TEST CASES TO FIX**

### **Test Case 1: Warren Road Bus Stops**

- **Input:** 73 Warren Road, Marrickville
- **Expected:** Find actual bus stops on Warren Road
- **Current:** Wrong suggestions (Meeks Road)
- **Fix:** NSW Transport API real integration

### **Test Case 2: Vegan Pho Search**

- **Input:** Vietnamese vegan restaurant search
- **Expected:** Real Google Places results
- **Current:** Mock restaurant suggestions
- **Fix:** Google Places API real calls

### **Test Case 3: Journey Planning**

- **Input:** Transport planning request
- **Expected:** Real-time bus schedules
- **Current:** Fake timing data
- **Fix:** Transport API + WebSocket stability

---

## 🎯 **SUCCESS METRICS**

**When these are fixed:**

- ✅ User gets accurate bus stop locations
- ✅ Real restaurant data from Google Places
- ✅ Actual transport schedules
- ✅ Stable WebSocket connections
- ✅ Consistent Turkish language support

**Current Status:** **PROTOTYPE LEVEL** (mock data)
**Target Status:** **PRODUCTION READY** (real APIs)

---

_Issues identified from chat session: December 2024_
_Priority: HIGH - User experience severely impacted_
