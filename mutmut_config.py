import re


def pre_mutation(context):
    if context.filename[:5] == 'test_':
        context.skip = True

    if context.filename == 'main.py':
        context.skip = True

    if re.match('.*/__init__.py', context.filename):
        context.skip = True

    if context.filename == 'src/db/sqlite.py':
        context.skip = True

    if context.filename != 'src/db/split_history.py':
        context.skip = True
