from distbuilder import (
    ConfigFactory,
    PyToBinPackageProcess,
    RobustInstallerProcess,
    mergeQtIfwPackages,
    PyInstHook
)

import subprocess
import os

exec(open('./signals-app/signals/config.py').read())

config = get_config()

env = {
    'NODE_ENV': 'production',
    'UI_HTTP_URL': config['ui_http_url'],
    'SERVER_HTTP_URL': config['server_http_url'],
    'SERVER_WS_URL': config['server_ws_url']
}

subprocess.run(
    ['npm', 'run', 'build'],
    shell=True,
    check=True,
    cwd='./signals-ui',
    env=dict(os.environ, **env)
)

f = masterConfigFactory = ConfigFactory()
f.productName = 'Signals'
f.companyLegalName = 'Signals'
f.version = (0,0,1,0)
f.setupName = 'SignalsSetup'

APP_CONFIG_KEY = 'app'
SERVER_CONFIG_KEY = 'server'

pkgFactories = {
    APP_CONFIG_KEY: None,
    SERVER_CONFIG_KEY: None
}

class BuildProcess(RobustInstallerProcess):
    def onConfigFactory(self, key, f):
        if key == APP_CONFIG_KEY:
            f.productName = 'Signals'
            f.description = 'Signal Processing Toolkit'
            f.binaryName = 'Signals'
            f.version = (0,0,1,0)
            f.isGui = True
            f.sourceDir = './signals-app'
            f.entryPointPy = 'app.py'
        elif key == SERVER_CONFIG_KEY:
            f.productName = 'Signals Server'
            f.description = 'Server for the Signals Signal Processing Toolkit'
            f.binaryName = 'SignalsServer'
            f.version = (0,0,1,0)
            f.isGui = True
            f.sourceDir = './signals-server'
            f.entryPointPy = 'server.py'
    
    def onPyInstConfig(self, key, cfg):
        cfg.isOneFile = False

        if key == SERVER_CONFIG_KEY:
            cfg.dataFilePaths = [
                './static;static',
                './schema;schema',
                './styles/dark.mplstyle;styles'
            ]

    def onPackagesStaged(self, cfg, pkgs):
        comboPkg = mergeQtIfwPackages(pkgs, APP_CONFIG_KEY, SERVER_CONFIG_KEY)
        comboPkg.pkgXml.debug()
        comboPkg.pkgXml.write()

p = BuildProcess(
    masterConfigFactory,
    pyPkgConfigFactoryDict=pkgFactories,
    isDesktopTarget=True
)

p.run()
