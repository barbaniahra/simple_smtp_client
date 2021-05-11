from socket import *
import ssl
import logging
import dns.resolver
import uuid
import base64
import mimetypes


NEWLINE = '\r\n'


def get_mxs(email):
    answers = dns.resolver.resolve(email.split('@')[-1], 'MX')
    for rdata in answers:
        logging.info('Mail host: {}, preference: {}'.format(rdata.exchange, rdata.preference))
        yield str(rdata.exchange)


def read(socket):
    data = socket.recv(1024)
    logging.debug('Read {} bytes from socket: {}'.format(len(data), data))
    return data


def write(socket, data: bytes):
    socket.send(data)
    logging.debug('Wrote {} bytes to socket: {}'.format(len(data), data))


def assert_prefix(data, prefix: bytes):
    if data[:len(prefix)] != prefix:
        raise Exception(f'Expected `{prefix} ...`, got: `{data}`')


def assert_ok(data):
    assert_prefix(data, b'250')


def connect(server, port) -> socket:
    mail_socket = socket(AF_INET,SOCK_STREAM)

    if port in {465, 587}:
        wrapped_mail_socket = ssl.wrap_socket(mail_socket, ssl_version=ssl.PROTOCOL_TLSv1)
    else:
        wrapped_mail_socket = mail_socket

    wrapped_mail_socket.connect((server, port))

    data = read(wrapped_mail_socket)
    assert_prefix(data, b'220')

    return wrapped_mail_socket


def greeting(socket, server):
    write(socket, f'HELO {server}{NEWLINE}'.encode())
    assert_ok(read(socket))


def send_mail(socket, sender, recipient, subject, body, attachments):
    boundary = uuid.uuid4().hex

    write(socket, f'MAIL FROM: <{sender}>{NEWLINE}'.encode())
    assert_ok(read(socket))
    write(socket, f'RCPT TO: <{recipient}>{NEWLINE}'.encode())
    assert_ok(read(socket))
    write(socket, f'DATA{NEWLINE}'.encode())
    assert_prefix(read(socket), b'354')

    escaped_body = NEWLINE.join(
        ('.' + line) if line.startswith('.') else line
        for line in body.split('\n')
    )

    # common
    write(socket, f"From: <{sender}>{NEWLINE}"
                  f"To: <{sender}>{NEWLINE}"
                  f"Subject: {subject}{NEWLINE}"
                  f"Content-Type: multipart/mixed; boundary={boundary}{NEWLINE}"
                  f"{NEWLINE}".encode())

    #body
    write(socket, f"--{boundary}{NEWLINE}"
                  f"Content-Type: text/plain{NEWLINE}"
                  f"{NEWLINE}"
                  f"{escaped_body}{NEWLINE}".encode())

    #files
    for attachment in attachments:
        with open(attachment, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())

        content_type = mimetypes.guess_type(attachment)[0]
        if content_type is None:
            content_type = 'application/octet-stream'

        write(socket, f"--{boundary}{NEWLINE}"
                      f"Content-Type: {content_type}{NEWLINE}"
                      f"Content-Transfer-Encoding: base64{NEWLINE}"
                      f"{NEWLINE}".encode() +
                      encoded_string +
                      f";{NEWLINE}".encode())

    write(socket, f"--{boundary}{NEWLINE}"
                  f".{NEWLINE}".encode())
    assert_ok(read(socket))


def close(socket):
    write(socket, f'QUIT{NEWLINE}'.encode())
    assert_prefix(read(socket), b'221')
    socket.close()
