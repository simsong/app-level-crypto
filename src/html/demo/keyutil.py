#!/usr/bin/python3
#

# Configuration information for the system:

CONFIG='/var/www/html/demo/config.ini'


import rsa
import json
from configparser import ConfigParser


# Added by W. Yates Feb 17th, 2017
# Playing a hunch that JWK does not like rsa integer keys
import math
import base64
import urllib
from array import array

# Not needed anymore, use MYSQLdb instead
def get_dbfile(configFile):
    config = ConfigParser()
    config.read(configFile)
    return config['files']['database']

def base64_to_uchr(s):
    # return urllib.parse.unquote(s)
    return base64.b64decode(urllib.parse.unquote(s))

def base64_to_uchr_array(s):
    # Convert to unsigned char array to check against client
    data = array('B', base64.b64decode(urllib.parse.unquote(s)))
    return data

def uchr_to_base64(n):
    # fromhex() needs an even number of hex characters,
    # so when converting our number to hex we need to give it an even
    # length. (2 characters per byte, 8 bits per byte)
    length = int(math.ceil(n.bit_length() / 8.0)) * 2
    fmt = '%%0%dx' % length
    packed = bytearray.fromhex(fmt % n)
    s = base64.b64encode(packed)
    return s.decode("ascii")

def uchr_to_base64url(n):
    # fromhex() needs an even number of hex characters,
    # so when converting our number to hex we need to give it an even
    # length. (2 characters per byte, 8 bits per byte)
    length = int(math.ceil(n.bit_length() / 8.0)) * 2
    fmt = '%%0%dx' % length
    packed = bytearray.fromhex(fmt % n)
    s = base64.urlsafe_b64encode(packed).rstrip(b'=')
    return s.decode("ascii")

def read_keydict(configFile):
    """Read the key dictionary from a configuration file"""
    config = ConfigParser()
    config.read(configFile)
    try:
        return json.loads(config['keys']['priv'])
    except KeyError as e:
        raise RuntimeError("[key][priv] not found in configuration file {}".format(configFile))

def dict_to_priv(d):
    """Convert a dictionary to an rsa.PrivateKey"""
    return rsa.PrivateKey(d['n'],d['e'],d['d'],d['p'],d['q'])

def dict_to_pub(d):
    return rsa.PublicKey(d['n'],d['e'])

def dict_to_pub_key(d):
    return uchr_to_base64(d['n'])

def dict_to_jwk(d):
    """Convert a key dictionary to a JSON Web Key string"""
    # return json.dumps({'n':d['n'],'e':d['e']})
    # Changed by W. Yates on Feb 17th, 2017
    # Needed a few changes to work with crypto importKey
    n_val = uchr_to_base64url(d['n'])
    e_val = uchr_to_base64url(d['e'])
    return json.dumps({'n':n_val,'e':e_val, 'kty':'RSA', 'use':'enc' })

if __name__=="__main__":
    import argparse

    parser = argparse.ArgumentParser("create/test keys")
    parser.add_argument("--read",   help="read ini file and test them",               action ="store_true")
    parser.add_argument("--create", help="Generate public key and write to the file", action ="store_true")
    parser.add_argument("--config", help="name of config file",                       default="config.ini")
    parser.add_argument("--write",  help="write new rsa keys to inifile",             action ="store_true")
    args = parser.parse_args()

    if args.write:
        # Make the public/private keypair
        (pub,priv) = rsa.newkeys(2048)

        # Convert to dictionary format for writing as JWK
        dpub = {'n':pub.n,'e':pub.e}
        dpriv = {'p':priv.p,'q':priv.q,'n':priv.n,'e':priv.e,'d':priv.d}

        # Write the output
        with open(args.config,"a") as f:
            f.write("[keys]\n")
            f.write("priv: {}\n".format(json.dumps(dpriv)))
    
    if args.read:
        keydict = read_keydict(args.config)
        priv = dict_to_priv(keydict)
        pub = dict_to_pub(keydict)
        assert b'foobar' == rsa.decrypt(rsa.encrypt(b'foobar',pub),priv)
        print("test passes")
