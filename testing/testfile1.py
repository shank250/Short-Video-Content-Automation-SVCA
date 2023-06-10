from moviepy.editor import *
from moviepy.video.VideoClip import ImageClip
from moviepy.config import change_settings


change_settings({"IMAGEMAGICK_BINARY": "C:/Program Files/ImageMagick-7.1.1-Q16/magick.exe"})
# openai.api_key = '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'
discarded_trends = []
Exception_counter = 0
final_key = "0"
video_file_name = "finalvideo.mp4"

height, width = 720, 1280
image_path = "C:\\Users\\980ar\\OneDrive\\Pictures\\Documents\\Projects\\SVCA\\image_downloads\\tbfqs.jpg"
white_image = ImageClip(image_path, duration=7)
white_image = white_image.set_duration(6)
white_image = white_image.set_position(("center", "center"))
white_image = white_image.crop(x1 = 720,   x2=1280)
output_path = "file.mp4" 
white_image.write_videofile(output_path, fps=30, codec="libx264", audio=False)


text_clip = VideoFileClip(filename="file.mp4" )
line1 = "hello this is "
line2 = "a sample text"
fontsize = 25
text_clip = TextClip(txt=line1, filename=text_clip, size=None, color='black', bg_color='white', fontsize=fontsize, font='Courier', stroke_color=None, stroke_width=1, method='label', kerning=None, align='center', interline=None, tempfilename=None, temptxt=None, transparent=True, remove_temp=True, print_cmd=True)
text_clip = text_clip.set_position(['center', 'center'])
text_clip = text_clip.set_duration(3)

final_clip = CompositeVideoClip([white_image, text_clip])
text_length_pixels = len(text) * fontsize * 0.6
width_pixels = white_image.w
print(text_length_pixels , "\n", width_pixels)
print()
# print(text_clip.pos)

# text_clip = VideoFileClip(filename="file.mp4" )
# text_clip = text_clip.subclip(3, 6)
# text = "this is another \n  sample text"
# text_clip = TextClip(text, text_clip, fontsize=23, color="black" ,font = 'Arial-Bold', stroke_color = "black", stroke_width = 1)
# text_clip = text_clip.set_position(['center', 'center'])
# text_clip = text_clip.set_duration(3)
# final_clip2 = CompositeVideoClip([white_image, text_clip])

# final_clip = CompositeVideoClip([final_clip1, final_clip2])
final_clip.write_videofile("final_video.mp4", fps=30, codec="libx264", audio=False)


