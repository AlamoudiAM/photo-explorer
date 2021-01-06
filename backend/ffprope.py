import subprocess
import re
from datetime import datetime, date, timedelta
import pytz

cache_folder = '/media/'

def get_video_duration(full_path):
    """ use ffprobe to get video duration"""
    cmd = subprocess.run("ffprobe {}".format(full_path), shell=True, capture_output=True)
    raw_out = cmd.stderr
    out = raw_out.decode('utf-8')
    raw_duration = re.findall('Duration:(.*?),', out)
    if len(raw_duration) > 0:
        duration = raw_duration[0]
        duration = duration.strip()
        return duration
    raise 'cannot determine duration'

def get_segments_list(duration, default_segment):
    """ split video duration into segments """
    
    segments_list = []
    
    # NOTE: currently video length has to be less than 24 hours
    # start_time is 00:00:00.00 and end_time is video duration
    end_time = datetime.today()
    end_time = end_time.replace(hour=duration[0], minute=duration[1], second=duration[2], microsecond=duration[3])
    start_time = datetime.combine(date.today(), datetime.min.time())  + timedelta(seconds=default_segment)
    
    # calculate segments
    while start_time < end_time:
        segments_list.append(default_segment)
        start_time = start_time + timedelta(seconds=default_segment)
    last_segment = default_segment - (start_time - end_time).seconds
    segments_list.append(last_segment)

    return segments_list


def generate_m3m8(segments_list, default_segment):
    # header
    m3m8 = '#EXTM3U\n#EXT-X-VERSION:3\n#EXT-X-MEDIA-SEQUENCE:0\n#EXT-X-ALLOW-CACHE:YES\n#EXT-X-TARGETDURATION:{}\n'.format(default_segment + 1)
    # body
    for index, segment in enumerate(segments_list):
        m3m8 = m3m8 + '#EXTINF:{},\nout{:06d}.ts\n'.format(segment, index)
    # end
    m3m8 = m3m8 + '#EXT-X-ENDLIST\n'
    return m3m8


def export_m3m8_file(m3m8, filename):
    with open('{}{}.m3u8'.format(cache_folder, filename), 'w') as f:
        f.write(m3m8)

def get_m3m8(video_full_path, default_segment, playlist_name):
    duration_str = get_video_duration(video_full_path)
    duration = re.split('[:.]', duration_str)
    duration = list(map(lambda i: int(i), duration))
    segments_list = get_segments_list(duration, default_segment)
    m3m8 = generate_m3m8(segments_list, default_segment)
    export_m3m8_file(m3m8, playlist_name)
    return m3m8


default_segment = 8
m3m8 = get_m3m8("/media/DSC_8939.MOV", default_segment, 'playlist')
print(m3m8)