from distbuilder import (
    ConfigFactory,
    PyToBinPackageProcess,
    RobustInstallerProcess,
    mergeQtIfwPackages,
    PyInstHook
)

from pathlib import Path

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
            f.isGui = False
            f.sourceDir = './signals-server'
            f.entryPointPy = 'server.py'
    
    def onPyInstConfig(self, key, cfg):
        cfg.isOneFile = False

        if key == SERVER_CONFIG_KEY:
            cfg.dataFilePaths = [
                '../signals-ui/dist;signals-ui',
                './schema;schema',
                './dark.mplstyle;dark.mplstyle'
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
