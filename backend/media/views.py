from django.shortcuts import render, redirect, HttpResponse
from django.http import Http404, StreamingHttpResponse
from ffprope import get_m3m8
from datetime import timedelta, datetime
import m3u8
from cryptography.fernet import Fernet
from backend.settings import fernet_key, cache_folder, cache_base_url, default_segment, playlist_name
import uuid
import re
import subprocess
import os
import signal
import time
from django.utils.encoding import smart_str

f = Fernet(fernet_key)
file_fullpath = f.encrypt(b"/media/Big_Buck_Bunny_4K.webm")
# copy file_fullpath to url
print(file_fullpath)


# * encrypted_file_fullpath: after decrypted it contains file (e.g. original video) full path
# the encrypted_file_fullpath is also used to unequely name playlist and segments file name

def decode(encrypted_file_fullpath):
    file_fullpath = f.decrypt(str.encode(encrypted_file_fullpath))
    return file_fullpath.decode('utf-8')


def view_video(request, encrypted_file_fullpath):
    file_fullpath = decode(encrypted_file_fullpath)
    m3u8_request_identifier = str(uuid.uuid4())
    request.session[m3u8_request_identifier] = {
        "file_fullpath": file_fullpath,
        "created_time": datetime.now().isoformat(),
        "updating_time": datetime.now().isoformat(),
        "pid": None,
        "group_pid": None,
        "starting_segment": None,
        "last_requested_segment": None,
    }
    
    playlist_absolute_uri = cache_base_url + m3u8_request_identifier + '/' + playlist_name + '.m3u8'
    m3m8 = get_m3m8(file_fullpath, m3u8_request_identifier)

    return render(request, 'index.html', context={"playlist_absolute_uri": playlist_absolute_uri, "m3u8_request_identifier": m3u8_request_identifier})

def get_video(request, m3u8_request_identifier, ts_filename):
    m3u8_request_details = request.session.get(m3u8_request_identifier)
    file_fullpath = m3u8_request_details.get('file_fullpath')
    playlist_filename = '{}.m3u8'.format(playlist_name)
    m3u8_request_path = '{}{}//'.format(cache_folder, m3u8_request_identifier)
    playlist_full_path = m3u8_request_path + playlist_filename
    ts_uri = '{}{}/{}'.format(cache_base_url, m3u8_request_identifier, ts_filename)
    ts_path = '{}{}/{}'.format(cache_folder, m3u8_request_identifier, ts_filename)

    duration = 0
    playlist = m3u8.load(playlist_full_path)
    for index, segment in enumerate(playlist.segments):
        if ts_filename in segment.absolute_uri:
            break
        duration += segment.duration

    current_requested_segment = index

    # start new transcoding in case of fresh m3u8 play
    if not m3u8_request_details.get('pid'):
        pid, group_pid = start_transcode(m3u8_request_path, duration, file_fullpath, current_requested_segment)
        m3u8_request_details['pid'] = pid
        m3u8_request_details['group_pid'] = group_pid
        m3u8_request_details['updating_time'] = datetime.now().isoformat()
        m3u8_request_details['starting_segment'] = current_requested_segment
        m3u8_request_details['last_requested_segment'] = current_requested_segment
    else:
        group_pid = m3u8_request_details['group_pid']
        starting_segment = m3u8_request_details['starting_segment']
        last_requested_segment = m3u8_request_details['last_requested_segment']

        # terminate current transcoding and start new transcoding
        if abs(current_requested_segment - last_requested_segment) not in [0, 1] or current_requested_segment < starting_segment:
            try:
                os.killpg(group_pid, signal.SIGTERM) 
            except ProcessLookupError:
                pass
            
            # remove ts files
            cmd = subprocess.run("""rm -f {}/*.ts""".format(m3u8_request_path), shell=True, capture_output=True)
            pid, group_pid = start_transcode(m3u8_request_path, duration, file_fullpath, current_requested_segment)
            m3u8_request_details['pid'] = pid
            m3u8_request_details['group_pid'] = group_pid
            m3u8_request_details['starting_segment'] = current_requested_segment
            m3u8_request_details['created_time'] = datetime.now().isoformat()
        os.killpg(group_pid, signal.SIGCONT) 
        m3u8_request_details['updating_time'] = datetime.now().isoformat()
        m3u8_request_details['last_requested_segment'] = current_requested_segment

    request.session[m3u8_request_identifier] = m3u8_request_details

    # maximum wait for segment to be ready is 10 seconds
    # in Safari segment has to be returned proccessed
    # else segment is skipped
    # therefore wait until segemnt is proccessed
    total_wait = 0
    while total_wait < 10:
        with open('{}/current_transcode.m3u8'.format(m3u8_request_path), 'r') as f:
            if ts_filename in f.read():
                return redirect(ts_uri)
        sleep = 0.5
        time.sleep(sleep)
        total_wait += sleep
    raise Http404
    
def start_transcode(m3u8_request_path, start, file_fullpath, current_requested_segment):
    cmd = subprocess.run("""mkdir -p {}""".format(m3u8_request_path), shell=True, capture_output=True)
    cmd = subprocess.run("""touch {}/current_transcode.m3u8""".format(m3u8_request_path), shell=True, capture_output=True)
    cmd = subprocess.Popen("""
        ffmpeg \
            -ss {} \
            -i {} \
            -vf scale=-2:720 \
            -vcodec libx264 \
            -preset veryfast \
            -acodec aac \
            -pix_fmt yuv420p \
            -x264opts:0 subme=0:me_range=4:rc_lookahead=10:me=dia:no_chroma_me:8x8dct=0:partitions=none \
            -force_key_frames "expr:gte(t,n_forced*{}.000)" \
            -f segment \
            -segment_list {}/current_transcode.m3u8 \
            -segment_time {} \
            -segment_start_number {} \
            -output_ts_offset {} \
            -vsync 2 \
            {}/%06d.ts
    """.format(
        start, 
        file_fullpath,
        default_segment,
        m3u8_request_path,
        default_segment,
        current_requested_segment,
        start,
        m3u8_request_path), shell=True, preexec_fn=os.setsid)
        # m3u8_request_path), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, preexec_fn=os.setsid)

    return cmd.pid, os.getpgid(cmd.pid)
