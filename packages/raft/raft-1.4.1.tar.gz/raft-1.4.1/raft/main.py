"""
Invoke's own 'binary' entrypoint.

Dogfoods the `program` module.
"""

from . import __version__, Program

program = Program(
    name='Invoke',
    binary='inv[oke]',
    binary_names=['raft', 'inv', 'invoke', 'convoke', 'fab'],
    version=__version__,
)
