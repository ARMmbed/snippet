import traceback
import logging

from snippet.config import Config
from snippet import file_wrangler


def extract_examples(config: Config, lines, path):
    """Finds examples!"""
    current_key = None
    current_block = None
    current_strip = None
    capture = False
    examples = {}

    for line_num, line in enumerate(lines):

        if config.start_flag in line:
            # start capturing code from the next line
            example_name = line.rsplit(':')[-1].strip()
            current_key = (path, line_num, example_name)
            current_block = []
            examples[current_key] = current_block
            current_strip = len(line) - len(line.lstrip())
            if capture:
                raise Exception('Start/end example mismatch - already capturing at %s' % (current_key,))
            capture = True
            continue

        if config.end_flag in line:
            # stop capturing, and discard empty blocks
            if not capture:
                raise Exception('Start/end example mismatch - not yet capturing at %s' % (current_key,))
            capture = False
            if not current_block:
                examples.pop(current_key)

        if capture:
            # whilst capturing, append code lines to the current block
            if config.fail_on_dedent and any(line[:current_strip].split(' ')):
                raise Exception('Unexpected dedent whilst capturing %s' % (current_key,))
            code_line = line[current_strip:].rstrip()
            for r_before, r_after in config.replacements.items():
                code_line = code_line.replace(r_before, r_after)
            for trigger in config.fail_on_contains:
                if trigger in code_line:
                    raise Exception('Unexpected phrase %r at %s' % (trigger, current_key))
            # add this line of code to the example block
            current_block.append(code_line)

    if capture:
        raise Exception('EOF reached whilst still capturing %s' % (current_key,))

    return examples


def run(config: Config):
    if config.log_level:
        logging.basicConfig(level=config.log_level)

    examples = {}
    failures = []
    for path in file_wrangler.find_files(config):
        try:
            lines = file_wrangler.load_file_lines(path)
        except Exception as e:
            if config.stop_on_first_failure:
                raise
            failures.append((path, traceback.format_exc()))
            continue
        try:
            new_examples = extract_examples(config, lines, path)
        except Exception as e:
            if config.stop_on_first_failure:
                raise
            failures.append((path, traceback.format_exc()))
            continue

        # store the new examples for analysis
        examples.update(new_examples)

    unique_example_names = dict()
    for (path, line_num, example_name), code_lines in examples.items():
        existing = unique_example_names.get(example_name)
        if existing:
            raise Exception('Example with duplicate name %s %s matches %s' % (path, line_num, existing))
        else:
            unique_example_names[example_name] = (path, line_num, example_name)

    for (path, line_num, example_name), code_lines in examples.items():
        example_block = '\n'.join(code_lines)
        logging.info('example: %s', example_name)
        logging.debug('example code: %s', example_block)

        try:
            file_wrangler.write_example(config, example_name, example_block)
        except Exception as e:
            if config.stop_on_first_failure:
                raise
            failures.append((path, traceback.format_exc()))
            continue


if __name__ == '__main__':
    run()
