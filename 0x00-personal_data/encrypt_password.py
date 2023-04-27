#!/usr/bin/env python3
"""[Module]"""
import bcrypt


def hash_password(password: str) -> bytes:
    """[summary]
    Args:
        password (str): [description]
    Returns:
        bytes: [description]
    """
    return bcrypt.hashpw(str.encode(password), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """[summary]
    Args:
        hashed_password (bytes): [description]
        password (str): [description]
    Returns:
        bool: [description]
    """
    return bool(bcrypt.checkpw(str.encode(password), hashed_password))