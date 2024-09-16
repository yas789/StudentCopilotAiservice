import requests


def test_controller():
    try:

    
        base_url = "http://127.0.0.1:8000"  # Adjust if your server is running on a different port
        response = requests.post(base_url + "/generate_notes", json={"prompt": "generate_notes"})
        print(response.json())
        assert response.status_code == 200

        print("Test passed successfully")
    except Exception as e:
        print("Test failed:", str(e))

if __name__ == "__main__":
 test_controller()


