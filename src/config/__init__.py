import os


class _Config:
    sqlite_path = 'lazy_split.db'
    sqlite_init_script_path = 'src/db/init.sql'
    jwt_token_secret = None
    bind_host = 'localhost'
    bind_port = 8000
    reload_app = True

    def __init__(self):
        self._try_find_in_env('sqlite_path', 'SQLITE_PATH')
        self._try_find_in_env('sqlite_init_script_path',
                              'SQLITE_INIT_SCRIPT_PATH')
        self._try_find_in_env(
            'jwt_token_secret',
            'JWT_TOKEN_SECRET',
            'secretxdd')
        self._try_find_in_env('bind_host', 'BIND_HOST')
        self._try_find_in_env('bind_port', 'BIND_PORT')
        self._try_find_in_env('reload_app', 'RELOAD_APP')

    def _try_find_in_env(self, key, env_key, fallback=None):
        if os.getenv(env_key) is not None:
            setattr(self, key, os.getenv(env_key))
        elif fallback is not None:
            setattr(self, key, fallback)


Config = _Config()
