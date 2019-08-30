
export function filename(path) {
    return path.split('\\').pop().split('/').pop();
}

export function to_unix_path(path) {
    return path.replace(/\\/g, "/");
}
