import requests
import time
import subprocess
import sys

def test_api():
    print("Testing API endpoint...")
    # Start the API server in the background
    # We use subprocess to start uvicorn
    proc = subprocess.Popen([sys.executable, "-m", "uvicorn", "api.index:app", "--port", "8000"],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    try:
        # Wait for server to start
        time.sleep(5)
        
        # Make a request
        payload = {
            "symbol": "SPY",
            "strategy": "momentum",
            "start_date": "2023-01-01",
            "end_date": "2023-06-01"
        }
        
        try:
            response = requests.post("http://127.0.0.1:8000/api/run_backtest", json=payload)
            if response.status_code == 200:
                data = response.json()
                print("API Success!")
                print(f"Metrics: {data['metrics']}")
                print(f"Chart Data Points: {len(data['chart_data'])}")
            else:
                print(f"API Failed: {response.status_code}")
                print(response.text)
        except requests.exceptions.ConnectionError:
            print("Failed to connect to API server.")
            
    finally:
        # Kill the server
        proc.terminate()
        proc.wait()

if __name__ == "__main__":
    test_api()
