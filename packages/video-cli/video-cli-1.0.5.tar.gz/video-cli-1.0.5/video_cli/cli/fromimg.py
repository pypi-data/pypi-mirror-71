import argparse
import glob
import os.path as osp

import imageio
import imgviz
import tqdm

from ..utils import get_macro_block_size
from ..utils import natural_sort


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("out_file")
    parser.add_argument(
        "-i",
        "--input-files",
        default="*.jpg",
        help="Input patterns like '*.jpg'",
    )
    parser.add_argument("--fps", type=int, default=10)
    parser.add_argument("--nframes", type=int, help="num frames")
    args = parser.parse_args()

    args.input_files = glob.glob(args.input_files)

    # fix low fps for non-GIF videos
    n_times_write = 1
    if osp.splitext(args.out_file)[1] != ".gif" and args.fps < 10:
        n_times_write = 10 // args.fps
        args.fps = 10

    files = natural_sort(args.input_files)
    if args.nframes:
        files = files[:args.nframes]

    writer = None
    for f in tqdm.tqdm(files, ncols=80):
        frame = imageio.imread(f)

        H, W = frame.shape[:2]
        if H % 2 != 0:
            H = (H // 2 + 1) * 2
        if W % 2 != 0:
            W = (W // 2 + 1) * 2
        frame = imgviz.centerize(frame, (H, W))

        if writer is None:
            writer = imageio.get_writer(
                args.out_file,
                fps=args.fps,
                macro_block_size=get_macro_block_size(frame.shape[:2]),
            )
        for _ in range(n_times_write):
            writer.append_data(frame)
