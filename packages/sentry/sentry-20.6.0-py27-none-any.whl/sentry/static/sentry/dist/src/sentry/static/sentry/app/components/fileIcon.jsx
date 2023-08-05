import React from 'react';
import { IconFile } from 'app/icons';
import theme from 'app/utils/theme';
var FILE_EXTENSION_TO_ICON = {
    jsx: 'react',
    tsx: 'react',
    js: 'javascript',
    ts: 'javascript',
    php: 'php',
    py: 'python',
    vue: 'vue',
    go: 'go',
    java: 'java',
    perl: 'perl',
    rb: 'ruby',
    rs: 'rust',
    rlib: 'rust',
    swift: 'swift',
    h: 'apple',
    m: 'apple',
    mm: 'apple',
    M: 'apple',
    cs: 'csharp',
    ex: 'elixir',
    exs: 'elixir',
};
var FileIcon = function (_a) {
    var fileName = _a.fileName, _b = _a.size, providedSize = _b === void 0 ? 'sm' : _b, className = _a.className;
    var _c;
    var fileExtension = fileName.split('.').pop();
    var iconName = fileExtension ? FILE_EXTENSION_TO_ICON[fileExtension] : null;
    var size = (_c = theme.iconSizes[providedSize]) !== null && _c !== void 0 ? _c : providedSize;
    if (!iconName) {
        return <IconFile size={size} className={className}/>;
    }
    return (<img src={require("platformicons/svg/" + iconName + ".svg")} width={size} height={size} className={className}/>);
};
export default FileIcon;
//# sourceMappingURL=fileIcon.jsx.map