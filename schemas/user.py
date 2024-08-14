def user_entity(user) -> dict:
    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"],
        "phone": user["phone"],
        "password": user["password"],
    }


def user_list_entity(users) -> list:
    return [user_entity(user) for user in users]
