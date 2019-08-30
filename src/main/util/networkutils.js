const net = require('net');

module.exports.findPorts = function findPorts(start, end, num, cb, ports=[]) {
    if (start>end) {
        cb(ports);
    } else {
        const c = net.createConnection({port: start, host: 'localhost'})
        c.on('connect', () => {
            c.end();
            findPorts(start+1, end, num, cb, ports);
        });
        c.on('error', () => {
            ports.push(start);
            
            if(num === ports.length) {
                cb(ports);
            } else {
                findPorts(start+1, end, num, cb, ports);
            }
        });
    }
}