"""
Configurações de midllewares
"""


class Users:

    exists = {"methods": ["UPDATE", "DELETE"], "path": "/users/", "ignore": ["/auth/logout/"]}
    check = {"methods": ["PATCH", "DELETE"], "path": "/users/", "ignore":["/auth/logout/"]}
    not_exists = {"methods": ["POST"], "path": "/users/", "ignore": ["/auth/logout"]}
    token= {"methods": ["PATCH", "DELETE"], "path": "/users/", "ignore": ["/auth/logout/"]}


