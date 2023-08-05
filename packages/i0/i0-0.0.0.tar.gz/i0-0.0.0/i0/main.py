import uvicorn

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


import typer

cli = typer.Typer()

@cli.command()
def collect(host: str = '0.0.0.0', port: str = '5000'):
    uvicorn.run("i0.main:app", host=host, port=port, log_level="info")

if __name__ == "__main__":
    cli()
