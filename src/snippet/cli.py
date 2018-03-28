import argparse

import snippet


def get_cli_opts():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=str, help='path to config file')
    return parser


def run_from_cli():
    parser = get_cli_opts()
    config_path = parser.parse_args().config
    snippet.workflow.run(snippet.config.get_config(config_path))


if __name__ == '__main__':
    run_from_cli()
