import pytest

from app.main import app

from app.gis import get_distance_m

def test_get_distance_m_zero():
    assert get_distance_m( 0, 0, 0, 0 ) == 0

def test_get_distance_m_half_perimeter():
    assert get_distance_m( 0, 0, 180, 0 ) == pytest.approx(20_000_000, abs = 20_000)

from starlette.responses import HTMLResponse
from starlette.testclient import TestClient


def test_app_home():
    client = TestClient(app)
    response = client.get('/')
    assert response.status_code == 200
    
    
def test_app_unknown():
    client = TestClient(app)
    response = client.get('/unknown/')
    assert response.status_code == 404