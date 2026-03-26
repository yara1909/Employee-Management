from datetime import datetime
from app.config.database import users_collection


def get_user_by_username(username: str):
    return users_collection.find_one({"username": username}, {"_id": 0})




def create_user(user_data: dict):
    users_collection.insert_one(user_data)
    return user_data



def update_user_activity(username: str, new_role: str):
    return users_collection.update_one(
        {"username": username},
        {
            "$push": {
                "activity_log": {
                    "action": f"Role changed to {new_role}",
                    "timestamp": datetime.now()
                }       
            }
        }
    )