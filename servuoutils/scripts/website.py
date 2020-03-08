import os

from starlette.applications import Starlette
from starlette.staticfiles import StaticFiles
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates
import uvicorn

import structlog
logger = structlog.get_logger()

website_path = os.path.realpath('../../../../website')

templates = Jinja2Templates(directory=os.path.join(website_path, 'templates'))

app = Starlette(debug=True)
app.mount('/static', StaticFiles(directory=os.path.join(website_path, 'statics')), name='static')


@app.route('/')
async def homepage(request):
    template = "index.html"
    context = {"request": request}
    return templates.TemplateResponse(template, context)


@app.route('/error')
async def error(request):
    """
    An example error. Switch the `debug` setting to see either tracebacks or 500 pages.
    """
    raise RuntimeError("Oh no")


@app.exception_handler(404)
async def not_found(request, exc):
    """
    Return an HTTP 404 page.
    """
    template = "404.html"
    context = {"request": request}
    return templates.TemplateResponse(template, context, status_code=404)


@app.exception_handler(500)
async def server_error(request, exc):
    """
    Return an HTTP 500 page.
    """
    template = "500.html"
    context = {"request": request}
    return templates.TemplateResponse(template, context, status_code=500)


if __name__ == "__main__":
    WEBSITE_HOST='0.0.0.0'
    WEBSITE_PORT=8000
    logger.info("running_website", path=website_path, host=WEBSITE_HOST, port=WEBSITE_PORT)
    uvicorn.run(app, host=WEBSITE_HOST, port=WEBSITE_PORT)
