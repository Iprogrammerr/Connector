from src.cli import http_cli, tcp_cli
from src.protocol.protocol import Protocol
from src.input import smart_input
import sys

NOT_IMPLEMENTED = 'Not implemented yet'
QUIT = 'q'


class Option:

    def __init__(self, key, value, action=None):
        self.key = key
        self.value = value
        self._action = action

    def execute(self):
        if self._action is not None:
            self._action()


def setup():
    smart_input.configure({
        ':q': close,
        ':m': show
    })


def show():
    options = []
    for p in Protocol:
        options.append(Option(p.name, p.value,
                              action=_protocol_action(p)))

    print('Welcome to connector.')
    print('Press :q to quit, :m to go back to menu,',
          'enter to skip any optional(o) input.')
    print('Have pleasurable connecting!')
    print()
    next_option = True
    while next_option:
        print('Choose protocol:')
        _show_options(options)
        option = smart_input.smart_input()
        next_option = _choose(options, option)


def close():
    print()
    print('Stay connected.')
    sys.exit(0)


def _protocol_action(protocol):
    if protocol == Protocol.UDP:
        return lambda: print(NOT_IMPLEMENTED)
    elif protocol == Protocol.TCP:
        return tcp_cli.show
    elif protocol == Protocol.HTTP:
        return http_cli.show
    else:
        return lambda: print("{} isn't proper protocol".format(protocol))


def _show_options(options):
    print('\n'.join(
        [str(o.key) + ' - ' + str(o.value) for o in options]))


def _choose(options, option):
    if option == QUIT:
        return False
    executed = False
    for o in options:
        if str(o.value) == option:
            o.execute()
            executed = True
            break
    if not executed:
        print(f'Choose proper option. {option} is unknown')
    return True
