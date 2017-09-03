from .config import load as load_config, ConfigError
from .manage import Tracemail, DatabaseError
import sys

def print_table(headers, rows):
    column_widths = [ max(len(headers[i]), max(len(str(row[i])) for row in rows))
            for i in range(len(headers)) ]
    fmt = ' ' + ' | '.join('{{:{}}}'.format(width) for width in column_widths) + ' '
    print(fmt.format(*headers))
    print('-' + '-+-'.join('-' * width for width in column_widths) + '-')
    for row in rows:
        print(fmt.format(*[str(c) for c in row]))


def main():
    if len(sys.argv) < 2:
        sys.stderr.write('Usage: {} <operation> [options]\n'.format(sys.argv[0]))
        sys.exit(1)

    try:
        config = load_config('config.toml')
    except ConfigError as e:
        sys.stderr.write('Error loading configuration: {}\n'.format(e))
        sys.exit(1)

    tm = Tracemail(config)

    operation = sys.argv[1]
    try:
        if operation == 'list':
            aliases = tm.list_aliases()
            if aliases:
                column_headers = [ 'Alias', 'Mailbox', 'Purpose', 'Created' ]
                print_table(column_headers, aliases)
        elif operation == 'add':
            if len(sys.argv) < 4:
                sys.stderr.write('Usage: {} add <alias> <mailbox> [<purpose>]\n')
                sys.exit(1)
            tm.new_alias(sys.argv[2], sys.argv[3], sys.argv[4] if len(sys.argv) > 4 else None)
    except DatabaseError as e:
        sys.stderr.write('Database error: {}\n'.format(str(e).replace('\n', ' ')))

if __name__ == '__main__':
    main()
