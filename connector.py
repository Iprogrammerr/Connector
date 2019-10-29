from src.cli import menu_cli
import sys
import traceback
import signal


def signal_handler(sig, frame):
    menu_cli.close()


try:
    signal.signal(signal.SIGINT, signal_handler)
    menu_cli.setup()
    menu_cli.show()
except KeyboardInterrupt:
    sys.exit()
except Exception as e:
    print("Something went wrong...")
    print(e)
