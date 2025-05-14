# api/auth.py
import requests
import os
from dotenv import load_dotenv

load_dotenv()

def get_access_token():
    try:
        response = requests.post(
            os.getenv("AUTH_URL"),
            auth=requests.auth.HTTPBasicAuth(os.getenv("CLIENT_ID"), os.getenv("CLIENT_SECRET")),
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={"grant_type": "client_credentials"}
        )
        response.raise_for_status()
        return response.json().get("access_token")
    except Exception as e:
        raise ValueError(f"Erro ao obter o token: {str(e)}")
