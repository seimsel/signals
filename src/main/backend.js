import { spawn } from 'child_process';

export function startBackend() {
    console.log(process.cwd())
    const backend = spawn('python', ['./src/backend/main.py']);
    backend.stdout.on('data', (data) => {
        console.log(`${data}`);
    });
    backend.stderr.on('data', (data) => {
        console.error(`${data}`);
    });
}
