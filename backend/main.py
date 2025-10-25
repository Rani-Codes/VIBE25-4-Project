from fastapi import FastAPI
import uvicorn

# Local AI - Nursalim
from ai import generate_video

# Local Manum eval - Bardia
from meval import eval_file

app = FastAPI()


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

    filepath: str = generate_video(prompt)
    print("File Path", filepath)

    video_link: str = eval_file(filepath)
    print("Video Link", video_link)

    return {"message": "Prompt received: {prompt}", "video_url": video_link}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
