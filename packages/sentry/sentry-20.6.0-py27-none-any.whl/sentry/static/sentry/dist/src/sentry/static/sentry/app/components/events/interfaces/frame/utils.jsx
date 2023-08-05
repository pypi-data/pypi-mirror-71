export function trimPackage(pkg) {
    var pieces = pkg.split(/^([a-z]:\\|\\\\)/i.test(pkg) ? '\\' : '/');
    var filename = pieces[pieces.length - 1] || pieces[pieces.length - 2] || pkg;
    return filename.replace(/\.(dylib|so|a|dll|exe)$/, '');
}
export function getPlatform(dataPlatform, platform) {
    // prioritize the frame platform but fall back to the platform
    // of the stacktrace / exception
    return dataPlatform || platform;
}
//# sourceMappingURL=utils.jsx.map