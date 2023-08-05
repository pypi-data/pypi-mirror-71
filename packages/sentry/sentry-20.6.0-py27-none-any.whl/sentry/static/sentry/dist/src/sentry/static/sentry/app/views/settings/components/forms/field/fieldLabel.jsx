import { __makeTemplateObject } from "tslib";
import styled from '@emotion/styled';
import isPropValid from '@emotion/is-prop-valid';
var shouldForwardProp = function (p) { return p !== 'disabled' && isPropValid(p); };
var FieldLabel = styled('div', { shouldForwardProp: shouldForwardProp })(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (p) { return (!p.disabled ? p.theme.gray800 : p.theme.gray500); });
export default FieldLabel;
var templateObject_1;
//# sourceMappingURL=fieldLabel.jsx.map