import os
import sys

from fastapi import FastAPI


def set_up(mocker) -> FastAPI:
    os.open('test_lazy_split.db', flags=os.O_CREAT)

    sys.path.append('src/')

    users_exists = mocker.patch(
        'config.Config.sqlite_path',
        'test_lazy_split.db',
    )

    import api
    import middleware
    import static

    app = FastAPI()
    middleware.setup(app)
    api.setup(app)
    static.setup(app)

    return app


def teardown():
    os.remove('test_lazy_split.db')
