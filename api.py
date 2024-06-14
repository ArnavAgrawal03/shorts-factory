from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from short import Short

app = FastAPI()

ports = [3000, 5000, 8000]
localhost_origins = [f"http://localhost:{port}" for port in ports]
ip_origins = [f"http://127.0.0.1:{port}" for port in ports]

origins = localhost_origins + ip_origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get(path="/short/title", response_class=FileResponse)
def make_short_from_title(topic: str) -> FileResponse:
    shor = Short(topic=topic, category="title")
    shor.generate_short(randomize=True)
    return FileResponse(shor.video_path)
