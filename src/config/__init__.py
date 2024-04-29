import os


class _Config:
    sqlite_path = 'lazy_split.db'
    sqlite_init_script_path = 'src/db/init.sql'
    jwt_token_secret = 'secretxdd'

    def __init__(self):
        self._try_find_in_env('sqlite_path', 'SQLITE_PATH')
        self._try_find_in_env('sqlite_init_script_path',
                              'SQLITE_INIT_SCRIPT_PATH')
        self._try_find_in_env('jwt_token_secret', 'JWT_TOKEN_SECRET')

    def _try_find_in_env(self, key, env_key):
        if os.getenv(env_key) is not None:
            setattr(self, key, os.getenv(env_key))


Config = _Config()
