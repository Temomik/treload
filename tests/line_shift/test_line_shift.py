"""
Regression test for `codeObjectsEqual`.

Background
----------
Before the fix, `codeObjectsEqual` skipped any field whose name contained
"lineno" (so `co_firstlineno`, `co_lnotab`, `co_linetable` were ignored).
As a result, two code objects that differ only by source-line positions
(e.g. a comment / import / blank line added above a function) were treated
as equal, `__code__` was not replaced on reload, and the debugger reported
stale `f_lineno` - breakpoints set on the new lines stopped firing.

The tests below compile two code objects from the SAME `filename` argument
so that only the line-related fields differ. That isolates exactly the case
the fix addresses (full-module reload tests already cover the combined case
where filename/paths also differ).
"""
from old import mod
from treload import reload
from treload.utils.utils import codeObjectsEqual

_FAKE_PATH = 'fake_mod.py'

_SRC_OLD = (
    'def func():\n'
    '    return 42\n'
)

_SRC_NEW_LINES_SHIFTED = (
    '# extra comment\n'
    '\n'
    '\n'
    'def func():\n'
    '    return 42\n'
)


def _compileFunc(source):
    moduleCode = compile(source, _FAKE_PATH, 'exec')
    for const in moduleCode.co_consts:
        if getattr(const, 'co_name', None) == 'func':
            return const
    raise AssertionError('func code object not found')


def test_codeObjectsEqualDetectsFirstLineNoShift():
    """Two code objects with the same bytecode and same co_filename but
    different co_firstlineno must NOT be reported as equal."""
    oldCode = _compileFunc(_SRC_OLD)
    newCode = _compileFunc(_SRC_NEW_LINES_SHIFTED)

    assert oldCode.co_filename == newCode.co_filename, 'preconditions'
    assert oldCode.co_code == newCode.co_code, 'bodies are byte-identical'
    assert oldCode.co_firstlineno != newCode.co_firstlineno, 'only line pos differs'

    assert not codeObjectsEqual(oldCode, newCode), (
        'codeObjectsEqual must consider co_firstlineno, otherwise the debugger '
        'will report stale line numbers after reload'
    )


def test_codeObjectsEqualStillEqualForIdenticalCode():
    """Sanity check: identical sources still compare equal."""
    oldCode = _compileFunc(_SRC_OLD)
    newCode = _compileFunc(_SRC_OLD)

    assert codeObjectsEqual(oldCode, newCode)


def test_reloadUpdatesFirstLineNoEndToEnd():
    """End-to-end smoke test: after reload, line numbers in mod.func's
    __code__ come from the new source file, not the old one."""
    oldLine = mod.func.__code__.co_firstlineno

    assert reload(mod), 'line-only changes must be reported as a reload change'

    newLine = mod.func.__code__.co_firstlineno
    assert newLine != oldLine, (
        'co_firstlineno of reloaded function must match the new source, '
        'otherwise the IDE and runtime line numbers diverge'
    )
    assert mod.func() == 42, 'behaviour must be preserved after reload'
