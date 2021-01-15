import subprocess
import re
from datetime import datetime, date, timedelta
import pytz
import time
from backend.settings import cache_folder, cache_base_url, default_segment, playlist_name
from django.urls import reverse

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


def get_time(duration):
    """ return start time (00:00:00.000) and end time (duration) as datetime """
    # NOTE: currently video length has to be less than 24 hours
    # start_time is 00:00:00.00 and end_time is video duration
    start_time = datetime.combine(date.today(), datetime.min.time())
    duration_dt = datetime.strptime(duration, '%H:%M:%S.%f')
    end_time = start_time.replace(hour=duration_dt.hour, minute=duration_dt.minute, second=duration_dt.second, microsecond=duration_dt.microsecond)
    return start_time, end_time



def get_segments_list(duration):
    """ split video duration into segments """
    
    segments_list = []
    start_time, end_time = get_time(duration)

    # calculate segments
    while start_time < end_time:
        segments_list.append(default_segment)
        start_time = start_time + timedelta(seconds=default_segment)
    last_segment = default_segment - (start_time - end_time).seconds
    segments_list.append(last_segment)

    return segments_list


# def get_day_as_seconds(dt):
#     """ convert xx:xx:xx.xxx to seconds """
#     hours_as_secs = dt.hour * 60 * 60 
#     minutes_as_secs = dt.minute * 60 
#     seconds = dt.second
#     microsecond_as_secs = dt.microsecond / 1000000
#     return hours_as_secs + minutes_as_secs + seconds + microsecond_as_secs


# def get_keyframe_times(video_full_path, duration):
#     """ generate list of video's keyframes """
#     video_full_path = '/test/Big_Buck_Bunny_4K.webm'
#     _, end_time = get_time(duration)

#     cmd = subprocess.run("""ffprobe -loglevel error -select_streams v:0 -show_entries packet=pts_time,flags -of csv=print_section=0 {} | awk -F',' '/K/ {{print $1}}'""".format(video_full_path), shell=True, capture_output=True)
#     stdout = cmd.stdout
#     stdout = cmd.stdout.decode('utf-8')
#     keyframe_times = stdout.split('\n')
#     # remove last empty item
#     keyframe_times = keyframe_times[:-1]
#     duration_as_seconds = get_day_as_seconds(end_time)
#     keyframe_times.append(duration_as_seconds)
#     return list(map(lambda kt: float(kt), keyframe_times))
    

# def filter_keyframe_times(keyframe_times):
#     """ reduce keyframes using default_segment """
#     duration_as_seconds = keyframe_times[-1]
#     filtered_keyframe_times = []
#     segment_count = default_segment
#     for kt in keyframe_times:
#         if kt > segment_count and kt < duration_as_seconds:
#             filtered_keyframe_times.append(kt)
#             segment_count += default_segment
#     filtered_keyframe_times.append(duration_as_seconds)
#     return filtered_keyframe_times


def generate_m3m8(segments_list, m3u8_request_identifier):
    # header
    m3m8 = '#EXTM3U\n#EXT-X-VERSION:3\n#EXT-X-MEDIA-SEQUENCE:0\n#EXT-X-ALLOW-CACHE:YES\n#EXT-X-TARGETDURATION:{}\n'.format(default_segment)
    # body
    for index, segment in enumerate(segments_list):
        m3m8 = m3m8 + '#EXTINF:{}.0000, nodesc\n{}\n'.format(segment, reverse('media', kwargs={'ts_filename': '{:06d}.ts'.format(index), 'm3u8_request_identifier': m3u8_request_identifier}))
    # end
    m3m8 = m3m8 + '#EXT-X-ENDLIST\n'
    return m3m8


# def generate_m3m8(keyframe_times):
#     # header
#     m3m8 = '#EXTM3U\n#EXT-X-VERSION:3\n#EXT-X-MEDIA-SEQUENCE:0\n#EXT-X-ALLOW-CACHE:YES\n#EXT-X-TARGETDURATION:{}\n'.format(default_segment+2)
#     # body
#     for index, kf in enumerate(keyframe_times):
#         if index == 0:
#             segment_duration = kf
#             print('{} - {}: {}'.format(0, kf, segment_duration))
#         else:
#             segment_duration = kf - keyframe_times[index-1]
#             print('{} - {}: {}'.format(keyframe_times[index-1], kf, segment_duration))

#         m3m8 = m3m8 + '#EXTINF:{:.6f},\n{}{}_{:06d}.ts\n'.format(segment_duration, cache_base_url, playlist_name, index)

#     # end
#     m3m8 = m3m8 + '#EXT-X-ENDLIST\n'
#     return m3m8


def export_m3m8_file(m3m8, m3u8_request_identifier):
    m3u8_request_path = '{}{}'.format(cache_folder, m3u8_request_identifier)
    cmd = subprocess.run("""mkdir -p {}""".format(m3u8_request_path), shell=True, capture_output=True)
    with open('{}/{}.m3u8'.format(m3u8_request_path, playlist_name), 'w') as f:
        f.write(m3m8)

def get_m3m8(video_full_path, m3u8_request_identifier):
    duration = get_video_duration(video_full_path)
    segments_list = get_segments_list(duration)
    # keyframe_times = get_keyframe_times(video_full_path, duration)
    # keyframe_times = filter_keyframe_times(keyframe_times)

    # print(','.join(map(lambda kf: str(kf), keyframe_times)))
    m3m8 = generate_m3m8(segments_list, m3u8_request_identifier)
    # m3m8 = generate_m3m8(keyframe_times)
    # print(m3m8)
    export_m3m8_file(m3m8, m3u8_request_identifier)
    return m3m8
