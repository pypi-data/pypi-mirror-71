from termcolor import colored, cprint


def clear() -> None:
    print(chr(27) + "[2J")


def pr(text: str, notation: str = '+', end='\n') -> None:
    col = {
        '+': 'green',
        '*': 'cyan',
        '~': 'cyan',
        'X': 'red',
        '!': 'yellow',
        '?': 'blue'
    }[notation]
    print(f"{colored(f'[{notation}]' , col)} {text}", end=end)


def choose(options: iter = ('Yes', 'No'), prompt: str = 'Choose action:', default: int = 0) -> int:
    if not options:
        raise ValueError(
            " [!] No options passed to choice() !!!")  # No options
    pr(prompt, '?')
    for index, option in enumerate(options):
        line = '\t'
        if index == default:
            line += '[%d]. ' % (index + 1)
        else:
            line += ' %d.  ' % (index + 1)
        line += option
        cprint(line, 'yellow')
    try:
        ans = input(colored('[>>>] ', 'yellow'))
        if not ans:
            return default
        ans = int(ans)
        assert 0 < ans <= len(options)
        return ans - 1
    except KeyboardInterrupt:
        return -2  # Keyboard Interrupt
    except AssertionError:
        return -1  # Bad Number
    except ValueError:
        return -1  # Probably text received


def ask(question: str) -> (None, str):
    """
    Ask the user something
    :param question:
    :return: the response, None if no response
    ** Expect a KeyboardInterrupt!!
    """
    pr(question, '?')
    answer = input('>')
    if answer == '':
        return None
    try:
        answer = int(answer)
    except ValueError:
        pass
    return answer


def pause(reason: str = 'continue', cancel: bool = False):
    s = 'Press %s to %s' % (colored('[ENTER]', 'cyan'), reason)
    if cancel:
        s += ', %s to cancel' % colored('[^C]', 'red')
    pr(s, '?')

    try:
        input()
        return True
    except KeyboardInterrupt:
        return False


def cyan(text: str) -> str:
    return colored(text, 'cyan')


def banner(txt: str, style: str = 'slant') -> str:
    """
    Depends on: "pyfiglet"
    :param txt: The text to return as an ASCII art
    :param style: The style (From: /usr/lib/python3.6/site-packages/pyfiglet/fonts/)
    :return: The created ASCII art
    """
    try:
        from pyfiglet import Figlet
    except ImportError:
        pr('Module "pyfiglet" not installed, rendering legacy banner', '!')
        return '~=~=~ %s ~=~=~' % txt
    f = Figlet(font=style)
    return f.renderText(text=txt)


def generic_menu_loop(directory: str, menu: dict) -> None:
    while 1:
        inp = input(colored(f'.{directory}->', 'red', attrs=['bold']))
        if not inp:
            break
        if 'help' in inp:
            for c in menu:
                v = menu[c]
                desc = v[1] if type(
                    v[1]) is str else f'Enter {v[0].capitalize()} menu'
                print(f'  {cyan(c)} -> {colored(desc, "yellow")}')
            continue

        pts = inp.split(' ')
        if pts[0] not in menu:
            pr('No such command! try "help".', '!')
            continue

        command = menu.get(pts[0])
        func = command[0]
        if callable(func):
            func(tuple([i for i in pts[1:] if i]))
        else:
            generic_menu_loop(f'{directory}.{func}', command[1])
        print()


def get_date() -> str:
    """
    :return: today's date (e.g. "28.11.2017" ;P)
    """
    from datetime import datetime
    return datetime.now().strftime("%d.%m.%Y")
