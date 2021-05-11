import sys
import os
import configargparse
from pathlib import Path
from os.path import *
import site
from main.utils import *
import logging


def get_resource_dir():
    possibilities = [
        abspath(join(dirname(__file__), '..', 'resources')),
        abspath(join(sys.prefix, 'simple_smtp_client_resources')),
        abspath(join(site.USER_BASE, 'simple_smtp_client_resources'))
    ]

    for p in possibilities:
        if Path(p).exists():
            return p


def set_logging_level(level):
    root = logging.getLogger()
    root.setLevel(logging.getLevelName(level))

    handler = logging.StreamHandler(sys.stderr)
    handler.setLevel(logging.getLevelName(level))
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    root.addHandler(handler)


def parse_args(argv):
    p = configargparse.ArgParser(default_config_files=[join(get_resource_dir(), 'config.ini')])
    p.add_argument('-c', '--config', required=False, is_config_file=True, help='Config file path')
    p.add_argument('--logging_level', required=True, help='Logging level')
    p.add_argument('--port', type=int, required=True, help='SMTP port to use')
    p.add_argument('--sender', required=True)
    p.add_argument('--recipient', required=True)
    p.add_argument('--subject', required=True)
    p.add_argument('--body_file', type=lambda x: open(join(get_resource_dir(), x), 'rt').read(), required=True)
    p.add_argument('--attachments', type=lambda x: join(get_resource_dir(), x), action='append', required=True)

    args = p.parse_args(argv)

    return args


def main():
    args = parse_args(sys.argv[1:])
    set_logging_level(args.logging_level)

    for mx in get_mxs(args.recipient):
        try:
            socket = connect(mx, args.port)
        except Exception as e:
            logging.warning("Ooops, can't connect to `{}`: [{}] {}".format(mx, type(e), e))
            continue

        logging.info("Connected to `{}`".format(mx))

        try:
            greeting(socket, 'barbanyagra.github.io')
            send_mail(socket,
                      sender=args.sender,
                      recipient=args.recipient,
                      subject=args.subject,
                      body=args.body_file,
                      attachments=args.attachments)
            close(socket)
            # hooray, success
            logging.info("Email successfully sent")
            break
        finally:
            socket.close()
    else:
        raise Exception("Unable to find an active SMTP server. The message is NOT sent.")


if __name__ == '__main__':
    main()
