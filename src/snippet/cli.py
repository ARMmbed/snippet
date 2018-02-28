from snippet import snippet
import argparse


def get_cli_opts():
    parser = argparse.ArgumentParser()
    parser.add_argument('config', help='path to config file')
    return parser


def run():
    parser = get_cli_opts()
    config_path = parser.parse_args().config
    snippet.get_config(config_path)
    snippet.run(config_path)


if __name__ == '__main__':
    run()
