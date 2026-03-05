"""Shared fixtures for end-to-end tests."""
import os
from pathlib import Path

import httpx
import pytest
from dotenv import load_dotenv

# Используем текущую рабочую директорию (где находится .env файл)
env_file = Path.cwd() / '.env.tests.e2e.secret'
print(f"Looking for .env file at: {env_file}")
print(f"File exists: {env_file.exists()}")

if env_file.exists():
    load_dotenv(env_file)
    print("Loaded .env file")
else:
    print(".env file not found!")

@pytest.fixture(scope="session")
def api_base_url() -> str:
    address = os.environ.get("ADDRESS", "")
    port = os.environ.get("PORT", "")
    
    print(f"ADDRESS from env: '{address}'")
    print(f"PORT from env: '{port}'")

    if not address or not port:
        pytest.skip("ADDRESS or PORT environment variables are not set")

    url = f"http://{address}:{port}"
    print(f"Constructed URL: {url}")
    return url.rstrip("/")

@pytest.fixture(scope="session")
def api_token() -> str:
    token = os.environ.get("API_TOKEN", "")
    if not token:
        pytest.skip("API_TOKEN environment variable is not set")
    print(f"API_TOKEN loaded (first 5 chars): {token[:5]}...")
    return token

@pytest.fixture(scope="session")
def client(api_base_url: str, api_token: str) -> httpx.Client:
    return httpx.Client(
        base_url=api_base_url,
        headers={"Authorization": f"Bearer {api_token}"}
    )
