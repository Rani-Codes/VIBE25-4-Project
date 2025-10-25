from fastapi import FastAPI
import uvicorn
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

# Local AI - Nursalim
from ai import generate_video

# Local Manum eval - Bardia
from meval import eval_file

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/media", StaticFiles(directory="media"), name="media")


@app.get("/")
async def root():
    return {"message": "Hello World"}


"""Call the route

    http://localhost:8000/prompt?prompt=your_text_here

   {
     "message": "Prompt received: hello",
     "video_url": "http://localhost:5000/video/123"
   }

"""
@app.get("/prompt")
async def prompt_endpoint(prompt: str):
    if prompt == "test":
        # Overwrite!!
        video_link = "http://127.0.0.1:8000/media/videos/quadratic_manim/480p15/QuadraticEquation.mp4"

        return {"message": "Prompt received: {prompt}", "video_url": video_link}

    print("Prompt", prompt)

    filepath: str = generate_video(prompt)
    print("file path", filepath)

    video_link: str = eval_file(filepath)
    print("video link", video_link)

    return {"message": "Prompt received: {prompt}", "video_url": video_link}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
