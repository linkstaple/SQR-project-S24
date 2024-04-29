from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi


def setup(app: FastAPI) -> None:
    def api_schema():
        schema_routes = list(filter(
            lambda route: route.path.startswith('/api'),
            app.routes))
        openapi_schema = get_openapi(
            title="LazySplitAPI",
            version="1.0.0",
            summary="This is OpenAPI schema for LazySplit app",
            description="Description of API urls for LazySplit app",
            routes=schema_routes,
        )

        app.openapi_schema = openapi_schema
        return app.openapi_schema

    app.openapi = api_schema
