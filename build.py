from distbuilder import (
    ConfigFactory,
    PyToBinPackageProcess,
    RobustInstallerProcess,
    mergeQtIfwPackages,
    PyInstHook
)

f = masterConfigFactory = ConfigFactory()
f.productName = 'Signals'
f.companyLegalName = 'Signals'
f.version = (0,0,1,0)
f.setupName = 'signals_setup'

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
            f.binaryName = 'signals'
            f.version = (0,0,1,0)
            f.isGui = True
            f.sourceDir = './signals-app'
            f.entryPointPy = 'app.py'
        elif key == SERVER_CONFIG_KEY:
            PyInstHook('bundle_ui')

            f.productName = 'Signals Server'
            f.description = 'Server for the Signals Signal Processing Toolkit'
            f.binaryName = 'signals-server'
            f.version = (0,0,1,0)
            f.isGui = False
            f.souceDir = './signals-server'
            f.entryPointPy = 'server.py'

    def onPackagesStaged(self, cfg, pkgs):
        comboPkg = mergeQtIfwPackages(pkgs, APP_CONFIG_KEY, SERVER_CONFIG_KEY)
        comboPkg.pkgXml.debug()
        comboPkg.pkgXml.write()

p = BuildProcess(
    masterConfigFactory,
    pyPkgConfigFactoryDict=pkgFactories,
    isDesktopTarget=True
)

p.isTestingInstall = True
p.run()
