from fastapi import FastAPI, Request, Form, Response,HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates as j
from fastapi.staticfiles import StaticFiles
from typing import Optional
from time import sleep
# sleep(200)
import minio_main as mm
import web as w
import db
import uvicorn
import logging



# logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def screen(url: str, is_fresh):
    exists = db.link_exists(url)
    if not is_fresh:
        # check 4 screen
        if exists:
            log.info('Requested old image, existed')
            screen_path = db.return_path(url)
            # return screen
            return mm.get_file(screen_path)
        else:
            log.info('Requested old image, did not exist')
            # make screen
            screen_path = mm.input_file(w.do_screen(url))
            db.insert_link(url, screen_path)
            return mm.get_file(screen_path)
    # if needed fresh
    screen_path = mm.input_file(w.do_screen(url))
    if exists:
        log.info('Requested new image, existed')
        # input new row
        db.change_path(url,screen_path)
    else:
        log.info('Requested new image, did not exist')
        # overwrite
        db.insert_link(url, screen_path)
    return mm.get_file(screen_path)

    # return open('trash/teses.png',"rb").read()


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
template = j(directory="templates")


# Load main page
@app.get("/", response_class=HTMLResponse)
def main_page(request: Request):
    return template.TemplateResponse(request=request, name="template.html")


# On submitting form return a screenshot
@app.post("/", responses={
    200: {
        "content": {"image/png": {}}
    }
},
          response_class=Response)
def get_url(url: str = Form(), is_fresh: Optional[str] = Form(None)):
    print(url)
    # image_bytes: bytes = screen(url, is_fresh)
    try:
        image_bytes = screen(url, is_fresh)
        return Response(content=image_bytes, media_type="image/png")
    except:
        log.info('here goes 404 ^-^')
        raise HTTPException(status_code=404,
                            detail="Site could not be reached"
                            )
    # media_type here sets the media type of the response sent to the client.


if __name__ == '__main__':
    # screen('https://duckduckgo.com',True)
    uvicorn.run(
        "main:app",
        host='0.0.0.0',
        port=8000,
        reload=True
    )

