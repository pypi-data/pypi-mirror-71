# YTMonsterClient - An Extensive API Wrapper
An API wrapper for interacting with YTMonster programmatically.

## Some basic use:
```py
from YTMonsterClient import YTMonsterClient

client = YTMonsterClient.YTMonsterClient('exampleuser', 'examplepassword')

print(client.get_like_video_from_exchanges())
print(client.get_channel_from_exchanges())
```

## Installation
```pip install YTMonsterClient```