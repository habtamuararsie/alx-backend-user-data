#!/usr/bin/env python3
""" a class to manage the API authentication.
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """ API authentication """


    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ validating if endpoint requires authentication """
        if path is None or excluded_paths is None or excluded_paths == []:
            return True

        length_path = len(path)
        if length_path == 0:
            return True

        slashPath = True if path[length_path - 1] == '/' else False

        temp_path = path
        if not slashPath:
            temp_path += '/'

        for exclude in excluded_paths:
            length_exc = len(exclude)
            if length_exc == 0:
                continue

            if exclude[length_exc - 1] != '*':
                if temp_path == exclude:
                    return False
            else:
                if exclude[:-1] == path[:length_exc - 1]:
                    return False

        return True


    def authorization_header(self, request=None) -> str:
        """ authorization header """
        if request is None:
            return None

        result=request.headers.get("Authorization", None)
        return result


    def current_user(self, request=None) -> TypeVar('User'):
        """ autheticate current user """
        return None
