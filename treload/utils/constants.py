TRELOAD_INTERNAL_PREFIX = '_treload_'
TRELOAD_REFS_ATTR = '_treload_refs_'

MODULE_METADATA_KEYS = ('__name__', '__path__', '__package__', '__loader__', '__spec__')
SKIP_UPDATE_NAMES = set(MODULE_METADATA_KEYS + ('__builtins__', '__slots__', '__tree_hash__', '__orig_bases__'))
SKIP_START_WITH_NAMES = (TRELOAD_INTERNAL_PREFIX, '_abc_')
