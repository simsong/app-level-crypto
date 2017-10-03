#!/usr/bin/env python3
input = "KBfXRWESS6bvyyP3apJ1EfGPUKrpunQ2s5QzKsGC4P-5eJH-KKkc9145RGHateZShuwVK-NwBMjouPUagq4ZS26XBzeAfv2TYjoTp13IFWEQfeeg3ojPmD2M5DrkSrRZTNFQLJFWlVN4o1XS8fIDxLl1TudY44XosWj0RXU7f9xOIBVdcLvyJow_A8L_AU9Q-ir2w3daiqyTrtwkHardIfYDm1DFRl7oXhrcCwhbvnTFcRWX0GZZmDeMTucz6p2ymvI4Mtv6AaIvuVAA--H5RCe0ijgxd65Zmoa-pbBJ0Yr4aymYEIbg2M34DPwln335e6kdslVjNsoeC4x079lDZA"

CONFIG='/var/www/html/demo/config.ini'

import rsa
import keyutil
import base64
import struct
from array import array

def UIntBase64url(s):
    s += '=' * (-len(s) % 4)
    data = base64.urlsafe_b64decode(s)
    return array('B', data)

keydict = keyutil.read_keydict(CONFIG)
priv    = keyutil.dict_to_priv(keydict)
pub     = keyutil.dict_to_pub(keydict)

print(UIntBase64url(input))
print(rsa.decrypt(UIntBase64url(input), priv))

