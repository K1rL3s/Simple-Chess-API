import os

from dotenv import load_dotenv


load_dotenv()

PORT = os.environ["PORT"]
BASE_URL = f"http://127.0.0.1:{PORT}/api/chess"
API_AUTH_KEY = os.getenv("API_AUTH_KEY")
PREPARED_ENGINES = int(os.getenv("PREPARED_ENGINES") or 0)
headers = {"Authorization": os.environ.get("API_AUTH_KEY")}
