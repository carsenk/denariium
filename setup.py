#!/usr/bin/env python3

# python setup.py sdist --format=zip,gztar

from setuptools import setup
import os
import sys
import platform
import imp
import argparse

with open('contrib/requirements/requirements.txt') as f:
    requirements = f.read().splitlines()

with open('contrib/requirements/requirements-hw.txt') as f:
    requirements_hw = f.read().splitlines()

version = imp.load_source('version', 'lib/version.py')

if sys.version_info[:3] < (3, 4, 0):
    sys.exit("Error: Denariium requires Python version >= 3.4.0...")

data_files = []

if platform.system() in ['Linux', 'FreeBSD', 'DragonFly']:
    parser = argparse.ArgumentParser()
    parser.add_argument('--root=', dest='root_path', metavar='dir', default='/')
    opts, _ = parser.parse_known_args(sys.argv[1:])
    usr_share = os.path.join(sys.prefix, "share")
    if not os.access(opts.root_path + usr_share, os.W_OK) and \
       not os.access(opts.root_path, os.W_OK):
        if 'XDG_DATA_HOME' in os.environ.keys():
            usr_share = os.environ['XDG_DATA_HOME']
        else:
            usr_share = os.path.expanduser('~/.local/share')
    data_files += [
        (os.path.join(usr_share, 'applications/'), ['denariium.desktop']),
        (os.path.join(usr_share, 'pixmaps/'), ['icons/denariium.png'])
    ]

setup(
    name="Denariium",
    version=version.DENARIIUM_VERSION,
    install_requires=requirements,
    packages=[
        'denariium',
        'denariium_gui',
        'denariium_gui.qt',
        'denariium_plugins',
        'denariium_plugins.audio_modem',
        'denariium_plugins.cosigner_pool',
        'denariium_plugins.email_requests',
        'denariium_plugins.greenaddress_instant',
        'denariium_plugins.hw_wallet',
        'denariium_plugins.keepkey',
        'denariium_plugins.labels',
        'denariium_plugins.ledger',
        'denariium_plugins.trezor',
        'denariium_plugins.digitalbitbox',
        'denariium_plugins.trustedcoin',
        'denariium_plugins.virtualkeyboard',
    ],
    package_dir={
        'denariium': 'lib',
        'denariium_gui': 'gui',
        'denariium_plugins': 'plugins',
    },
    package_data={
        'denariium': [
            'servers.json',
            'servers_testnet.json',
            'currencies.json',
            'checkpoints.json',
            'checkpoints_testnet.json',
            'www/index.html',
            'wordlist/*.txt',
            'locale/*/LC_MESSAGES/denariium.mo',
        ]
    },
    scripts=['denariium'],
    data_files=data_files,
    description="Lightweight Denarius Wallet",
    author="Thomas Voegtlin",
    author_email="thomasv@denariium.org",
    license="MIT Licence",
    url="https://denariium.org",
    long_description="""Lightweight Denarius Wallet"""
)

# Optional modules (not required to run Denariium)
import pip
opt_modules = requirements_hw + ['pycryptodomex']
[ pip.main(['install', m]) for m in opt_modules ]
