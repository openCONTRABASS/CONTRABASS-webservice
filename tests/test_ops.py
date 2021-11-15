import io
import pytest
import json
from flask import g, session

DATA_MODEL_FILE = "tests/data/MODEL1507180056_url.xml"


def __read_file(path):
    with open(path, 'r') as file:
        data = file.read().replace('\n', '')
        return data


def test_websocket_endpoints(client):
    assert client.get('/websockets/get_endpoint').status_code == 200
    assert client.get('/websockets/example_event_join').status_code == 200
    assert client.get('/websockets/example_event_message').status_code == 200


@pytest.mark.parametrize("filename", [DATA_MODEL_FILE])
def test_submit(client, filename):
    data = {'file': (io.BytesIO(__read_file(filename).encode()), "model.xml")}
    result = client.post(
        '/submit',
        data=data,
        follow_redirects=True,
        content_type='multipart/form-data'
    )

    assert result.status_code == 200


@pytest.mark.parametrize("filename", [DATA_MODEL_FILE])
def test_critical_reactions(client, filename):
    data = {'file': (io.BytesIO(__read_file(filename).encode()), "model.xml")}
    result = client.post(
        '/submit',
        data=data,
        follow_redirects=True,
        content_type='multipart/form-data'
    )
    assert result.status_code == 200
    data = json.loads(result.get_data(as_text=True))

    assert client.get(f"/results/{data['model_uuid']}/critical_reactions").status_code == 200

@pytest.mark.parametrize("filename", [DATA_MODEL_FILE])
def test_growth_dependent(client, filename):
    data = {'file': (io.BytesIO(__read_file(filename).encode()), "model.xml")}
    result = client.post(
        '/submit',
        data=data,
        follow_redirects=True,
        content_type='multipart/form-data'
    )
    assert result.status_code == 200
    data = json.loads(result.get_data(as_text=True))

    assert client.get(f"/results/{data['model_uuid']}/critical_reactions").status_code == 200
    print(client.get(f"/results/{data['model_uuid']}/critical_reactions").get_data())



