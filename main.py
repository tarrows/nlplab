import io
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from fastapi import FastAPI, Request
from starlette.responses import StreamingResponse

app = FastAPI()

@app.get("/")
def hello():
    return {"hello": "world"}

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
