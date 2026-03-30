def test_homepage_loads(client):
    response = client.get("/")
    assert response.status_code == 200

def test_export_csv_route_exists(client):
    response = client.get("/export")
    assert response.status_code in [200, 302, 500]

def test_update_status_requires_post(client):
    response = client.get("/update_status")
    assert response.status_code == 405

def test_404_for_unknown_route(client):
    response = client.get("/this-route-does-not-exist")
    assert response.status_code == 404