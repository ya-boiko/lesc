import bcrypt


def hashpw(passwd):
    """
    Hashes a password using bcrypt.
    """
    return bcrypt.hashpw(passwd.encode("utf8"), bcrypt.gensalt()).decode("utf8")


print(hashpw("admin"))
