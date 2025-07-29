# Roundcube Session Decrypt

Decrypt user's password from user's session stored in DB.

```shell
❯ python3 roundcube_session_decrypt.py
usage: roundcube_session_decrypt.py [-h]
                                    (--session SESSION | --session-file SESSION_FILE)
                                    --des-key DES_KEY

Decrypt user's password from user's session stored in DB.

options:
  -h, --help            show this help message and exit
  --session SESSION     Session stored in roundcube.session table
  --session-file SESSION_FILE
                        File containing session records, one by line
  --des-key DES_KEY, -k DES_KEY
                        Triple DES key located in config/config.inc.php

```
