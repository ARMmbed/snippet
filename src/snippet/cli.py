import argparse
import os
import logging

import snippet


def get_cli_opts():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=str, action='append',
                        help='paths (or globs) to config files')
    parser.add_argument('dir', nargs='?', default=os.getcwd(),
                        help='path to project root, used by any relative paths in loaded configs [cwd]')
    parser.add_argument('-v', '--verbosity', action='count', default=0,
                        help='increase output verbosity')
    return parser


def run_from_cli():
    args = get_cli_opts().parse_args()
    log_level = logging.WARNING - 10 * args.verbosity
    logging.basicConfig(level=log_level)
    snippet.main(snippet.config.get_config(
        config_paths=args.config,
        project_root=args.dir,
    ))


if __name__ == '__main__':
    run_from_cli()
