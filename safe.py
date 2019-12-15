#!/usr/bin/env python3
from pathlib import Path
import sys
import argparse
from typing import Tuple

from nacl.public import PrivateKey, PublicKey, SealedBox  # type: ignore
from nacl.encoding import HexEncoder  # type: ignore


def get_keys() -> Tuple[PrivateKey, str]:
    private_key_path = Path("~/.safe.private.key").expanduser()

    if private_key_path.is_file():
        private_key_hex = private_key_path.read_text().strip()
        assert len(private_key_hex) == 64
        private_key = PrivateKey(HexEncoder.decode(private_key_hex))
    else:
        private_key = PrivateKey.generate()
        private_key_hex = HexEncoder.encode(private_key.encode()).decode()
        private_key_path.write_text(private_key_hex)

    public_key_hex = HexEncoder.encode(private_key.public_key.encode()).decode()
    print(f"Your private key: '{private_key_path.absolute()}'")
    print(f"Your public key: {public_key_hex}")
    return private_key, public_key_hex


def encrypt(public_key: PublicKey, input_path: Path, output_path: Path) -> None:
    box = SealedBox(public_key)
    encrypted = box.encrypt(input_path.read_bytes())
    output_path.write_bytes(encrypted)


def decrypt(private_key: PrivateKey, input_path: Path, output_path: Path) -> None:
    box = SealedBox(private_key)
    decrypted = box.decrypt(input_path.read_bytes())
    output_path.write_bytes(decrypted)


def main() -> None:
    parser = argparse.ArgumentParser(description="Simple public key encryption using libsodium")
    parser.add_argument("-e", metavar="KEY", help="Encrypt to public key")
    parser.add_argument("-d", help="Decrypt using your private key", action="store_true")
    parser.add_argument("file", nargs="?", help="Path to file")
    args = parser.parse_args()

    private_key, public_key_hex = get_keys()

    if not args.file and (args.e or args.d):
        print("No file specified")
        sys.exit(1)

    if args.e:
        path = Path(args.file)
        try:
            assert len(public_key_hex) == 64
            public_key = PublicKey(HexEncoder.decode(args.e.encode()))
        except Exception:
            print("Public key format error")
            sys.exit(1)
        output_path = path.with_name(path.name + ".encrypted")
        encrypt(public_key, path, output_path)
        print(f"Encrypted file to {args.e}: '{output_path}'")
    elif args.d:
        path = Path(args.file)
        try:
            output_path = path.with_name(path.name + ".decrypted")
            decrypt(private_key, path, output_path)
            print(f"Decrypted file: '{output_path}'")
        except Exception:
            print("Could not decrypt file with private key")


if __name__ == "__main__":
    main()
