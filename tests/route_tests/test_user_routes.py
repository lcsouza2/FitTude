from fastapi.testclient import TestClient
from app.routes.user_routes import USER_ROUTER, save_pwd_change_protocol, search_for_user, 

test_client = TestClient(USER_ROUTER)

def test_create_user():