[geeqie dependencies list](http://www.geeqie.org/geeqie-install-debian.sh)

[filestash dockerfile](https://github.com/mickael-kerjean/filestash/blob/master/docker/Dockerfile)

[filestash package.json](https://github.com/mickael-kerjean/filestash/blob/master/package.json)

[filestash image transcode](https://github.com/mickael-kerjean/filestash/blob/fd1249c4d68a755ba1e3cedea9a534c5e60e643e/server/plugin/plg_image_light/deps/README.md)

[filestash video transcode](https://github.com/mickael-kerjean/filestash/blob/fd1249c4d68a755ba1e3cedea9a534c5e60e643e/server/plugin/plg_video_transcoder/index.go)

```bash
ffmpeg \
	`# -timelimit 15` \
    `#-ss 00:00:00.00` \
    -i DSC_8939.MOV \
    `#-t 00:00:45.00` \
    -vf scale=-2:720 \
    -vcodec libx264 \
    -preset veryfast \
    -acodec aac \
    -pix_fmt yuv420p \
    -x264opts:0 subme=0:me_range=4:rc_lookahead=10:me=dia:no_chroma_me:8x8dct=0:partitions=none \
    -force_key_frames "expr:gte(t,n_forced*8.000)" \
	-f segment \
    -segment_list playlist.m3u8 \
    -segment_time 8 `# each segment length` \
    `#-segment_start_number 5` `# segment filename start` \
    `-output_ts_offset 00:10:10.000` \
    -vsync 2 \
    out%06d.ts
    

```

google: python video transcode

google: nginx video transcoder

google: handbreak cli

google: transcode tcp

google: VLC cli tcp transcode

[Extracting extension from filename in Python](https://stackoverflow.com/questions/541390/extracting-extension-from-filename-in-python)

google: http on fly transcoding tool

[dash.js](https://github.com/Dash-Industry-Forum/dash.js)

[shaka-player](https://github.com/google/shaka-player)

ffmpeg http

ffmpeg Nginx http

vlc transcode on demand

[a way for generating vlc commands](https://www.youtube.com/watch?v=_3_KSju8KNg)

[ffmpeg-libav-tutorial](https://github.com/leandromoreira/ffmpeg-libav-tutorial)

[ffmpeg-python](https://github.com/kkroening/ffmpeg-python)

[video-transcoding-scripts](https://github.com/donmelton/video-transcoding-scripts)

handbreak trancode cli

[FFmpeg Protocols HTTP](https://ffmpeg.org/ffmpeg-protocols.html#http)

[FFmpeg Formats HSL](https://ffmpeg.org/ffmpeg-formats.html#hls-2)

[FFmpeg Formats Segment](https://ffmpeg.org/ffmpeg-formats.html#segment)

```bash
ffmpeg -i Big_Bhls_timeuck_Bunny_4K.webm -c:v h264 -flags +cgop -g 30 - 1 out.m3u8
```

[Using NGINX Open Source for Video Streaming and Storage](https://www.youtube.com/watch?v=Js1OlvRNsdI)

```
ffmpeg -re -i Big_Buck_Bunny_4K.webm -vcodec libx264 -loop -1 -c:a aac -b:a 160k -ar 44100 -strict -2 -f flv rtmp:photo-explorer-nginx/live/bbb
```

[Node-Media-Server (hls)](https://github.com/illuspas/Node-Media-Server#readme)

[python-ffmpeg-video-streaming (hls)](https://github.com/aminyazdanpanah/python-ffmpeg-video-streaming)

vlc hls stream

[django-video-transcoding](https://github.com/just-work/django-video-transcoding)

[HTTP_Live_Streaming#Servers](https://en.wikipedia.org/wiki/HTTP_Live_Streaming#Servers)

[Python - Django: Streaming video/mp4 file using HttpResponse](https://stackoverflow.com/questions/33208849/python-django-streaming-video-mp4-file-using-httpresponse)

[Stream file from remote url to Django view response](https://stackoverflow.com/questions/43951485/stream-file-from-remote-url-to-django-view-response)