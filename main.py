from contextlib import asynccontextmanager
from typing import Annotated, Literal

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from codenames import load_words, Words, gen_name


@asynccontextmanager
async def lifespan(app: FastAPI):
    adjs, adjs_weights = await load_words('words/adj.txt')
    nouns, nouns_weights = await load_words('words/noun.txt')
    words = Words(
        adjs=adjs,
        adjs_weights=adjs_weights,
        nouns=nouns,
        nouns_weights=nouns_weights,
    )
    app.words = words
    yield


app = FastAPI(lifespan=lifespan)


templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def index_handler(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html", context={}
    )


@app.post("/", response_class=HTMLResponse)
async def index_form_handler(
    request: Request,
    language: Annotated[str, Form()],
    project: Annotated[Literal["project", "operation"], Form()],
    number: Annotated[int, Form()],
):
    project_name = await gen_name(request.app.words, language, project, number)
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "project_name": project_name,
            "language": language,
            "project": project,
            "number": number,
        },
    )
