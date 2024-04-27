from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi.staticfiles import StaticFiles


def setup(app):
    mount_static_folders(app)

    templates = Jinja2Templates(directory="static")
    html_templates = Jinja2Templates(directory="static/html")

    @app.get("/", response_class=HTMLResponse)
    async def root_page(request: Request):
        return html_templates.TemplateResponse(
            request=request, name="main.html"
        )

    @app.get("/login", response_class=HTMLResponse)
    async def login_page(request: Request):
        return html_templates.TemplateResponse(
            request=request, name="login.html",
            context={'script_type': 'login'}
        )

    @app.get("/register", response_class=HTMLResponse)
    async def register_page(request: Request):
        return html_templates.TemplateResponse(
            request=request, name="login.html",
            context={'script_type': 'register'}
        )

    @app.get("/profile", response_class=HTMLResponse)
    async def profile_page(request: Request):
        return html_templates.TemplateResponse(
            request=request, name="profile.html"
        )

    @app.get("/group/{group_id}")
    def update_item(request: Request, group_id: int):
        return html_templates.TemplateResponse(
            request=request, name="group.html", context={'group_id': group_id}
        )

    @app.get("/easter_egg", response_class=HTMLResponse)
    async def read_item(request: Request):
        return templates.TemplateResponse(
            request=request, name="index.html"
        )


def mount_static_folders(app):
    app.mount("/static", StaticFiles(directory="static"),
              name="static")
    app.mount("/static-css", StaticFiles(directory="static/css"),
              name="static-css")
    app.mount("/static-js", StaticFiles(directory="static/js"),
              name="static-js")
