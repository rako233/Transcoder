#!/usr/bin/env python3

from pathlib import Path
import argparse
import sys
import os

class Transcoder:
    def __init__(self, src, dst, vfile):
        self.src = src.resolve()
        self.dst = dst.resolve()
        self.file = vfile.resolve()

    def __str__(self):
        return f"\nSRC: {self.src}\nDST: {self.dst}\nFILE: {self.file}\n"

    def _make_relative_path(self):
        return self.file.relative_to(self.src)

    def _build_dir_structure(self):
        rel_path_to_file = self._make_relative_path()

        p = self.dst / rel_path_to_file.parent

        try:
            p.mkdir(mode=0o664, parents=True,  exist_ok=True)
        except  FileExistsError:
            print("directory couldn\'t created because of existing file. Transcoder stopped", file=sys.stderr)
            return False

        return True

    def get_destination_file_path(self):
        rel_path_to_file = self._make_relative_path()
        return self.dst / rel_path_to_file.with_suffix('.mov')

    def run(self):
        if self._build_dir_structure():
            os.system(f'ffmpeg -i {self.file}  -c:v copy -c:a pcm_s24be {self.get_destination_file_path()}')

if  __name__ == '__main__':
    parser = argparse.ArgumentParser(description='A software used by watcher')
    parser.add_argument('-s', '--source',action='store',help='source directory', required=True)
    parser.add_argument('-d', '--destination',action='store',help='destination dir', required=True)
    parser.add_argument('-e', '--event', action='store', help='watcher\'s event',type=int, required=True)
    parser.add_argument('file')
    args = parser.parse_args()

    event = int(args.event)
    if args.event&0x08 == 0:
        print(f'Skipping event {args.event}',file=sys.stdout)
        exit(0)

    videofile = Path(args.file).resolve();
    if (not videofile.exists()) or (not videofile.is_file()):
        print(f'\nvideo file \'{args.file}\' doesn\'t exists or isn\'t a file!\n', file=sys.stderr)
        exit(0)

    if (videofile.suffix not in  ['.mpg','.mkv', '.mov', '.mp4']):
        print(f'\nvideo file \'{args.file}\' doesn\'t have the right suffix', file=sys.stderr)
        exit(0)

    sourcedir = Path(args.source).resolve()
    if (not sourcedir.exists()) or (not sourcedir.is_dir()):
        print(f'\nsource directory \'{args.source}\' doesn\'t exists!\n', file=sys.stderr)
        exit(1)

    destdir = Path(args.destination).resolve()
    if (not destdir.exists()) or (not destdir.is_dir()):
        print(f'\ndestination directory \'{args.destination}\' doesn\'t exists!\n', file=sys.stderr)
        exit(1)

    transcoder = Transcoder(sourcedir, destdir, videofile)
    transcoder.run()


