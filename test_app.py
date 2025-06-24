#!/usr/bin/env python3
"""
Simple test script for the Vercel Flask app
"""

import requests
import json

def test_app():
    """Test the Flask app endpoints"""
    base_url = "http://localhost:5000"
    
    print("🧪 Тестирование Flask приложения...")
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health")
        print(f"✅ Health check: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False
    
    # Test status endpoint
    try:
        response = requests.get(f"{base_url}/status")
        print(f"✅ Status check: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"❌ Status check failed: {e}")
        return False
    
    # Test chat endpoint
    try:
        data = {"message": "Привет"}
        response = requests.post(f"{base_url}/chat", json=data)
        print(f"✅ Chat test: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"❌ Chat test failed: {e}")
        return False
    
    # Test scrape endpoint
    try:
        data = {"url": "https://example.com"}
        response = requests.post(f"{base_url}/scrape", json=data)
        print(f"✅ Scrape test: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"❌ Scrape test failed: {e}")
        return False
    
    print("🎉 Все тесты прошли успешно!")
    return True

if __name__ == "__main__":
    test_app() 