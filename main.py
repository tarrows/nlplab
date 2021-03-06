import io
import re
import pandas as pd
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import StreamingResponse

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/")
def hello():
    return {"hello": "world"}


@app.get("/items/{item_id}")
def read_item(request: Request, item_id: str):
    context = {"request": request, "item_id": item_id}
    return templates.TemplateResponse("item.html", context)


@app.get("/image")
async def draw_image():
    data = {'y': np.random.randn(10), 'z': np.random.randn(10)}
    df = pd.DataFrame(data, index=pd.period_range('1-2000', periods=10))
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    df.plot(ax=ax)

    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    return StreamingResponse(buf, media_type='image/png')


pattern = r'(\d+):(\d+):(\d+)'
target = re.compile(pattern)


@app.get("/time-series/{name}")
async def draw_time_series(name: str):
    df = pd.read_csv(f'data/{name}.csv', parse_dates=[0])
    print(df)
    df['sec'] = df['time'].map(lambda x: int(target.match(x).group(2)) * 60 + int(target.match(x).group(3)))
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(df['date'], df['sec'])

    daysFmt = mdates.DateFormatter('%Y-%m-%d')
    ax.xaxis.set_major_formatter(daysFmt)
    fig.autofmt_xdate()

    print(df[['date', 'sec']])

    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    return StreamingResponse(buf, media_type='image/png')
