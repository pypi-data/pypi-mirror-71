import os
import metaform
#
import dict2xml
# import dicttoxml

# ------- HTTP Server --------- #
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse

METADRIVE_DIR = os.path.expanduser('~/.metadrive/')
DATA_DIR =  os.path.join(METADRIVE_DIR, 'data')

app = FastAPI()

@app.get("/")
def read_root(request: Request):
    base_url = str(request.base_url).strip('/')
    return {it: f'{base_url}/feed/{it}'
            for it in os.listdir(DATA_DIR)}

@app.get("/feed/{name}")
def read_types(request: Request, name: str, q: str = None):
    base_url = str(request.base_url).strip('/')
    types = os.listdir(f'{DATA_DIR}/{name}')
    return {it: f'{base_url}/feed/{name}/{it}' for it in types}

@app.get("/feed/{name}/{type}")
def read_feed(request: Request, type: str, name: str, q: str = None):
    base_url = str(request.base_url).strip('/')
    fnames = os.listdir(f'{DATA_DIR}/{name}/{type}')
    items = []
    for fname in fnames:
        item = metaform.load(os.path.join(f'{DATA_DIR}/{name}/{type}', fname))
        items.append(item)

    fmt = request.query_params.get('format')
    if fmt == 'rss':
        items_xml = ''
        for item in items:
            # item_xml_b = str(dicttoxml.dicttoxml(item, root=False), encoding='utf-8')
            item_xml = dict2xml.dict2xml(item, wrap="item", indent="")
            items_xml += item_xml

        result = f'''<?xml version="1.0" encoding="UTF-8" ?><rss version="2.0"><channel><title>{name} / {type}</title><link>{base_url}/feed/{name}/{type}</link><description></description>{items_xml}</channel></rss>'''

        return PlainTextResponse(result)

    return items


# ------- CLI Launcher -------- #
import typer

cli = typer.Typer()

@cli.command()
def publish(path: str = '~/.metadrive', host: str = '0.0.0.0', port: str = '1111'):
    uvicorn.run("i0.main:app", host=host, port=port, log_level="info")

if __name__ == "__main__":
    cli()
