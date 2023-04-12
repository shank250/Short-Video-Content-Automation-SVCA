from bing_image_downloader import downloader
query_string=input("Enter a word : ")
num = int(input("No. of images : "))
downloader.download(query_string, limit=num,  output_dir='image downloads', adult_filter_off=True, force_replace=False, timeout=60, verbose=True)

