# Simple SMTP client

# Disclaimer
This is just a lab project to explore SMTP. Please do not use it.

# Installation
```
pip3 install -r requirements.txt
 ```

# Running

Update `config.ini` with sender, recipient, etc.
Run the script to send an email: `python3 -m main.runner`

See #Parameters for configuration.

# Examples

1) Run with default configs (set in `resources/config.ini`)
```
% python3 -m main.runner
2021-05-11 02:45:54,032 - root - INFO - Mail host: alt2.gmail-smtp-in.l.google.com., preference: 20
2021-05-11 02:45:54,435 - root - INFO - Connected to `alt2.gmail-smtp-in.l.google.com.`
2021-05-11 02:45:56,359 - root - INFO - Email successfully sent
```
![](https://i.imgur.com/kV9wiLr.png)

2) Run with overwritten configs:
```
% python3 -m main.runner --recipient contego@yandex.ru --subject Goodbye --attachments img3.png
2021-05-11 02:58:00,980 - root - INFO - Mail host: mx.yandex.ru., preference: 10
2021-05-11 02:58:01,148 - root - INFO - Connected to `mx.yandex.ru.`
2021-05-11 02:58:01,960 - root - INFO - Email successfully sent
```
![](https://i.imgur.com/qm3hTfC.png)

# Parameters
```
% python3 -m main.runner --help
usage: runner.py [-h] [-c CONFIG] --logging_level LOGGING_LEVEL --port PORT --sender SENDER --recipient RECIPIENT --subject SUBJECT --body_file BODY_FILE --attachments ATTACHMENTS

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        Config file path
  --logging_level LOGGING_LEVEL
                        Logging level
  --port PORT           SMTP port to use (default 25)
  --sender SENDER
  --recipient RECIPIENT
  --subject SUBJECT
  --body_file BODY_FILE
  --attachments ATTACHMENTS

Args that start with '--' (eg. --logging_level) can also be set in a config file. Config file syntax allows:
key=value, flag=true, stuff=[a,b,c] (for details, see syntax at https://goo.gl/R74nmi). If an arg is specified in more than one place, then commandline values override config file values which override
defaults.
```

See `resources/config.ini` for default configs.
All files are to be specified relatively to `resource` folder.