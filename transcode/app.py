from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

    """
    ffmpeg \
        -vaapi_device /dev/dri/renderD128 \
        -ss 0 \
        -i Big_Buck_Bunny_4K.webm \
        -vf 'hwupload,scale_vaapi=w=1280:h=720:format=nv12' \
        -vcodec h264_vaapi \
        -c:v h264_vaapi -b:v 2M -maxrate 2M \
        -preset veryfast \
        -acodec aac \
        -pix_fmt yuv420p \
        -x264opts:0 \
        subme=0:me_range=4:rc_lookahead=10:me=dia:no_chroma_me:8x8dct=0:partitions=none \
        -force_key_frames "expr:gte(t,n_forced*10.000)" \
        -f segment \
        -segment_list current_transcode.m3u8 \
        -segment_time 10 \
        -segment_start_number 0 \
        -output_ts_offset 0 \
        -vsync 2 \
        %06d.ts
    """

    """
    ffmpeg \
        -hwaccel vaapi \
        -hwaccel_output_format vaapi \
        -i Big_Buck_Bunny_4K.webm \
        -vf 'deinterlace_vaapi,scale_vaapi=w=1280:h=720,hwdownload,format=nv12' \
        -c:v libx264 \
        -b:v 2M -maxrate 2M \
        -preset veryfast \
        -acodec aac \
        -pix_fmt yuv420p \
        -x264opts:0 \
        subme=0:me_range=4:rc_lookahead=10:me=dia:no_chroma_me:8x8dct=0:partitions=none \
        -force_key_frames "expr:gte(t,n_forced*10.000)" \
        -f segment \
        -segment_list current_transcode.m3u8 \
        -segment_time 10 \
        -segment_start_number 0 \
        -output_ts_offset 0 \
        -vsync 2 \
        %06d.ts
    """