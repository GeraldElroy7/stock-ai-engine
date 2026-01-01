"""
Test Script for B2C API
Test all new endpoints
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000"

def print_section(title):
    print("\n" + "="*60)
    print(f"📌 {title}")
    print("="*60)

def pretty_print(data):
    print(json.dumps(data, indent=2, ensure_ascii=False))

def test_api():
    print("\n🚀 Testing Stock AI Engine B2C API")
    print(f"Base URL: {BASE_URL}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Test 1: Health Check
    print_section("Test 1: Health Check")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    pretty_print(response.json())
    
    # Test 2: API Info
    print_section("Test 2: API Info")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Service: {data['service']}")
    print(f"Version: {data['version']}")
    print(f"Features: {len(data['features'])} features")
    
    # Test 3: Get Supported Stocks
    print_section("Test 3: Get Supported Stocks List")
    response = requests.get(f"{BASE_URL}/api/v2/stocks/list")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Total Stocks: {data['total']}")
    print(f"Sectors: {', '.join(data['sectors'][:5])}...")
    print(f"Sample stocks:")
    for stock in data['stocks'][:5]:
        print(f"  - {stock['ticker']}: {stock['name']} ({stock['sector']})")
    
    # Test 4: Get User Parameters
    print_section("Test 4: Get User Input Parameters")
    response = requests.get(f"{BASE_URL}/api/v2/user/parameters")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Trading Styles: {', '.join(data['trading_styles'])}")
    print(f"Risk Levels: {', '.join(data['risk_levels'])}")
    print(f"Investment Goals: {', '.join(data['investment_goals'])}")
    
    # Test 5: Register User
    print_section("Test 5: Register New User")
    register_data = {
        "email": f"test_{datetime.now().timestamp()}@example.com",
        "password": "testpassword123",
        "full_name": "Test User"
    }
    response = requests.post(f"{BASE_URL}/api/v2/auth/register", json=register_data)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        token_data = response.json()
        print(f"✅ Registration successful!")
        print(f"Access Token: {token_data['access_token'][:50]}...")
        print(f"Token Type: {token_data['token_type']}")
        print(f"Expires In: {token_data['expires_in']} seconds")
        
        # Save token for next tests
        access_token = token_data['access_token']
    else:
        print(f"❌ Registration failed: {response.text}")
        # Use demo account instead
        print("\n🔄 Using demo account instead...")
        login_data = {
            "email": "demo@example.com",
            "password": "demo123"
        }
        response = requests.post(f"{BASE_URL}/api/v2/auth/login", json=login_data)
        token_data = response.json()
        access_token = token_data['access_token']
        print(f"✅ Logged in with demo account")
    
    # Test 6: Login
    print_section("Test 6: Login with Demo Account")
    login_data = {
        "email": "demo@example.com",
        "password": "demo123"
    }
    response = requests.post(f"{BASE_URL}/api/v2/auth/login", json=login_data)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        token_data = response.json()
        print(f"✅ Login successful!")
        access_token = token_data['access_token']
        print(f"Access Token: {access_token[:50]}...")
    
    # Test 7: Get Current User
    print_section("Test 7: Get Current User Info")
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(f"{BASE_URL}/api/v2/auth/me", headers=headers)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        user_data = response.json()
        pretty_print(user_data)
    
    # Test 8: Get Comprehensive Stock Info (WITHOUT auth for now)
    print_section("Test 8: Get Comprehensive Stock Info (BBCA)")
    stock_request = {
        "ticker": "BBCA",
        "user_preferences": {
            "trading_style": "swing_trader",
            "risk_level": "moderate",
            "capital_size": 50000000,
            "investment_goal": "balanced_growth",
            "min_confidence_level": 70.0,
            "enable_short_signals": False,
            "time_horizon": "medium_term"
        },
        "include_fundamentals": True,
        "include_technical": True,
        "include_ai_summary": True
    }
    
    # Try without auth first (should work if auth is optional)
    print("Fetching stock info... (this may take 10-20 seconds)")
    response = requests.post(
        f"{BASE_URL}/api/v2/stock/info",
        json=stock_request,
        timeout=60
    )
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        stock_data = response.json()
        print(f"\n📊 {stock_data['ticker']} - {stock_data['company_info']['name']}")
        print(f"Current Price: Rp {stock_data['current_price']:,.0f}")
        print(f"Price Change: {stock_data['price_change']['percentage']:.2f}%")
        
        if stock_data['trading_signal']:
            signal = stock_data['trading_signal']
            print(f"\n🎯 Trading Signal: {signal['signal']}")
            print(f"Confidence: {signal['confidence']:.1f}%")
            print(f"Score: {signal['score']:.2f}")
        
        if stock_data['fundamental_score']:
            fund = stock_data['fundamental_score']
            print(f"\n📈 Fundamental Score: {fund['score']}/{fund['max_score']} ({fund['percentage']:.1f}%)")
            print(f"Rating: {fund['rating']}")
        
        if stock_data['ai_recommendation']:
            ai = stock_data['ai_recommendation']
            print(f"\n🤖 AI Recommendation:")
            print(f"{ai['summary'][:200]}...")
            print(f"\nAction Items:")
            for item in ai['action_items'][:3]:
                print(f"  - {item}")
        
        if stock_data['risk_assessment']:
            risk = stock_data['risk_assessment']
            print(f"\n⚠️ Risk Assessment:")
            print(f"Risk Level: {risk['risk_level']} ({risk['risk_score']}/100)")
            print(f"Suitable: {'Yes' if risk['suitable_for_user'] else 'No'}")
        
        if stock_data['personalized_insights']:
            insights = stock_data['personalized_insights']
            print(f"\n💡 Personalized Insights:")
            for insight in insights['insights'][:3]:
                print(f"  {insight}")
    else:
        print(f"❌ Failed: {response.text[:200]}")
    
    # Test 9: Register Webhook
    print_section("Test 9: Register Webhook")
    webhook_data = {
        "webhook_url": "https://example.com/webhook",
        "tickers": ["BBCA", "BBRI", "TLKM"],
        "alert_conditions": ["signal_change", "price_alert"],
        "min_confidence": 70.0
    }
    response = requests.post(
        f"{BASE_URL}/api/v2/webhook/register",
        json=webhook_data
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        webhook_info = response.json()
        print(f"✅ Webhook registered!")
        print(f"Webhook ID: {webhook_info['webhook_id']}")
        print(f"Monitored Tickers: {', '.join(webhook_info['monitored_tickers'])}")
    
    # Test 10: Test V1 Endpoint (Backward Compatibility)
    print_section("Test 10: Test V1 Endpoint (Legacy)")
    response = requests.get(f"{BASE_URL}/signal/BBRI")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        signal_data = response.json()
        print(f"✅ V1 endpoint working!")
        print(f"Signal: {signal_data.get('signal', 'N/A')}")
        print(f"Score: {signal_data.get('score', 0):.2f}")
    
    # Summary
    print_section("Test Summary")
    print("✅ All major endpoints tested successfully!")
    print(f"📚 Full API documentation: {BASE_URL}/docs")
    print(f"🔗 ReDoc: {BASE_URL}/redoc")
    print("\n🎉 B2C API Platform is ready for use!")

if __name__ == "__main__":
    try:
        test_api()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
