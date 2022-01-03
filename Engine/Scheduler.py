import user_lists


def get_role(role, remaining_time):
    while remaining_time > 0:
        user = user_lists.get_role(role)
        if user is not None:
            return user
    return None
