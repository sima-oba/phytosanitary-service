import requests
from http import HTTPStatus
from flask import request, abort, jsonify, make_response
from functools import wraps
from requests.exceptions import ConnectionError
from typing import Optional

from .roles import Role
from .user_info import UserInfo


class Authorization:
    def __init__(self, _introspect_uri: str, enabled: bool = True):
        self._introspect_uri = _introspect_uri
        self._global_granted_roles = []
        self._enabled = enabled

    @property
    def current_user(self) -> Optional[UserInfo]:
        if hasattr(request, 'current_user'):
            return request.current_user

        return None

    def grant_role_for_any_request(self, *roles: Role):
        self._global_granted_roles.extend([role.value for role in roles])

    def verify_permission(self, *granted_roles: Role):
        if not self._enabled or request.method == 'OPTIONS':
            return

        token = self._extract_bearer_token()

        if token is None:
            self._send_error('Missing bearer token', HTTPStatus.UNAUTHORIZED)

        user = self._introspect_token(token)

        if user is None:
            self._send_error('Access denied', HTTPStatus.UNAUTHORIZED)

        if not self._is_user_access_granted(user, *granted_roles):
            message = f'User {user.username} does not have privileges'
            self._send_error(message, HTTPStatus.UNAUTHORIZED)

        setattr(request, 'current_user', user)

    def _extract_bearer_token(self) -> Optional[str]:
        header = request.headers.get('Authorization')
        token = header.replace('Bearer ', '') if header else None

        return token

    def _introspect_token(self, token: str) -> Optional[UserInfo]:
        try:
            response = requests.post(
                self._introspect_uri, json={'token': token}
            )
        except ConnectionError:
            self._send_error(
                'Cannot reach authorization server',
                HTTPStatus.SERVICE_UNAVAILABLE
            )

        if response.ok:
            data = response.json()
        else:
            self._send_error(
                'Unexpected authorization error',
                HTTPStatus.INTERNAL_SERVER_ERROR
            )

        if not data.get('active'):
            return None

        return UserInfo(
            username=data['username'],
            doc=data.get('doc'),
            active=data['active'],
            email_verified=data['email_verified'],
            roles=data['realm_access']['roles']
        )

    def _is_user_access_granted(self, user: UserInfo, *granted: Role) -> bool:
        combined_granted_roles = [
            *self._global_granted_roles,
            *[role.value for role in granted]
        ]

        return any(role in combined_granted_roles for role in user.roles)

    def _send_error(self, message: str, status: HTTPStatus):
        payload = jsonify(message=message)
        error = make_response(payload, status)
        abort(error)

    def require_role(self, *roles: Role):
        def decorator(func):

            @wraps(func)
            def wrapper(*args, **kwargs):
                self.verify_permission(*roles)
                return func(*args, **kwargs)

            return wrapper
        return decorator
