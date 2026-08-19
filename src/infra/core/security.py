"""
Configurações de midllewares
"""


class Users:

    exits = {"methods": ["UPDATE", "DELETE"], "path": "/users", "ignore": ["/users/logout"]}
    check = {"methods": ["PATCH", "DELETE"], "path": "/users", "ignore":["/users/logout"]}
    not_exists = {"methods": ["POST"], "path": "/users", "ignore": ["/users/logout"]}


