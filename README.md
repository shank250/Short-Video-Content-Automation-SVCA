# Short Video Content Automation (SVCA)

SVCA is a pipeline for automatically generating and uploading short-form video content to YouTube based on trending topics.

## Pipeline Steps

1. Data Extraction: Fetch trending topics from Google Trends
2. Topic Selection: Choose a trending topic for video creation
3. Image Selection: Retrieve relevant images from Bing search for the chosen topic
4. Script Generation: Use an LLM to create a short script based on the topic and images
5. Video Creation: Utilize MoviePy to produce a 40-second video
6. Upload: Automatically push the generated video to YouTube

## Requirements

- Python 3.x
- Libraries: 
  - pytrends
  - bing_image_downloader
  - transformers (or other LLM library)
  - moviepy
  - google-api-python-client
