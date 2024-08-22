from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from transliterate import translit
from transliterate.exceptions import LanguagePackNotFound

from codenames import gen_word, load_words, Words


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
    project: Annotated[str, Form()],
    number: Annotated[int, Form()],
):
    gen_name = await gen_word(request.app.words)
    project_name = f"{project}_{gen_name}"
    try:
        project_name = translit(project_name, language)
    except LanguagePackNotFound:
        pass
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "project_name": f"{project_name}_{number}",
            "language": language,
            "project": project,
            "number": number,
        },
    )
