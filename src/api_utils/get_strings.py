import os
from functools import lru_cache
from src.api_utils.api_auth import handle_request
import dotenv
from src.api_utils.create_session import SESSION

dotenv.load_dotenv()
BASE_URL = os.getenv("BASE_URL")
API_KEY = os.getenv("API_KEY")
@lru_cache(maxsize=None)
def get_strings(page: str):
    session = SESSION
    url = f"{BASE_URL}/api/getStrings/{page}"
    api_call = lambda: session.get(url, headers={"api-key": API_KEY})
    response = handle_request(api_call)
    return response