from snippet.config import Config
from snippet import exceptions


def extract_snippets(config: Config, lines, path):
    """Finds snippets in lines of text"""
    current_key = None
    current_block = None
    current_strip = None
    capture = False
    cloak = False
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
                raise exceptions.StartEndMismatch(f'Already capturing at {current_key}')
            capture = True
            continue

        if config.end_flag in line:
            # stop capturing, and discard empty blocks
            if not capture:
                raise exceptions.StartEndMismatch(f'Not yet capturing at {current_key}')
            capture = False
            if not current_block:
                examples.pop(current_key)
            continue

        if config.uncloak_flag in line:
            if not cloak:
                raise exceptions.CloakMismatch(f'Already uncloaked at {current_key}')
            cloak = False
            continue

        if capture and not cloak:
            if config.cloak_flag in line:
                if cloak:
                    raise exceptions.CloakMismatch(f'Already cloaked at {current_key}')
                cloak = True
                continue

            # whilst capturing, append code lines to the current block
            if config.fail_on_dedent and any(line[:current_strip].split(' ')):
                raise exceptions.ValidationFailure(f'Unexpected dedent whilst capturing {current_key}')
            clean_line = line[current_strip:].rstrip()
            for r_before, r_after in config.replacements.items():
                clean_line = clean_line.replace(r_before, r_after)
            for trigger in config.fail_on_contains:
                if trigger in clean_line:
                    raise exceptions.ValidationFailure(f'Unexpected phrase {repr(trigger)} at {current_key}')
            # add this line of code to the example block
            current_block.append(clean_line)

    if capture:
        raise exceptions.StartEndMismatch(f'EOF reached whilst still capturing {current_key}')

    if cloak:
        raise exceptions.CloakMismatch(f'EOF reached whilst still cloaked {current_key}')

    return examples
