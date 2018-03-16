# -*- mode: python -*-

from PyInstaller.utils.hooks import collect_data_files, collect_submodules, collect_dynamic_libs

import sys
import os

PACKAGE='Denariium'
PYPKG='denariium'
MAIN_SCRIPT='denariium'
ICONS_FILE='denariium.icns'

for i, x in enumerate(sys.argv):
    if x == '--name':
        VERSION = sys.argv[i+1]
        break
else:
    raise BaseException('no version')

denariium = os.path.abspath(".") + "/"
block_cipher = None

# see https://github.com/pyinstaller/pyinstaller/issues/2005
hiddenimports = []
hiddenimports += collect_submodules('trezorlib')
hiddenimports += collect_submodules('btchip')
hiddenimports += collect_submodules('keepkeylib')
hiddenimports += collect_submodules('websocket')

datas = [
    (denariium+'lib/currencies.json', PYPKG),
    (denariium+'lib/servers.json', PYPKG),
    (denariium+'lib/checkpoints.json', PYPKG),
    (denariium+'lib/servers_testnet.json', PYPKG),
    (denariium+'lib/checkpoints_testnet.json', PYPKG),
    (denariium+'lib/wordlist/english.txt', PYPKG + '/wordlist'),
    (denariium+'lib/locale', PYPKG + '/locale'),
    (denariium+'plugins', PYPKG + '_plugins'),
]
datas += collect_data_files('trezorlib')
datas += collect_data_files('btchip')
datas += collect_data_files('keepkeylib')

# Add libusb so Trezor will work
binaries = [(denariium + "contrib/build-osx/libusb-1.0.dylib", ".")]

# Workaround for "Retro Look":
binaries += [b for b in collect_dynamic_libs('PyQt5') if 'macstyle' in b[0]]

# We don't put these files in to actually include them in the script but to make the Analysis method scan them for imports
a = Analysis([denariium+MAIN_SCRIPT,
              denariium+'gui/qt/main_window.py',
              denariium+'gui/text.py',
              denariium+'lib/util.py',
              denariium+'lib/wallet.py',
              denariium+'lib/simple_config.py',
              denariium+'lib/denarius.py',
              denariium+'lib/dnssec.py',
              denariium+'lib/commands.py',
              denariium+'plugins/cosigner_pool/qt.py',
              denariium+'plugins/email_requests/qt.py',
              denariium+'plugins/trezor/client.py',
              denariium+'plugins/trezor/qt.py',
              denariium+'plugins/keepkey/qt.py',
              denariium+'plugins/ledger/qt.py',
              ],
             binaries=binaries,
             datas=datas,
             hiddenimports=hiddenimports,
             hookspath=[])

# http://stackoverflow.com/questions/19055089/pyinstaller-onefile-warning-pyconfig-h-when-importing-scipy-or-scipy-signal
for d in a.datas:
    if 'pyconfig' in d[0]:
        a.datas.remove(d)
        break

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.datas,
          name=PACKAGE,
          debug=False,
          strip=False,
          upx=True,
          icon=denariium+ICONS_FILE,
          console=False)

app = BUNDLE(exe,
             version = VERSION,
             name=PACKAGE + '.app',
             icon=denariium+ICONS_FILE,
             bundle_identifier=None,
             info_plist={
                'NSHighResolutionCapable': 'True',
                'NSSupportsAutomaticGraphicsSwitching': 'True'
             }
)
