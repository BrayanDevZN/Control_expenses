"""
Configurações de midllewares
"""


class Users:

    exists = {"methods": ["UPDATE", "DELETE"], "path": "/users/", "ignore": ["/auth/"]}
    check = {"methods": ["PATCH", "DELETE"], "path": "/users/", "ignore":["/auth/"]}
    not_exists = {"methods": ["POST"], "path": "/users/", "ignore": ["/auth/"]}
    token= {"methods": ["PATCH", "DELETE"], "path": "/users/", "ignore": ["/auth/"]}


