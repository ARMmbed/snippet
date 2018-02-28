from snippet.config import Config


def extract_snippets(config: Config, lines, path):
    """Finds snippets in lines of text"""
    current_key = None
    current_block = None
    current_strip = None
    capture = False
    examples = {}

    for line_num, line in enumerate(lines or []):

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
            clean_line = line[current_strip:].rstrip()
            for r_before, r_after in config.replacements.items():
                clean_line = clean_line.replace(r_before, r_after)
            for trigger in config.fail_on_contains:
                if trigger in clean_line:
                    raise Exception('Unexpected phrase %r at %s' % (trigger, current_key))
            # add this line of code to the example block
            current_block.append(clean_line)

    if capture:
        raise Exception('EOF reached whilst still capturing %s' % (current_key,))

    return examples
