import urllib.request, urllib.error
import json

def get_coordinates(port=4242):
    url = f"http://localhost:{port}/coordinates"
    try:
        with urllib.request.urlopen(url) as response:
            # Read the response and decode from bytes to string
            data_str = response.read().decode("utf-8")
            # Parse JSON string into a Python object (a list in this case)
            try:
                data = json.loads(data_str)
                # Ensure is properly formatted (b/c of trolls)
                assert isinstance(data, list)
                assert all(isinstance(x, tuple) for x in data)
            except Exception as e:
                print(f"Error: {e}")
                return []
            return data
    except urllib.error.URLError as e:
        return []
