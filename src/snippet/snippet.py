import glob
import toml
import pystache


def extract_examples(path, examples, replacements, red_flags):
    with open(path, 'r') as fh:
        lines = fh.readlines()

    if not lines:
        return

    current_key = None
    current_block = None
    current_strip = None

    capture = False
    for line_num, line in enumerate(lines):
        if start_flag in line:
            # start capturing code from the next line
            example_name = line.rsplit(':')[-1].strip()
            current_key = (path, line_num, example_name)
            current_block = examples.setdefault(current_key, [])
            current_strip = len(line) - len(line.lstrip())
            if capture:
                raise Exception('Start/end example mismatch - already capturing at %s' % (current_key,))
            capture = True
            continue
        if end_flag in line:
            # stop capturing, and discard empty blocks
            if not capture:
                raise Exception('Start/end example mismatch - not yet capturing at %s' % (current_key,))
            capture = False
            if not current_block:
                examples.pop(current_key)
        if capture:
            # whilst capturing, append code lines to the current block
            if any(line[:current_strip].split(' ')):
                raise Exception('Unexpected dedent whilst capturing %s' % (current_key,))
            code_line = line[current_strip:].rstrip()
            for r_before, r_after in replacements.items():
                code_line = code_line.replace(r_before, r_after)

            for red_flag in red_flags:
                if red_flag in code_line:
                    raise Exception('Red flag %r at %s' % (red_flag, current_key))
            current_block.append(code_line)

    if capture:
        raise Exception('EOF reached whilst still capturing %s' % (current_key,))

    return examples

class Config:
    # IO
    input_glob = 'tests/example/*.py'
    output_template = '```python\n# example: {{name}}{{code}}\n```'  # a mustache template for each file
    output_append = False  # if the output file exists, append to it
    output_dir = None

    # Code block indicators
    start_flag = 'an example'
    end_flag = 'end of example'

    # Hidden block indicators
    start_cloak_flag = 'cloak'
    start_uncloak_flag = 'uncloak'

    # Validation and formatting logic
    replacements = {'self.': ''}  # straightforward replacements
    fail_on_contains = ['assert']  # fail if these strings are found in code blocks
    auto_dedent = True  # keep code left-aligned with the start flag
    fail_on_dedent = True  # fail if code is dedented before reaching the end flag


def get_config(config_path=None, **options):
    new_options = {}
    if config_path:
        with open(config_path) as f:
            new_options.update(toml.load(f))
    new_options.update(options)
    config = Config()
    for k, v in new_options:
        setattr(config, k, v)
    return config


def run(config: Config):

    path_pattern='tests/example/*.py')
    paths_to_load = glob.glob(path_pattern)
    examples = {}
    replacements = {'self.': ''}
    red_flags = {'assert', 'fail'}

    for path in paths_to_load:
        if __file__ in path:
            continue
        extract_examples(path, examples, replacements, red_flags)

    for (path, line_num, example_name), code in examples.items():
        print(5*'#', 'example:', example_name)
        print('\n'.join(code))
        print()


if __name__ == '__main__':
    run()
