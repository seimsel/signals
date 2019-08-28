
export function toPrimitive(array, property) {
    return array.map(item => item[property]);
}

export function contains(array, property, value) {
    return indexOf(array, property, value) !== -1;
}

export function indexOf(array, property, value) {
    return toPrimitive(array, property).indexOf(value);
}

export function distinct(array, property) {
    const filteredArray = array.filter((item, index) => {
        return indexOf(array, property, item[property]) === index;
    });

    return filteredArray;
}
