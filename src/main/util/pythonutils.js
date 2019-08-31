const { exec } = require('child_process');
const semver = require('semver');

module.exports.findPython = function findPython(tryPaths, cb) {
    if(tryPaths.length === 0) {
        return;
    }

    exec(`${tryPaths[0]} --version`, (error, stdout, stderr) => {
        const version = semver.clean(stdout.slice(7));

        if(semver.valid(version) && semver.gt(version, '3.0.0')) {
            cb(tryPaths[0]);
        } else {
            findPython(tryPaths.slice(1), cb);
        }
    });
}