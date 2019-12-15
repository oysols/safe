# Simple public key encryption for sharing files

Command line interface for libsodium

Uses PyNaCl python bindings.

# Setup

`pip3 install --user git+https://github.com/oysols/safe`

# Usage

As easy as 1-2-3:

1. Receiver runs `safe` to create private key

```
$ safe
Your private key: '/home/receiver/.safe.private.key'
Your public key: bfad2a2061398a799388e86426297dcfdbdbb2d943d4b0c728b31e24e2c38b76
```

2. Sender encrypts the file with the Receivers public key

```
$ safe -e bfad2a2061398a799388e86426297dcfdbdbb2d943d4b0c728b31e24e2c38b76 secret_message.txt
```

3. Receiver decrypts the file

```
$ safe -d secret_message.txt.encrypted
Decrypted file: 'secret_message.txt.encrypted.decrypted'
```
