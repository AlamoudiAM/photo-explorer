from flask import Flask
from flask import jsonify
from flask import request
import subprocess
import os
import signal

app = Flask(__name__)
default_segment = 3

# {"start_time": 0, "file_path": "/media/Big_Buck_Bunny_4K.webm", "m3u8_request_path": "/media/test", "current_requested_segment": 0}
# curl -i -H "Content-Type: application/json" -X POST -d '{"start_time": 0, "file_path": "/media/Big_Buck_Bunny_4K.webm", "m3u8_request_path": "/media/test", "current_requested_segment": 0}' http://127.0.0.1:5000/start-transcode/
# requests.post('http://127.0.0.1:5000/start-transcode/', json = {"start_time": 0, "file_path": "/media/Big_Buck_Bunny_4K.webm", "m3u8_request_path": "/media/test", "current_requested_segment": 0})

@app.route('/start-transcode/', methods=['POST'])
def start_transcode():
    if not request.json:
        abort(400)
    start_time = request.json.get('start_time')
    file_path = request.json.get('file_path')
    m3u8_request_path = request.json.get('m3u8_request_path')
    current_requested_segment = request.json.get('current_requested_segment')

    # return jsonify()
    command_str = """
    ffmpeg \
        -hwaccel vaapi \
        -hwaccel_output_format vaapi \
        -ss {} \
        -i {} \
        -vf 'deinterlace_vaapi,scale_vaapi=w=1280:h=720,hwdownload,format=nv12' \
        -c:v libx264 \
        -b:v 2M -maxrate 2M \
        -preset veryfast \
        -acodec aac \
        -pix_fmt yuv420p \
        -x264opts:0 \
        subme=0:me_range=4:rc_lookahead={}:me=dia:no_chroma_me:8x8dct=0:partitions=none \
        -force_key_frames "expr:gte(t,n_forced*{}.000)" \
        -f segment \
        -segment_list {}/current_transcode.m3u8 \
        -segment_time {} \
        -segment_start_number {} \
        -output_ts_offset {} \
        -vsync 2 \
        {}/%06d.ts
    """.format(
        start_time,
        file_path,
        default_segment,
        default_segment,
        m3u8_request_path,
        default_segment,
        current_requested_segment,
        start_time,
        m3u8_request_path
    )
    command_exec = subprocess.Popen(command_str, shell=True, preexec_fn=os.setsid)
    # command_exec = subprocess.Popen(command_str, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, preexec_fn=os.setsid)

    return jsonify({'pid': command_exec.pid, 'group_pid': os.getpgid(command_exec.pid)}), 201

@app.route('/resume-transcode/<int:group_pid>', methods=['POST'])
def resume_transcode(group_pid):
    os.killpg(group_pid, signal.SIGCONT)
    return jsonify({}), 201

@app.route('/pause-transcode/<int:group_pid>', methods=['POST'])
def pause_transcode(group_pid):
    os.killpg(group_pid, signal.SIGSTOP)
    return jsonify({}), 201

@app.route('/terminate-transcode/<int:group_pid>', methods=['POST'])
def terminate_transcode(group_pid):
    os.killpg(group_pid, signal.SIGTERM)
    return jsonify({}), 201