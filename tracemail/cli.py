from .config import load as load_config, ConfigError
from .manage import Tracemail
import sys


def main():
    #try:
    config = load_config('config.toml')
    #except ConfigError as e:
    #    sys.stderr.write('Error loading configuration: {}\n'.format(e))
    #    sys.exit(1)

    tm = Tracemail(config)
    tm.list_aliases()

if __name__ == '__main__':
    main()
