# Simulate a Firebase-like authentication
firebase_db = {
    "users": {
        "582144194": {
            "balance": 800,
            "firstName": "Amana",
            "gamesPlayed": 0,
            "lastInteraction": 1727467859589,
            "lastName": "Unknown",
            "phoneNumber": "+251935993930",
            "securityCode": 21073,
            "status": "active"
        },
        "5169578668": {
            "balance": 0,
            "firstName": "Penta Web Developers",
            "gamesPlayed": 0,
            "lastInteraction": 1727468195879,
            "lastName": "Unknown",
            "phoneNumber": "+251978011557",
            "securityCode": 13664,
            "status": "active"
        }
    }
}

from game import Player

def authenticate_user(user_id, security_code):
    user = firebase_db['users'].get(user_id)
    if user and user['securityCode'] == security_code:
        return Player(user_id, user['balance'])
    return None
