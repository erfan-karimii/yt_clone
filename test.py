from pytube import YouTube
import time



# url = 'https://www.youtube.com/watch?v=7BXJIjfJCsA'
# url = 'https://www.youtube.com/watch?v=BZP1rYjoBgI'

start = time.time()

url = 'https://www.youtube.com/watch?v=7BXJIjfJCsA'
video = YouTube(url)


# streams = video.streams.filter(file_extension='mp4').order_by('resolution')

# print(video.keywords)

# end = time.time()
# print(end - start)


# for stream in streams:
#     print(stream , stream.filesize_mb,'\n')


# video
# ['_js', '_js_url', '_vid_info', '_watch_html', '_embed_html', '_player_config_args', '_age_restricted', '_fmt_streams', '_initial_data', 
# '_metadata', 'video_id', 'watch_url', 'embed_url', 'stream_monostate', '_author', '_title', '_publish_date', 'use_oauth', 'allow_oauth_cache',
#  '__module__', '__doc__', '__init__', '__repr__', '__eq__', 'watch_html', 'embed_html', 'age_restricted', 'js_url', 'js', 'initial_data',
#  'streaming_data', 'fmt_streams', 'check_availability', 'vid_info', 'bypass_age_gate', 'caption_tracks', 'captions', 'streams',
#  'thumbnail_url', 'publish_date', 'title', 'description', 'rating', 'length', 'views', 'author', 'keywords', 'channel_id', 'channel_url',
#  'metadata', 'register_on_progress_callback', 'register_on_complete_callback', 'from_id', '__dict__', '__weakref__', '__hash__', '__new__',
#  '__str__', '__getattribute__', '__setattr__', '__delattr__', '__lt__', '__le__', '__ne__', '__gt__', '__ge__', '__reduce_ex__',
#  '__reduce__', '__getstate__', '__subclasshook__', '__init_subclass__', '__format__', '__sizeof__', '__dir__', '__class__']

# stream
# ['fmt_streams', 'itag_index', '__module__', '__doc__', '__init__', 'filter', '_filter', 'order_by', 'desc', 'asc', 'get_by_itag',
#  'get_by_resolution', 'get_lowest_resolution', 'get_highest_resolution', 'get_audio_only', 'otf', 'first', 'last', 'count', 'all',
#  '__getitem__', '__len__', '__repr__', '__dict__', '__weakref__', '__abstractmethods__', '_abc_impl', '__slots__', '__iter__',
#  '__contains__', '__reversed__', 'index', '__subclasshook__', '__class_getitem__', '__new__', '__hash__', '__str__', '__getattribute__',
#  '__setattr__', '__delattr__', '__lt__', '__le__', '__eq__', '__ne__', '__gt__', '__ge__', '__reduce_ex__', '__reduce__', '__getstate__',
#  '__init_subclass__', '__format__', '__sizeof__', '__dir__', '__class__']

['file', '_name', 'size', 'content_type', 'charset', 'content_type_extra', '__module__', '__doc__', '__init__', 'temporary_file_path', 'close', '__repr__', '_get_name', '_set_name', 'name', 'DEFAULT_CHUNK_SIZE', '__str__', '__bool__', '__len__', 'chunks', 'multiple_chunks', '__iter__', '__enter__', '__exit__', 'open', 'encoding', 'fileno', 'flush', 'isatty', 'newlines', 'read', 
'readinto', 'readline', 'readlines', 'seek', 'tell', 'truncate', 'write', 'writelines', 'closed', 'readable', 'writable', 'seekable', '__dict__', '__weakref__', '__new__', '__hash__', '__getattribute__', '__setattr__', '__delattr__', '__lt__', '__le__', 
'__eq__', '__ne__', '__gt__', '__ge__', '__reduce_ex__', '__reduce__', '__getstate__', '__subclasshook__', '__init_subclass__', '__format__', '__sizeof__', '__dir__', '__class__']