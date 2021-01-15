[geeqie dependencies list](http://www.geeqie.org/geeqie-install-debian.sh)

[filestash dockerfile](https://github.com/mickael-kerjean/filestash/blob/master/docker/Dockerfile)

[filestash package.json](https://github.com/mickael-kerjean/filestash/blob/master/package.json)

[filestash image transcode](https://github.com/mickael-kerjean/filestash/blob/fd1249c4d68a755ba1e3cedea9a534c5e60e643e/server/plugin/plg_image_light/deps/README.md)

[filestash video transcode](https://github.com/mickael-kerjean/filestash/blob/fd1249c4d68a755ba1e3cedea9a534c5e60e643e/server/plugin/plg_video_transcoder/index.go)

```bash
# ffprobe example
ffprobe -show_packets -read_intervals 0%+15 -print_format json -select_streams flags:K_  Big_Buck_Bunny_4K.webm > packets

# ffprobe get keyframe interval
ffprobe -loglevel error -select_streams v:0 -show_entries packet=pts_time,flags -of csv=print_section=0 Big_Buck_Bunny_4K.webm | awk -F',' '/K/ {print $1}'
# use `awk -F',' '/K/ {print $1; exit}'` to exis on first found frame

# ffprobe: show all parameters for frames/packets
-show_packets
-show_frames
# ffprobe: json output
-print_format json
# ffprobe: show_entries for frames
-show_entries frame=media_type,pkt_pos,key_frame
# ffprobe: show_entries for packet
-show_entries packet=pts_time,flags,pos
# ffprobe: only lookup between 0 and 15 seconds
-read_intervals 0%+15
# ffprobe: only loopup 100 packet after 10 seconds
-read_intervals 10%+#100
# ffprobe: only show video stream
-select_streams 'v'

# use -hls_time 20 -hls_flags to understand #EXT-X-BYTERANGE

# 1883203,29180833,43507003,56845664,81480828
# 3.553,7.82,9.953,12.086,16.27,18.403,22.27,24.403,27.436,31.703,33.836,38.103,39.736,44.003,46.136,48.27,52.103,54.236,58.503,60.47,64.736,67.203,70.32,72.453,75.686,79.936,82.07,84.203,88.62,90.753,94.136,97.936,100.07,102.203,106.27,108.303,112.57,114.703,117.053,121.32,124.486,127.403,129.986,133.403,135.536,139.803,141.936,144.07,148.336,150.47,153.486,157.753,159.886,162.536,165.236,169.836,172.403,176.086,178.22,180.353,184.27,187.02,189.153,192.486,195.87,198.703,201.32,204.236,208.503,210.32,213.27,216.02,220.32,222.453,225.52,228.186,232.786,234.32,238.986,241.12,243.253,246.436,250.036,252.17,255.153,258.07,261.403,265.57,267.236,270.57,274.736,276.87,279.003,282.32,285.786,289.103,291.236,295.503,298.736,301.503,303.603,306.72,309.586,313.853,315.986,318.82,321.603,325.736,328.103,330.236,334.503,336.636,340.87,343.403,346.286,348.42,352.686,354.82,359.086,361.22,363.353,367.62,369.753,374.02,376.153,379.236,381.903,384.87,387.703,391.97,394.103,396.903,400.52,402.653,406.236,408.27,411.486,414.653,418.67,420.52,423.87,426.27,430.82,433.686,435.186,438.103,442.703,444.836,447.603,451.87,454.003,456.136,460.403,462.536,465.286,469.553,472.786,474.92,477.27,481.536,483.67,486.07,490.37,492.82,497.003,499.136,501.27,505.536,507.67,511.936,514.07,516.203,520.47,522.603,526.87,529.003,531.136,535.403,537.536,541.803,543.936,546.07,550.336,552.47,556.736,558.87,561.003,565.27,567.403,571.67,573.803,576.136,580.403,582.536,586.803,588.936,591.07,595.336,597.47,601.736,603.87,606.003,610.27,612.403,616.67,618.736,623.003,625.136,627.27,631.536,633.67,634.55

# my test
ffmpeg \
    -ss 0 \
    -i Big_Buck_Bunny_4K.webm \
    -vf scale=-2:720 \
    -vcodec libx264 \
    -preset veryfast \
    -acodec aac \
    -pix_fmt yuv420p \
    -x264opts:0 subme=0:me_range=4:rc_lookahead=10:me=dia:no_chroma_me:8x8dct=0:partitions=none \
    -force_key_frames 3.553,7.82,9.953,12.086,16.27,18.403,22.27,24.403,27.436,31.703,33.836,38.103,39.736,44.003,46.136,48.27,52.103,54.236,58.503,60.47,64.736,67.203,70.32,72.453,75.686,79.936,82.07,84.203,88.62,90.753,94.136,97.936,100.07,102.203,106.27,108.303,112.57,114.703,117.053,121.32,124.486,127.403,129.986,133.403,135.536,139.803,141.936,144.07,148.336,150.47,153.486,157.753,159.886,162.536,165.236,169.836,172.403,176.086,178.22,180.353,184.27,187.02,189.153,192.486,195.87,198.703,201.32,204.236,208.503,210.32,213.27,216.02,220.32,222.453,225.52,228.186,232.786,234.32,238.986,241.12,243.253,246.436,250.036,252.17,255.153,258.07,261.403,265.57,267.236,270.57,274.736,276.87,279.003,282.32,285.786,289.103,291.236,295.503,298.736,301.503,303.603,306.72,309.586,313.853,315.986,318.82,321.603,325.736,328.103,330.236,334.503,336.636,340.87,343.403,346.286,348.42,352.686,354.82,359.086,361.22,363.353,367.62,369.753,374.02,376.153,379.236,381.903,384.87,387.703,391.97,394.103,396.903,400.52,402.653,406.236,408.27,411.486,414.653,418.67,420.52,423.87,426.27,430.82,433.686,435.186,438.103,442.703,444.836,447.603,451.87,454.003,456.136,460.403,462.536,465.286,469.553,472.786,474.92,477.27,481.536,483.67,486.07,490.37,492.82,497.003,499.136,501.27,505.536,507.67,511.936,514.07,516.203,520.47,522.603,526.87,529.003,531.136,535.403,537.536,541.803,543.936,546.07,550.336,552.47,556.736,558.87,561.003,565.27,567.403,571.67,573.803,576.136,580.403,582.536,586.803,588.936,591.07,595.336,597.47,601.736,603.87,606.003,610.27,612.403,616.67,618.736,623.003,625.136,627.27,631.536,633.67,634.55 \
	-f segment  \
    -segment_list _playlist.m3u8  \
    -segment_times 3.553,7.82,9.953,12.086,16.27,18.403,22.27,24.403,27.436,31.703,33.836,38.103,39.736,44.003,46.136,48.27,52.103,54.236,58.503,60.47,64.736,67.203,70.32,72.453,75.686,79.936,82.07,84.203,88.62,90.753,94.136,97.936,100.07,102.203,106.27,108.303,112.57,114.703,117.053,121.32,124.486,127.403,129.986,133.403,135.536,139.803,141.936,144.07,148.336,150.47,153.486,157.753,159.886,162.536,165.236,169.836,172.403,176.086,178.22,180.353,184.27,187.02,189.153,192.486,195.87,198.703,201.32,204.236,208.503,210.32,213.27,216.02,220.32,222.453,225.52,228.186,232.786,234.32,238.986,241.12,243.253,246.436,250.036,252.17,255.153,258.07,261.403,265.57,267.236,270.57,274.736,276.87,279.003,282.32,285.786,289.103,291.236,295.503,298.736,301.503,303.603,306.72,309.586,313.853,315.986,318.82,321.603,325.736,328.103,330.236,334.503,336.636,340.87,343.403,346.286,348.42,352.686,354.82,359.086,361.22,363.353,367.62,369.753,374.02,376.153,379.236,381.903,384.87,387.703,391.97,394.103,396.903,400.52,402.653,406.236,408.27,411.486,414.653,418.67,420.52,423.87,426.27,430.82,433.686,435.186,438.103,442.703,444.836,447.603,451.87,454.003,456.136,460.403,462.536,465.286,469.553,472.786,474.92,477.27,481.536,483.67,486.07,490.37,492.82,497.003,499.136,501.27,505.536,507.67,511.936,514.07,516.203,520.47,522.603,526.87,529.003,531.136,535.403,537.536,541.803,543.936,546.07,550.336,552.47,556.736,558.87,561.003,565.27,567.403,571.67,573.803,576.136,580.403,582.536,586.803,588.936,591.07,595.336,597.47,601.736,603.87,606.003,610.27,612.403,616.67,618.736,623.003,625.136,627.27,631.536,633.67,634.55 \
    -segment_start_number 0  \
    -segment_time_delta 0.05 \
    -vsync 2 \
    _playlist_%06d.ts
     

# filestash
ffmpeg \
	-timelimit 30 \
    -ss 40.00 \
    -i DSC_8939.MOV \
    -t 10.00 \
    -vf scale=-2:720 \
    -vcodec libx264 \
    -preset veryfast \
    -acodec aac \
    -pix_fmt yuv420p \
    -x264opts:0 subme=0:me_range=4:rc_lookahead=10:me=dia:no_chroma_me:8x8dct=0:partitions=none \
    -force_key_frames "expr:gte(t,n_forced*10.000)" \
	-f segment \
    -segment_list playlist.m3u8 \
    -segment_time 10.00 `# each segment length` \
    -segment_start_number 3 `# segment filename start` \
    -output_ts_offset 40.00 \
    -vsync 2 \
    playlist_%06d.ts
    

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

```python
""" request m3u8 + m3u8_request_identefier """
""" request segment """
""" does m3u8_request_identefier has any sigments ? """
# if no, start new pid
""" is requested_sigment not contunution of prev_requested_sigment """
# kill prev pid -> start new pid
""" is gap between current sigment and latest generated segment more than 3 sigments ? """
# pause pid
# else cont. pid
""" is requested_sigment finished processing and ready to use ? """
# redirect user to sigment
# else return 404

### celery every default_sigment * 3 ###
""" 
in case of user exist video 
# is difference between current_time and last_requested_time more than default_sigment * 3
"""
# pause pid
```

