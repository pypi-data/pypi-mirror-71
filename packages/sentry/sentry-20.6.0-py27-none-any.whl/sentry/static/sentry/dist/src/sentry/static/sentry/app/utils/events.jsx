import { isNativePlatform } from 'app/utils/platform';
/**
 * Extract the display message from an event.
 */
export function getMessage(event) {
    var metadata = event.metadata, type = event.type, culprit = event.culprit;
    switch (type) {
        case 'error':
            return metadata.value;
        case 'csp':
            return metadata.message;
        case 'expectct':
        case 'expectstaple':
        case 'hpkp':
            return '';
        default:
            return culprit || '';
    }
}
/**
 * Get the location from an event.
 */
export function getLocation(event) {
    if (event.type === 'error' && isNativePlatform(event.platform)) {
        return event.metadata.filename || null;
    }
    return null;
}
export function getTitle(event) {
    var metadata = event.metadata, type = event.type, culprit = event.culprit;
    var result = {
        title: event.title,
        subtitle: '',
    };
    if (type === 'error') {
        result.subtitle = culprit;
        if (metadata.type) {
            result.title = metadata.type;
        }
        else {
            result.title = metadata.function || '<unknown>';
        }
    }
    else if (type === 'csp') {
        result.title = metadata.directive || '';
        result.subtitle = metadata.uri || '';
    }
    else if (type === 'expectct' || type === 'expectstaple' || type === 'hpkp') {
        result.title = metadata.message || '';
        result.subtitle = metadata.origin || '';
    }
    else if (type === 'default') {
        result.title = metadata.title || '';
    }
    return result;
}
//# sourceMappingURL=events.jsx.map