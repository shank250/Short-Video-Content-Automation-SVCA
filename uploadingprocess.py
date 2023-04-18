from youtube_upload.client import YoutubeUploader
import os

current_dir = os.getcwd()
secret_file_location = current_dir + r"\api keys and other files\client_secret_shashank21005.json"
file_path = current_dir + r"\cut_video_processed10.mp4"


uploader = YoutubeUploader(secrets_file_path = secret_file_location)
uploader.authenticate()
options = {
    "title" : "Example title", # The video title
    "description" : "Example description", # The video description
    "tags" : ["tag1", "tag2", "tag3"],
    "categoryId" : "22",
    "privacyStatus" : "private", # Video privacy. Can either be "public", "private", or "unlisted"
    "kids" : False, # Specifies if the Video if for kids or not. Defaults to False.
    "thumbnailLink" : "https://cdn.havecamerawilltravel.com/photographer/files/2020/01/youtube-logo-new-1068x510.jpg" # Optional. Specifies video thumbnail.
}

# upload video
uploader.upload(file_path, options)
uploader.close() 