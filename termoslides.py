#!/usr/bin/python3
import os
import shutil
from subprocess import run
from argparse import ArgumentParser


# supported terminal styles
TERM_STYLES: dict = {
    'bold': '\033[1m',
    'italic': '\033[3m',
    'underline': '\033[4m',
    'strikethrough': '\033[9m',
    'reset': '\033[0m'
}


def play(slides: str) -> None:
    global TERM_STYLES

    # get the size of terminal
    width, height = shutil.get_terminal_size()

    with open(slides, 'rb') as fd:
        # apply styles to the text
        # TODO: rethink style escape method
        pages = []
        page_max_lens = []
        for page in fd.read().decode().split('EOS\n'):
            lines = []
            line_lens = []

            # iterate over lines in page and apply styles
            # also compute maximum line length for current page
            for line in page.split('\n'):
                clean_line = line
                for style, code in TERM_STYLES.items():
                    style_format = f'{{{style}}}'
                    clean_line = clean_line.replace(style_format, '')
                    line = line.replace(style_format, code)

                lines.append(line)
                line_lens.append(len(clean_line))

            # collect page and its maximum length
            pages.append(lines)
            page_max_lens.append(max(line_lens))
            del lines, line_lens

    page_count = len(pages)
    pid = 0
    while pid < page_count:
        page = pages[pid]
        max_len = page_max_lens[pid]
        pid += 1
        clear()

        # generate horizontal and vertival padddings
        padx = ' ' * ((width - max_len) // 2)
        pady = '\n' * ((height - len(page) - 2) // 2)

        # set top padding
        print(pady)

        for line in page:
            # print(f'{padx}{line}'[:width - 5])
            print(padx, line, sep='')

        # set bottom padding
        print(pady)
        print('\033[92m' + f'Slides [{pid}/{page_count}]: ', end='')

        # navigate to the page
        raw_next_id: str = input(' Goto -> ')

        # remove color settings
        print(TERM_STYLES['reset'])

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

    clear()


# define cross-platform terminal screen cleanup function
if os.name == 'nt':
    def clear() -> None:
        """ Clear terminal screen

        """
        run('cls', shell=True)
else:
    def clear() -> None:
        """ Clear terminal screen

        """
        run('clear')


if __name__ == '__main__':
    cmd_parser = ArgumentParser(description='Terminal Slides')
    cmd_parser.add_argument(
        'slides',
        help='file containing slides'
    )
    cmd_args = cmd_parser.parse_args()

    try:
        play(cmd_args.slides)
    except KeyboardInterrupt:
        # remove color settings
        print(TERM_STYLES['reset'])
        clear()
