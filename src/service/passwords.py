import base64

import bcrypt


def hash_password(plain_text_password):
    # Hash a password for the first time
    #   (Using bcrypt, the salt is saved into the hash itself)
    return base64.b64encode(bcrypt.hashpw(
        plain_text_password.encode(), bcrypt.gensalt()))


def check_password(plain_text_password, hashed_password):
    # Check hashed password. Using bcrypt, the salt is saved into the hash
    # itself
    return bcrypt.checkpw(plain_text_password.encode(),
                          base64.b64decode(hashed_password))
