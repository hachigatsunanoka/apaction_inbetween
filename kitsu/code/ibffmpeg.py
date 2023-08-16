import subprocess
import json

FFMPEG = 'I:/IB-PIPELINE/distro/ffmpeg/ffmpeg-master-latest-win64-gpl/bin/ffmpeg.exe'
FFPROBE = 'I:/IB-PIPELINE/distro/ffmpeg/ffmpeg-master-latest-win64-gpl/bin/ffprobe.exe'


def create_thumbnail(input_file, output, width=640, height=360):

    cmd = [FFMPEG, '-i', input_file, '-vf', 'thumbnail,scale=%d:%d' %
           (width, height), '-frames:v', '1', output]

    subprocess.run(cmd)


def get_duration(input_file):

    cmd = [FFPROBE,
           '-v',
           'error',
           '-select_streams',
           'v:0',
           '-show_entries',
           'stream=nb_frames',
           '-of',
           'default=nokey=1:noprint_wrappers=1',
           input_file]

    p = subprocess.run(cmd, stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE).stdout

    frame_count = int(p)
    return frame_count


# def get_duration(input_file):
#     result = subprocess.run(['ffmpeg', '-i', input_file, '-map', '0:v:0', '-c',
#                             'copy', '-f', 'null', '-'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#     output = result.stderr.decode('utf-8')
#     frame_count = int(output.split('frame=')[-1].split('fps=')[0].strip())
#     return frame_count
