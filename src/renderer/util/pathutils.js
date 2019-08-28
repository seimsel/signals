
export function filename(path) {
    return path.split('\\').pop().split('/').pop();
}
