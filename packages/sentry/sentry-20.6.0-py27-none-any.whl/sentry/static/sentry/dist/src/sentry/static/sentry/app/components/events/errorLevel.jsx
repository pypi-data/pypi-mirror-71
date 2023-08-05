import { __makeTemplateObject } from "tslib";
import styled from '@emotion/styled';
var DEFAULT_SIZE = '13px';
function getLevelColor(_a) {
    var _b = _a.level, level = _b === void 0 ? '' : _b, theme = _a.theme;
    var COLORS = {
        error: theme.orange,
        info: theme.blue400,
        warning: theme.yellowOrange,
        fatal: theme.red,
        sample: theme.purple,
    };
    return "background-color: " + (COLORS[level] || theme.orange) + ";";
}
var ErrorLevel = styled('span')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  padding: 0;\n  position: relative;\n  width: ", ";\n  height: ", ";\n  text-indent: -9999em;\n  display: inline-block;\n  border-radius: 50%;\n  flex-shrink: 0;\n\n  ", "\n"], ["\n  padding: 0;\n  position: relative;\n  width: ", ";\n  height: ", ";\n  text-indent: -9999em;\n  display: inline-block;\n  border-radius: 50%;\n  flex-shrink: 0;\n\n  ", "\n"])), function (p) { return p.size || DEFAULT_SIZE; }, function (p) { return p.size || DEFAULT_SIZE; }, getLevelColor);
export default ErrorLevel;
var templateObject_1;
//# sourceMappingURL=errorLevel.jsx.map