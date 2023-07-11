import pytest
import json

def open_data():
    with open("tests/test_data.json", "r") as data:
        decoded_data = json.load(data)
        data.close()
        # print(decoded_data)
        return decoded_data
