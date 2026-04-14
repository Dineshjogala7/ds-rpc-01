# db/users.py
from typing import Dict

users_db: Dict[str, Dict[str, str]] = {
    "Tony":    {"password": "password123", "role": "engineering"},
    "Bruce":   {"password": "securepass",  "role": "marketing"},
    "Sam":     {"password": "financepass", "role": "finance"},
    "Peter":   {"password": "pete123",     "role": "engineering"},
    "Sid":     {"password": "sidpass123",  "role": "marketing"},
    "Natasha": {"password": "hrpass123",   "role": "hr"},
}