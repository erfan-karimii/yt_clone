from pytube import YouTube


# url = 'https://www.youtube.com/watch?v=7BXJIjfJCsA'
# url = 'https://www.youtube.com/watch?v=BZP1rYjoBgI'
url = 'https://www.youtube.com/watch?v=QC8iQqtG0hg'
video = YouTube(url)
video.streams.order_by('resolution').desc().first().download()
print('test')
# print(video.__dir__())
print(video.description,video.thumbnail_url,video.rating,video.length,video.keywords)
# print(video.title)

# for stream in video.streams:
#     print(stream.__dir__())
#     break

# x = video.streams.first()
# print(x.resolution)