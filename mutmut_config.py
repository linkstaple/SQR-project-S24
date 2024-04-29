def pre_mutation(context):
    if context.filename[:5] == 'test_':
        context.skip = True

    if context.filename == 'main.py':
        context.skip = True

    if context.filename == '__init__.py':
        context.skip = True

    if context.filename != 'src/db/user.py':
        context.skip = True
