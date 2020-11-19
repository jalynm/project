import vlc
import pafy

import urllib.request
import urllib.parse
import re

import time

search_input = input("Search: ") + " audio"
query_string = urllib.parse.urlencode({"search_query" : search_input})
html_content = urllib.request.urlopen("https://www.youtube.com/results?" + query_string)
video_ids = re.findall(r"watch\?v=(\S{11})", html_content.read().decode())
url = "https://www.youtube.com/watch?v=" + video_ids[0]
print(video_ids[0])

video = pafy.new(url)
best = video.getbest()
playurl = best.url

Instance = vlc.Instance()
player = Instance.media_player_new()
Media = Instance.media_new(playurl)
Media.get_mrl()
player.set_media(Media)
player.audio_set_volume(80)
player.play()
