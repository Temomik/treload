import types

from treload.type_reloaders import (function, method, classmethod_,
                                    staticmethod_, class_, builtin_)

TYPE_RELOADER_ITEMS = [
    function,
    method,
    classmethod_,
    staticmethod_,
    class_,
    builtin_,
]
