'''
When picking Pocha as a test framework I forgot that it can have some issues
with not getting installed to path.

This module is a quick workaround. I will likely end up submitting a pullrequest
to their repo to fix this and make it so it will be possible to do:
python3 -m pocha
'''

from pocha.cli import cli
cli()
