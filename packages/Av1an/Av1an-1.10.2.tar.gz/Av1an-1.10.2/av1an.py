#!/usr/bin/env python3

import time
import json
import re
from tqdm import tqdm
import sys
import os
import shutil
import atexit
from distutils.spawn import find_executable
from ast import literal_eval
import argparse
import subprocess
from subprocess import PIPE, STDOUT
from pathlib import Path
import cv2
import numpy as np
from scipy import interpolate
from math import isnan
import matplotlib.pyplot as plt
from multiprocessing.managers import BaseManager
import concurrent
import concurrent.futures
from utils.aom_keyframes import find_aom_keyframes, aom_keyframes
from utils.pyscenedetect import pyscene
from utils.utils import  get_brightness, frame_probe, frame_probe_fast, get_cq, man_cq
from utils.utils import reduce_scenes, determine_resources, terminate, extra_splits
from utils.vmaf import read_vmaf_xml, call_vmaf, plot_vmaf
from utils.ffmpeg import split, concatenate_video
from utils.encoder_comp import aom_vpx_encode, rav1e_encode, svt_av1_encode
from utils.boost import boosting

if sys.version_info < (3, 6):
    print('Python 3.6+ required')
    sys.exit()

if sys.platform == 'linux':
    def restore_term():
        os.system("stty sane")
    atexit.register(restore_term)


# Stuff for updating encoded progress in real-time
class MyManager(BaseManager):
    pass


def Manager():
    m = MyManager()
    m.start()
    return m


class Counter():
    def __init__(self, total, initial):
        self.tqdm_bar = tqdm(total=total, initial=initial, dynamic_ncols=True, unit="fr", leave=True, smoothing=0.2)

    def update(self, value):
        self.tqdm_bar.update(value)


MyManager.register('Counter', Counter)


class Av1an:

    def __init__(self):
        """Av1an - Python framework for AV1, VP9, VP8 encodes."""
        self.d = dict()
        self.encoders = {'svt_av1': 'SvtAv1EncApp', 'rav1e': 'rav1e', 'aom': 'aomenc', 'vpx': 'vpxenc'}



    def log(self, info):
        """Default logging function, write to file."""
        with open(self.d.get('logging'), 'a') as log:
            log.write(time.strftime('%X') + ' ' + info)

    def call_cmd(self, cmd, capture_output=False):
        """Calling system shell, if capture_output=True output string will be returned."""
        if capture_output:
            return subprocess.run(cmd, shell=True, stdout=PIPE, stderr=STDOUT).stdout

        with open(self.d.get('logging'), 'a') as log:
            subprocess.run(cmd, shell=True, stdout=log, stderr=log)

    def check_executables(self):
        if not find_executable('ffmpeg'):
            print('No ffmpeg')
            terminate()

        # Check if encoder executable is reachable
        if self.d.get('encoder') in self.encoders:
            enc = self.encoders.get(self.d.get('encoder'))

            if not find_executable(enc):
                print(f'Encoder {enc} not found')
                terminate()
        else:
            print(f'Not valid encoder {self.d.get("encoder")} ')
            terminate()

    def process_inputs(self):
        # Check input file for being valid
        if not self.d.get('input'):
            print('No input file')
            terminate()

        inputs = self.d.get('input')

        if inputs[0].is_dir():
            inputs = [x for x in inputs[0].iterdir() if x.suffix in (".mkv", ".mp4", ".mov", ".avi", ".flv", ".m2ts")]

        valid = np.array([i.exists() for i in inputs])

        if not all(valid):
            print(f'File(s) do not exist: {", ".join([str(inputs[i]) for i in np.where(not valid)[0]])}')
            terminate()

        if len(inputs) > 1:
            self.d['queue'] = inputs
        else:
            self.d['input'] = inputs[0]

    def config(self):
        """Creation and reading of config files with saved settings"""
        cfg = self.d.get('config')
        if cfg:
            if cfg.exists():
                with open(cfg) as f:
                    c: dict = dict(json.load(f))
                    self.d.update(c)

            else:
                with open(cfg, 'w') as f:
                    c = dict()
                    c['video_params'] = self.d.get('video_params')
                    c['encoder'] = self.d.get('encoder')
                    c['ffmpeg'] = self.d.get('ffmpeg')
                    c['audio_params'] = self.d.get('audio_params')
                    json.dump(c, f)

        # Changing pixel format, bit format
        self.d['pix_format'] = f'-strict -1 -pix_fmt {self.d.get("pix_format")}'
        self.d['ffmpeg_pipe'] = f' {self.d.get("ffmpeg")} {self.d.get("pix_format")} -f yuv4mpegpipe - |'

        # Make sure that vmaf calculated after encoding
        if self.d.get('vmaf_target'):
            self.d['vmaf'] = True

        if self.d.get("vmaf_path"):
            if not Path(self.d.get("vmaf_path")).exists():
                print(f'No such model: {Path(self.d.get("vmaf_path")).as_posix()}')
                terminate()

    def arg_parsing(self):
        """Command line parsing"""
        parser = argparse.ArgumentParser()
        parser.add_argument('--mode', '-m', type=int, default=0, help='0 - local, 1 - master, 2 - encoder')

        # Input/Output/Temp
        parser.add_argument('--input', '-i', nargs='+', type=Path, help='Input File')
        parser.add_argument('--temp', type=Path, default=Path('.temp'), help='Set temp folder path')
        parser.add_argument('--output_file', '-o', type=Path, default=None, help='Specify output file')

        # Splitting
        parser.add_argument('--split_method', type=str, default='pyscene', help='Specify splitting method')
        parser.add_argument('--extra_split', '-xs', type=int, default=0, help='Number of frames after which make split')


        # PySceneDetect split
        parser.add_argument('--scenes', '-s', type=str, default=None, help='File location for scenes')
        parser.add_argument('--threshold', '-tr', type=float, default=50, help='PySceneDetect Threshold')

        # Encoding
        parser.add_argument('--passes', '-p', type=int, default=2, help='Specify encoding passes')
        parser.add_argument('--video_params', '-v', type=str, default='', help='encoding settings')
        parser.add_argument('--encoder', '-enc', type=str, default='aom', help='Choosing encoder')
        parser.add_argument('--workers', '-w', type=int, default=0, help='Number of workers')
        parser.add_argument('-cfg', '--config', type=Path, help='Parameters file. Save/Read: '
                                                                'Video, Audio, Encoder, FFmpeg parameteres')

        # FFmpeg params
        parser.add_argument('--ffmpeg', '-ff', type=str, default='', help='FFmpeg commands')
        parser.add_argument('--audio_params', '-a', type=str, default='-c:a copy', help='FFmpeg audio settings')
        parser.add_argument('--pix_format', '-fmt', type=str, default='yuv420p', help='FFmpeg pixel format')

        # Misc
        parser.add_argument('--logging', '-log', type=str, default=None, help='Enable logging')
        parser.add_argument('--resume', '-r', help='Resuming previous session', action='store_true')
        parser.add_argument('--no_check', '-n', help='Do not check encodings', action='store_true')
        parser.add_argument('--keep', help='Keep temporally folder after encode', action='store_true')

        # Boost
        parser.add_argument('--boost', help='Experimental feature, decrease CQ of clip based on brightness.'
                                            'Darker = lower CQ', action='store_true')
        parser.add_argument('--boost_range', default=15, type=int, help='Range/strength of CQ change')
        parser.add_argument('--boost_limit', default=10, type=int, help='CQ limit for boosting')

        # Grain
        # Todo: grain stuf
        # parser.add_argument('--grain', help='Exprimental feature, adds generated grain based on video brightness',
        #                    action='store_true')
        # parser.add_argument('--grain_range')

        # Vmaf
        parser.add_argument('--vmaf', help='Calculating vmaf after encode', action='store_true')
        parser.add_argument('--vmaf_path', type=Path, default=None, help='Path to vmaf models')

        # Target Vmaf
        parser.add_argument('--vmaf_target', type=float, help='Value of Vmaf to target')
        parser.add_argument('--vmaf_steps', type=int, default=4, help='Steps between min and max qp for target vmaf')
        parser.add_argument('--min_cq', type=int, default=25, help='Min cq for target vmaf')
        parser.add_argument('--max_cq', type=int, default=50, help='Max cq for target vmaf')
        parser.add_argument('--vmaf_plots', help='Make plots of probes in temp folder', action='store_true')

        # Server parts
        parser.add_argument('--host', nargs='+', type=str, help='ips of encoders')

        # Store all vars in dictionary
        self.d = vars(parser.parse_args())

    def outputs_filenames(self):
        if self.d.get('output_file'):
            self.d['output_file'] = self.d.get('output_file').with_suffix('.mkv')
        else:
            self.d['output_file'] = Path(f'{self.d.get("input").stem}_av1.mkv')

    def set_logging(self):
        """Setting logging file location"""
        if self.d.get('logging'):
            self.d['logging'] = f"{self.d.get('logging')}.log"
        else:
            self.d['logging'] = self.d.get('temp') / 'log.log'

        self.log(f"Av1an Started\nCommand:\n{' '.join(sys.argv)}\n")

    def setup(self):
        """Creating temporally folders when needed."""
        # Make temporal directories, and remove them if already presented
        if not self.d.get('resume'):
            if self.d.get('temp').is_dir():
                shutil.rmtree(self.d.get('temp'))

        (self.d.get('temp') / 'split').mkdir(parents=True, exist_ok=True)
        (self.d.get('temp') / 'encode').mkdir(exist_ok=True)

        if self.d.get('logging') is os.devnull:
            self.d['logging'] = self.d.get('temp') / 'log.log'

    def extract_audio(self, input_vid: Path):
        """Extracting audio from source, transcoding if needed."""
        audio_params = self.d.get("audio_params")
        audio_file = self.d.get('temp') / 'audio.mkv'
        if audio_file.exists():
            self.log('Reusing Audio File\n')
            return

        # Checking is source have audio track
        check = fr' ffmpeg -y -hide_banner -loglevel error -ss 0 -i "{input_vid}" -t 0 -vn -c:a copy -f null -'
        is_audio_here = len(subprocess.run(check, shell=True, stdout=PIPE, stderr=STDOUT).stdout) == 0

        # If source have audio track - process it
        if is_audio_here:
            self.log(f'Audio processing\n'
                     f'Params: {audio_params}\n')
            cmd = f'ffmpeg -y -hide_banner -loglevel error -i "{input_vid}" -vn ' \
                  f'{audio_params} {audio_file}'
            self.call_cmd(cmd)

    def frame_check(self, source: Path, encoded: Path):
        """Checking is source and encoded video frame count match."""
        try:
            status_file = Path(self.d.get("temp") / 'done.json')
            with status_file.open() as f:
                d = json.load(f)

            if self.d.get("no_check"):
                s1 = frame_probe(source)
                d['done'][source.name] = s1
                with status_file.open('w') as f:
                    json.dump(d, f)
                    return

            s1, s2 = [frame_probe(i) for i in (source, encoded)]

            if s1 == s2:
                d['done'][source.name] = s1
                with status_file.open('w') as f:
                    json.dump(d, f)
            else:
                print(f'Frame Count Differ for Source {source.name}: {s2}/{s1}')
        except IndexError:
            print('Encoding failed, check validity of your encoding settings/commands and start again')
            terminate()
        except Exception as e:
            _, _, exc_tb = sys.exc_info()
            print(f'\nError frame_check: {e}\nAt line: {exc_tb.tb_lineno}\n')

    def get_video_queue(self, source_path: Path):
        """Returns sorted list of all videos that need to be encoded. Big first."""
        queue = [x for x in source_path.iterdir() if x.suffix == '.mkv']

        done_file = self.d.get('temp') / 'done.json'
        if self.d.get('resume') and done_file.exists():
            try:
                with open(done_file) as f:
                    data = json.load(f)
                data = data['done'].keys()
                queue = [x for x in queue if x.name not in data]
            except Exception as e:
                _, _, exc_tb = sys.exc_info()
                print(f'Error at resuming {e}\nAt line {exc_tb.tb_lineno}')

        queue = sorted(queue, key=lambda x: -x.stat().st_size)

        if len(queue) == 0:
            # TODO: this could also be because we're resuming but everything
            # is done.
            print('Error: No files found in .temp/split, probably splitting not working')
            terminate()

        return queue

    def compose_encoding_queue(self, files):
        """Composing encoding queue with split videos."""
        encoder = self.d.get('encoder')
        passes = self.d.get('passes')
        pipe = self.d.get("ffmpeg_pipe")
        params = self.d.get("video_params")
        enc_exe = self.encoders.get(self.d.get('encoder'))
        inputs = [(self.d.get('temp') / "split" / file.name,
                   self.d.get('temp') / "encode" / file.name,
                   file) for file in files]

        if encoder in ('aom', 'vpx'):
            if not params:
                if enc_exe == 'vpxenc':
                    params = '--codec=vp9 --threads=4 --cpu-used=1 --end-usage=q --cq-level=40'
                    self.d['video_params'] = params

                if enc_exe == 'aomenc':
                    params = '--threads=4 --cpu-used=6 --end-usage=q --cq-level=40'
                    self.d['video_params'] = params

            queue = aom_vpx_encode(inputs, enc_exe, passes, pipe, params)

        elif encoder == 'rav1e':
            if not params:
                params = ' --tiles 8 --speed 10 --quantizer 100'
                self.d['video_params'] = params
            queue = rav1e_encode(inputs, passes, pipe, params)

        elif encoder == 'svt_av1':
            if not params:
                print('-w -h -fps is required parameters for svt_av1 encoder')
                terminate()
            queue = svt_av1_encode(inputs, passes, pipe, params)

        self.log(f'Encoding Queue Composed\n'
                 f'Encoder: {self.d.get("encoder").upper()} Queue Size: {len(queue)} Passes: {self.d.get("passes")}\n'
                 f'Params: {self.d.get("video_params")}\n')

        # Catch Error
        if len(queue) == 0:
            print('Error in making command queue')
            terminate()

        return queue

    def target_vmaf(self, source):
        # TODO speed up for vmaf stuff
        # TODO reduce complexity

        if self.d.get('vmaf_steps') < 4:
            print('Target vmaf require more than 3 probes/steps')
            terminate()

        vmaf_target = self.d.get('vmaf_target')
        mincq = self.d.get('min_cq')
        maxcq = self.d.get('max_cq')
        steps = self.d.get('vmaf_steps')
        frames = frame_probe(source)
        probe = source.with_suffix(".mp4")
        plot_probes = self.d.get('vmaf_plots')
        ffmpeg = self.d.get('ffmpeg')

        try:
            # Making 4 fps probing file
            cmd = f' ffmpeg -y -hide_banner -loglevel error -i {source.as_posix()} ' \
                  f'-r 4 -an {ffmpeg} -c:v libx264 -crf 0 {source.with_suffix(".mp4")}'
            self.call_cmd(cmd)

            # Make encoding fork
            q = list(np.unique(np.linspace(mincq, maxcq, num=steps, dtype=int, endpoint=True)))

            # Moving highest cq to first check, for early skips
            # checking highest first, lowers second, for early skips
            q.insert(0, q.pop(-1))

            # Encoding probes, 1 pass, highest speed
            params = " aomenc  -q --passes=1 --threads=8 --end-usage=q --cpu-used=6 --cq-level="
            cmd = [[f'ffmpeg -y -hide_banner -loglevel error -i {probe} {self.d.get("ffmpeg_pipe")}'
                    f'{params}{x} -o {probe.with_name(f"v_{x}{probe.stem}")}.ivf - ',
                    probe, probe.with_name(f'v_{x}{probe.stem}').with_suffix('.ivf'), x] for x in q]

            # Encoding probe and getting vmaf
            ls = []
            pr = []
            for count, i in enumerate(cmd):
                self.call_cmd(i[0])

                v = call_vmaf(i[1], i[2], model=self.d.get('vmaf_path') ,return_file=True)
                _, mean, _, _, _ = read_vmaf_xml(v)

                pr.append(round(mean, 1))
                ls.append((round(mean, 3), i[3]))

                # Early Skip on big CQ
                if count == 0 and round(mean) > vmaf_target:
                    self.log(f"File: {source.stem}, Fr: {frames}\n"
                             f"Probes: {pr}, Early Skip High CQ\n"
                             f"Target CQ: {maxcq}\n\n")
                    return maxcq, f'Target: CQ {maxcq} Vmaf: {round(mean, 2)}\n'

                # Early Skip on small CQ
                if count == 1 and round(mean) < vmaf_target:
                    self.log(f"File: {source.stem}, Fr: {frames}\n"
                             f"Probes: {pr}, Early Skip Low CQ\n"
                             f"Target CQ: {mincq}\n\n")
                    return mincq, f'Target: CQ {mincq} Vmaf: {round(mean, 2)}\n'

            x = [x[1] for x in sorted(ls)]
            y = [float(x[0]) for x in sorted(ls)]

            # Interpolate data
            f = interpolate.interp1d(x, y, kind='cubic')
            xnew = np.linspace(min(x), max(x), max(x) - min(x))

            # Getting value closest to target
            tl = list(zip(xnew, f(xnew)))
            vmaf_target_cq = min(tl, key=lambda x: abs(x[1] - vmaf_target))

            if plot_probes:
                # Saving plot of got data
                plt.plot(x, y, 'x', color='tab:blue')
                plt.plot(xnew, f(xnew), color='tab:blue')
                plt.plot(vmaf_target_cq[0], vmaf_target_cq[1], 'o', color='red')

                for x in range(0, 100):
                    plt.axhline(x, color='grey', linewidth=0.4)
                    plt.axvline(x, color='grey', linewidth=0.3)

                    if x % 5 == 0:
                        plt.axhline(x, color='black', linewidth=0.6)

                plt.xlim(mincq, maxcq)
                vmafs = [int(x[1]) for x in tl if isinstance(x[1], float) and not isnan(x[1])]
                plt.ylim(min(vmafs), max(vmafs) + 1)
                plt.ylabel('VMAF')
                plt.xlabel('CQ')
                plt.title(f'Chunk: {probe.stem}, Frames: {frames}')
                plt.tight_layout()
                temp = self.d.get('temp') / probe.stem
                plt.savefig(temp, dpi=300)
                plt.close()

            self.log(f"File: {source.stem}, Fr: {frames}\n"
                     f"Probes: {sorted(pr)}\n"
                     f"Target CQ: {round(vmaf_target_cq[0])}\n\n")

            return int(vmaf_target_cq[0]), f'Target: CQ {int(vmaf_target_cq[0])} Vmaf: {round(float(vmaf_target_cq[1]), 2)}\n'

        except Exception as e:
            _, _, exc_tb = sys.exc_info()
            print(f'Error in vmaf_target {e} \nAt line {exc_tb.tb_lineno}')
            terminate()

    def encode(self, commands):
        """Single encoder command queue and logging output."""
        counter = commands[1]
        commands = commands[0]
        encoder = self.d.get('encoder')
        passes = self.d.get('passes')
        boost = self.d.get('boost')
        # Passing encoding params to ffmpeg for encoding.
        # Replace ffmpeg with aom because ffmpeg aom doesn't work with parameters properly.
        try:
            st_time = time.time()
            source, target = Path(commands[-1][0]), Path(commands[-1][1])
            frame_probe_source = frame_probe(source)

            # Target Vmaf Mode
            if self.d.get('vmaf_target'):
                tg_cq, tg_vf = self.target_vmaf(source)

                cm1 = man_cq(commands[0], tg_cq)

                if passes == 2:
                    cm2 = man_cq(commands[1], tg_cq)
                    commands = (cm1, cm2) + commands[2:]
                else:
                    commands = cm1 + commands[1:]

            else:
                tg_vf = ''

            # Boost
            if boost:
                bl = self.d.get('boost_limit')
                br = self.d.get('boost_range')
                brightness = get_brightness(source.absolute().as_posix())
                try:
                    com0, cq = boosting(commands[0], brightness, bl, br )

                    if passes == 2:
                        com1, _ = boosting(commands[1], brightness, bl, br, new_cq=cq)
                        commands = (com0, com1) + commands[2:]
                    else:
                        commands = com0 + commands[1:]

                except Exception as e:
                    _, _, exc_tb = sys.exc_info()
                    print(f'Error in encoding loop {e}\nAt line {exc_tb.tb_lineno}')

                boost = f'Avg brightness: {br}\nAdjusted CQ: {cq}\n'
            else:
                boost = ''

            self.log(f'Enc: {source.name}, {frame_probe_source} fr\n{tg_vf}{boost}\n')

            # Queue execution
            for i in commands[:-1]:
                f, e = i.split('|')
                f = " ffmpeg -y -hide_banner -loglevel error " + f
                f, e = f.split(), e.split()
                try:
                    frame = 0

                    ffmpeg_pipe = subprocess.Popen(f, stdout=PIPE, stderr=STDOUT)
                    pipe = subprocess.Popen(e, stdin=ffmpeg_pipe.stdout, stdout=PIPE,
                                            stderr=STDOUT,
                                            universal_newlines=True)
                    if encoder in ('aom', 'vpx'):
                        while True:
                            line = pipe.stdout.readline().strip()
                            if len(line) == 0 and pipe.poll() is not None:
                                break
                            if 'Pass 2/2' in line or 'Pass 1/1' in line:
                                match = re.search(r"frame.*?\/([^ ]+?) ", line)
                                if match:
                                    new = int(match.group(1))
                                    if new > frame:
                                        counter.update(new - frame)
                                        frame = new

                    elif encoder == 'rav1e':
                        while True:
                            line = pipe.stdout.readline().strip()
                            if len(line) == 0 and pipe.poll() is not None:
                                break
                            match = re.search(r"encoded.*? ([^ ]+?) ", line)
                            if match:
                                new = int(match.group(1))
                                if new > frame:
                                    counter.update(new - frame)
                                    frame = new

                    elif encoder == 'svt_av1':
                        while True:
                            line = pipe.stdout.readline().strip()
                            if len(line) == 0 and pipe.poll() is not None:
                                break
                        counter.update(frame_probe_source // passes)

                except Exception as e:
                    _, _, exc_tb = sys.exc_info()
                    print(f'Error at encode {e}\nAt line {exc_tb.tb_lineno}')

            self.frame_check(source, target)

            frame_probe_fr = frame_probe(target)

            enc_time = round(time.time() - st_time, 2)

            self.log(f'Done: {source.name} Fr: {frame_probe_fr}\n'
                     f'Fps: {round(frame_probe_fr / enc_time, 4)} Time: {enc_time} sec.\n\n')
        except Exception as e:
            _, _, exc_tb = sys.exc_info()
            print(f'Error in encoding loop {e}\nAt line {exc_tb.tb_lineno}')

    def encoding_loop(self, commands):
        """Creating process pool for encoders, creating progress bar."""
        try:
            enc_path = self.d.get('temp') / 'split'
            done_path = self.d.get('temp') / 'done.json'

            if self.d.get('resume') and done_path.exists():
                self.log('Resuming...\n')

                with open(done_path) as f:
                    data = json.load(f)

                total = data['total']
                done = len(data['done'])
                initial = sum(data['done'].values())

                self.log(f'Resumed with {done} encoded clips done\n\n')
            else:
                initial = 0
                total = frame_probe_fast(self.d.get('input'))
                d = {'total': total, 'done': {}}
                with open(done_path, 'w') as f:
                    json.dump(d, f)

            clips = len([x for x in enc_path.iterdir() if x.suffix == ".mkv"])
            w = min(self.d.get('workers'), clips)

            print(f'\rQueue: {clips} Workers: {w} Passes: {self.d.get("passes")}\n'
                  f'Params: {self.d.get("video_params").strip()}')

            with concurrent.futures.ThreadPoolExecutor(max_workers=self.d.get('workers')) as executor:
                counter = Manager().Counter(total, initial)
                future_cmd = {executor.submit(self.encode, (cmd, counter)): cmd for cmd in commands}
                for future in concurrent.futures.as_completed(future_cmd):
                    future_cmd[future]
                    try:
                        future.result()
                    except Exception as exc:
                        print(f'Encoding error: {exc}')
                        terminate()
        except KeyboardInterrupt:
            terminate()

    def split_routine(self):

        if self.d.get('scenes') == '0':
            self.log('Skipping scene detection\n')
            return []

        split_method = self.d.get('split_method')
        sc = []

        scenes = self.d.get('scenes')
        video = self.d.get('input')

        if scenes:
            scenes = Path(scenes)
            if scenes.exists():
                # Read stats from CSV file opened in read mode:
                with scenes.open() as stats_file:
                    stats = literal_eval(stats_file.read().strip())
                    self.log('Using Saved Scenes\n')
                    return stats

        # Splitting using PySceneDetect
        if split_method == 'pyscene':
            queue_fix = not self.d.get('queue')
            threshold = self.d.get("threshold")
            self.log(f'Starting scene detection Threshold: {threshold}\n')
            try:
                sc = pyscene(video, threshold, progress_show=queue_fix )
            except Exception as e:
                self.log(f'Error in PySceneDetect: {e}\n')
                print(f'Error in PySceneDetect{e}\n')
                terminate()

        # Splitting based on aom keyframe placement
        elif split_method == 'aom_keyframes':
            try:
                video: Path = self.d.get("input")
                stat_file = self.d.get('temp') / 'keyframes.log'
                sc = aom_keyframes(video, stat_file)
            except:
                self.log('Error in aom_keyframes')
                print('Error in aom_keyframes')
                terminate()
        else:
            print(f'No valid split option: {split_method}\nValid options: "pyscene", "aom_keyframes"')
            terminate()



        self.log(f'Found scenes: {len(sc)}\n')

        # Fix for windows character limit
        if sys.platform != 'linux':
            if len(sc) > 600:
                sc = reduce_scenes(sc)

        # Write scenes to file

        if scenes:
            Path(scenes).write_text(','.join([str(x) for x in sc]))

        return sc

    def setup_routine(self):
        """
        All pre encoding routine.
        Scene detection, splitting, audio extraction
        """
        if self.d.get('resume') and (self.d.get('temp') / 'done.json').exists():
            self.set_logging()

        else:
            self.setup()
            self.set_logging()

            # Splitting video and sorting big-first

            framenums = self.split_routine()
            xs = self.d.get('extra_split')
            if xs:
                framenums = extra_splits(self.d.get('input'), framenums, xs )
                self.log(f'Applying extra splits\nSplit distance: {xs}\nNew splits:{len(framenums)}\n')

            split( self.d.get('input'),self.d.get('temp'),framenums)

            # Extracting audio
            self.extract_audio(self.d.get('input'))

    def video_encoding(self):
        """Encoding video on local machine."""
        self.outputs_filenames()
        self.setup_routine()

        files = self.get_video_queue(self.d.get('temp') / 'split')

        # Make encode queue
        commands = self.compose_encoding_queue(files)

        self.d['workers'] = determine_resources(self.d.get('encoder'), self.d.get('workers'))

        self.encoding_loop(commands)

        try:
            self.log('Concatenating\n')
            concatenate_video(self.d.get("temp"), self.d.get("output_file"), keep=self.d.get('keep'))

        except Exception as e:
            _, _, exc_tb = sys.exc_info()
            print(f'Concatenation failed, FFmpeg error\nAt line: {exc_tb.tb_lineno}\nError:{str(concat)}')
            self.log(f'Concatenation failed, aborting, error: {e}\n')
            terminate()

        if self.d.get("vmaf"):
            plot_vmaf(self.d.get('input'), self.d.get('output_file'), model=self.d.get('vmaf_path'))

    def main_queue(self):
        # Video Mode. Encoding on local machine
        tm = time.time()
        if self.d.get('queue'):
            for file in self.d.get('queue'):
                tm = time.time()
                self.d['input'] = file
                print(f'Encoding: {file}')
                self.d['output_file'] = None
                self.video_encoding()
                print(f'Finished: {round(time.time() - tm, 1)}s\n')
        else:
            self.video_encoding()
            print(f'Finished: {round(time.time() - tm, 1)}s')

    def main_thread(self):
        """Main."""
        self.arg_parsing()

        # Read/Set parameters
        self.config()

        # Check all executables
        self.check_executables()

        self.process_inputs()
        self.main_queue()


def main():
    # Main thread
    try:
        Av1an().main_thread()
    except KeyboardInterrupt:
        print('Encoding stopped')
        sys.exit()


if __name__ == '__main__':
    main()
