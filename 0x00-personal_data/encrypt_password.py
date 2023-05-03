#!/usr/bin/env python3
"""[Module]"""
import bcrypt


def hash_password(password: str) -> bytes:
    """Hashes a password using a random salt.
    """
    return bcrypt.hashpw(str.encode(password), bcrypt.gensalt())

def is_valid(hashed_password: bytes, password: str) -> bool:
    """Checks is a hashed password was formed from the given password.
    """
    return bool(bcrypt.checkpw(str.encode(password), hashed_password))