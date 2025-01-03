import os
from argparse import ArgumentParser
from shutil import get_terminal_size

from typing import Final


# supported ANSII escape codes for styling
ANSII_CODES: Final[dict] = {
    'bold': '\033[1m',
    'italic': '\033[3m',
    'underline': '\033[4m',
    'strikethrough': '\033[9m',
    'reset': '\033[0m',
}


def write(*args: str) -> None:
    """ A thin wrapper around the "print" function with overriden defaults

    """
    print(*args, sep='', end='')


def play(slides: str) -> None:
    global ANSII_CODES

    # get the size of terminal
    WIDTH, HEIGHT = get_terminal_size()

    with open(slides, 'rb') as fd:
        # apply styles to the text
        # TODO: rethink style escape method
        pages: list = []
        page_max_widths: list = []
        for page in fd.read().decode().split('EOS\n'):
            lines: list[str] = []
            line_lens: list[int] = []

            # iterate over lines in page and apply styles
            # also compute maximum line length for current page
            for line in page.split('\n'):
                clean_line = line
                for style, code in ANSII_CODES.items():
                    style_format = f'{{{style}}}'
                    clean_line = clean_line.replace(style_format, '')
                    line = line.replace(style_format, code)

                lines.append(line)
                line_lens.append(len(clean_line))

            # collect page and its maximum length
            pages.append(lines)
            page_max_widths.append(max(line_lens))
            del lines, line_lens

    page_count: int = len(pages)
    pid: int = 0
    while pid < page_count:
        page = pages[pid]
        max_width = page_max_widths[pid]
        pid += 1

        # generate horizontal and vertival padddings
        padx_chars: str = ' ' * ((WIDTH - max_width) // 2)
        pady: int = round((HEIGHT - len(page) + 1) / 2)

        write(
            f'\033[2J\033[H\033[{pady};0f',
            '\n'.join(f'{padx_chars}{line}' for line in page),
            f'\033[{HEIGHT};0f\033[92mSlides [{pid}/{page_count}]: Goto -> ',
        )

        # navigate to the page
        raw_next_id: str = input()

        # remove color settings
        write(ANSII_CODES['reset'])

        # resolve the next slide
        if not raw_next_id:
            continue
        elif raw_next_id.isdigit() and raw_next_id != '0':
            # navigate to the specified slide or stay on the same
            next_id: int = int(raw_next_id) - 1
            if next_id < page_count:
                pid = next_id
            else:
                pid -= 1
        else:
            pid -= 1


if __name__ == '__main__':
    cmd_parser = ArgumentParser(description='Terminal Slides')
    cmd_parser.add_argument(
        'slides',
        help='path to the file containing slides'
    )
    cmd_args = cmd_parser.parse_args()

    if not os.path.isfile(cmd_args.slides):
        cmd_parser.error("File not found")
        exit(1)

    try:
        # save the cursor's position and enable the alternative buffer
        write('\033[s\033[?25l\033[?1049h')
        play(cmd_args.slides)
    except KeyboardInterrupt:
        pass
    finally:
        # clear screen + reset + disable the alternative buffer + restore the
        # cursor's position + reset
        write('\033[2J\033[H\033[0m\033[?1049l\033[u\033[?25h\033[0m')
