import tempfile

from pathlib import Path
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from amap.download.cli import atlas_parser as amap_parser
import amap.download.cli as atlas_download

from cellfinder.download import models
from cellfinder.download.download import amend_cfg


home = Path.home()
DEFAULT_DOWNLOAD_DIRECTORY = home / ".cellfinder"
temp_dir = tempfile.TemporaryDirectory()
temp_dir_path = Path(temp_dir.name)


def download_directory_parser(parser):
    parser.add_argument(
        "--install-path",
        dest="install_path",
        type=Path,
        default=DEFAULT_DOWNLOAD_DIRECTORY,
        help="The path to install files to.",
    )
    parser.add_argument(
        "--download-path",
        dest="download_path",
        type=Path,
        default=temp_dir_path,
        help="The path to download files into.",
    )
    parser.add_argument(
        "--no-amend-config",
        dest="no_amend_config",
        action="store_true",
        help="Don't amend the config file",
    )
    return parser


def model_parser(parser):
    parser.add_argument(
        "--no-models",
        dest="no_models",
        action="store_true",
        help="Don't download the model",
    )
    parser.add_argument(
        "--model",
        dest="model",
        type=str,
        default="resnet50_tv",
        help="The model to use",
    )
    return parser


def download_parser():
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser = amap_parser(parser)
    parser = model_parser(parser)
    parser = download_directory_parser(parser)
    return parser


def main():
    args = download_parser().parse_args()
    if not args.no_atlas:
        atlas_dir = args.install_path  # / "atlas"
        atlas_download.atlas_download(
            args.atlas, atlas_dir, args.download_path
        )
    if not args.no_models:
        model_path = models.main(args.model, args.install_path)

    if not args.no_amend_config:
        amend_cfg(
            new_atlas_folder=atlas_dir,
            atlas=args.atlas,
            new_model_path=model_path,
        )


if __name__ == "__main__":
    main()
