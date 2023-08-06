# youtube_library

This library allow easy work with youtube api on python. allows you to use the following handlers:
    
    - Get channel info by channel name or channel id
    - Work with playlists and and filtering them
    - Work with playlistsItems and and filtering them
    
# ---Channel info---
### Get channel info by channel name

```python
from youtubelight.channel_info_handler import СhannelInfoHandler

API_KEY = 'some_key'
obj = СhannelInfoHandler(API_KEY)
obj.get_channel_info_by_name('channel_name')
```

### Get channel info by channel id

```python
from youtubelight.channel_info_handler import СhannelInfoHandler

API_KEY = 'some_key'
obj = СhannelInfoHandler(API_KEY)
obj.get_channel_info_by_id('channel_id')
```

### Get channel info by channel selections

```python
from youtubelight.channel_info_handler import СhannelInfoHandler

API_KEY = 'some_key'
obj = СhannelInfoHandler(API_KEY)
obj.get_channel_sections('channel_id')
```

All methods above have an optional parameter: default_param='snippet,contentDetails,statistics'. More information you can find here: https://developers.google.com/youtube/v3/docs

# ---PlayList or PlayListItems--- 

### Get playlist by channel id

```python
from youtubelight.playlist_handler import PlaylistHandler

API_KEY = 'some_key'
obj = PlaylistHandler(API_KEY)
obj.get_play_list(channel_id, itm_result) # default itm_result=50
```

### Get next page playlist
```python
from youtubelight.playlist_handler import PlaylistHandler

API_KEY = 'some_key'
obj = PlaylistHandler(API_KEY)
obj.get_play_list(channel_id, itm_result) # default itm_result=50
obj.playlist_next_page()
```

### Get all pages playlist
```python
from youtubelight.playlist_handler import PlaylistHandler

API_KEY = 'some_key'
obj = PlaylistHandler(API_KEY)
obj.get_all_playlists(channel_id)
```

### Filter playlist by such parameters: title, description, publishedAt.
```python
from youtubelight.playlist_handler import PlaylistHandler

API_KEY = 'some_key'
obj = PlaylistHandler(API_KEY)
result = obj.get_play_list(channel_id)
# if use method get all playlists
    obj.filter_playlist(result['items'], title, description, date or date_lt or date_lte or date_gt or date_gte)
# else:
    obj.filter_playlist(result['content']['items'], title, description, date or date_lt or date_lte or date_gt or date_gte) # title, description, date optional parameters. Date must by date obj with tz.
```

### Get PlaylistItm by Playlist id

```python
from youtubelight.playlist_handler import PlaylistItemHandler

API_KEY = 'some_key'    
obj = PlaylistItemHandler(API_KEY)
obj.get_play_list_itm(channel_id, itm_result) # default itm_result=50
```

### Get next page PlaylistItm
```python
from youtubelight.playlist_handler import PlaylistItemHandler

API_KEY = 'some_key'
obj = PlaylistItemHandler(API_KEY)
obj.get_play_list_itm(channel_id, itm_result) # default itm_result=50
obj.list_itm_next_page()
```

### Get all pages playlist
```python
from youtubelight.playlist_handler import PlaylistItemHandler

API_KEY = 'some_key'
obj = PlaylistItemHandler(API_KEY)
obj.get_all_playlist_itm(channel_id)
```

### Filter playlistitm by such parameters: title, description, publishedAt.
```python
from youtubelight.playlist_handler import PlaylistItemHandler

API_KEY = 'some_key'
obj = PlaylistItemHandler(API_KEY)
result = obj.get_play_list_itm(channel_id)
# if use method get all playlists
    obj.filter_playlist_itm(result['items'], title, description, date or date_lt or date_lte or date_gt or date_gte)
# else:
    obj.filter_playlist_itm(result['content']['items'], title, description, date or date_lt or date_lte or date_gt or date_gte) # title, description, date optional parameters. Date must by date obj with tz.
```

All methods above have an optional parameter: default_param='snippet,contentDetails,statistics'. More information you can find here: https://developers.google.com/youtube/v3/docs

# ---Video info---

### Get video info by video_id
```python
from youtubelight.video_handler import VideoStatisticHandler

API_KEY = 'some_key'
obj = VideoStatisticHandler(API_KEY)
obj.get_video_info(video_id or video_id,video_id or [video_id, video_id])
```
Method above have an optional parameter: default_param='snippet,contentDetails,statistics'. More information you can find here: https://developers.google.com/youtube/v3/docs

# ---Comment info---

### Get comment by video id
```python
from youtubelight.comment_handler import CommentHandler

API_KEY = 'some_key'
obj = CommentHandler(API_KEY)
obj.get_video_comment(video_id)
```
### Get comemnt next page
```python
from youtubelight.comment_handler import CommentHandler

API_KEY = 'some_key'
obj = CommentHandler(API_KEY)
obj.get_video_comment(video_id)
obj.comments_next_page()
```

### Filter comment by textOriginal field
```python
from youtubelight.comment_handler import CommentHandler

API_KEY = 'some_key'
obj = CommentHandler(API_KEY)
res = obj.get_video_comment(video_id)
obj.filter_comment(res.get('content'), string_for_search)
```

Method above have an optional parameter: default_param='snippet,replies'. More information you can find here: https://developers.google.com/youtube/v3/docs.
Hundler for comments does not have a get_all_comment_by_video_id method, because a video can have many 5k comments or more, and this can affect the performance of your application.