def pre_mutation(context):
    if context.filename == 'src/main.py':
        context.skip = True

    if context.filename == 'src/api/__init__.py':
        context.skip = True

    if context.filename == 'src/config/__init__.py':
        context.skip = True

    if context.filename == 'src/schema/__init__.py':
        context.skip = True

    if context.filename == 'src/static/__init__.py':
        context.skip = True

    if context.filename == 'src/db/sqlite.py':
        context.skip = True
