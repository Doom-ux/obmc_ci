import pytest
import time
import requests
from requests import HTTPError, ConnectionError, Timeout
import json

@pytest.fixture(scope="module")
def session_token():
	url = "https://127.0.0.0:2443/redfish/v1/SessionService/Sessions"
	headers = {"Content-Type": "application/json"}
	data = {"UserName": "root", "Password": "0penBmc"}

	try:
		resp = requests.post(url, headers=headers, data=json.dumps(data), verify=False)

	except ConnectionError:
		assert 0, "A connection error occured."
	except HTTPError:
		assert 0, "HTTP request returned an unsuccessful status code."
	except Timout:
		assert 0, "The request timed out while trying to connect to server or send/get the data."

	return resp

@pytest.fixture(scope="module")
def session_logger():
	logger = logging.getLogger()


def test_auth_correct(session_token):
	#print(session_token.headers)
	#print(session_token.text)
	assert session_token.status_code == 201, "Server: error response."
	assert "X-Auth-Token" in session_token.headers, "Token is not exist."


def test_system_info(session_token):
	url = "https://127.0.0.0:2443/redfish/v1/Systems/system"
	headers = {"X-Auth-Token": session_token.headers["X-Auth-Token"]}

	try:
		r = requests.get(url, headers=headers, verify=False)

	except ConnectionError:
		assert 0, "A connection error occured (func 'test_system_info')."
	except HTTPError:
		assert 0, "HTTP request returned an unsuccessful status code (func 'test_system_info')."
	except Timout:
		assert 0, "The request timed out while trying to get the data (func 'test_system_info')."
	
	data_dict = r.json()

	assert r.status_code == requests.codes.ok, "Server: error response."
	assert "Status" in data_dict, "Property 'Status' is not exist."
	assert "PowerState" in data_dict, "Property 'PowerState' is not exist."


def test_power_on(session_token):
	url = "https://127.0.0.0:2443/redfish/v1/Systems/system/Actions/ComputerSystem.Reset"
	headers = {"X-Auth-Token": session_token.headers["X-Auth-Token"], "Content-Type": "application/json"}
	data = {"ResetType": "On"}

	url_system = "https://127.0.0.0:2443/redfish/v1/Systems/system"
	headers_system = {"X-Auth-Token": session_token.headers["X-Auth-Token"]}

	try:
		r = requests.post(url, headers=headers, data=json.dumps(data), verify=False)
		assert r.status_code == 204, "Server: error response."
		time.sleep(2)
		r = requests.get(url_system, headers=headers_system, verify=False)

	except ConnectionError:
		assert 0, "A connection error occured (func 'test_power_on')."
	except HTTPError:
		assert 0, "HTTP request returned an unsuccessful status code (func 'test_power_on')."
	except Timout:
		assert 0, "The request timed out while trying to get the data (func 'test_power_on')."
	
	data_dict = r.json()
	assert data_dict["PowerState"] == "On", "PowerState is 'Off'."
	

