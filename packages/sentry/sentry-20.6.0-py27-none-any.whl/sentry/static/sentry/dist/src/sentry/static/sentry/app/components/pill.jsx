import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import space from 'app/styles/space';
var Pill = /** @class */ (function (_super) {
    __extends(Pill, _super);
    function Pill() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.getRenderTypeAndValue = function () {
            var value = _this.props.value;
            if (value === undefined) {
                return {};
            }
            var type;
            var renderValue;
            switch (value) {
                case 'true':
                case true:
                    type = 'positive';
                    renderValue = 'yes';
                    break;
                case 'false':
                case false:
                    type = 'negative';
                    renderValue = 'no';
                    break;
                case null:
                case undefined:
                    type = 'negative';
                    renderValue = 'n/a';
                    break;
                default:
                    renderValue = value.toString();
            }
            return { type: type, renderValue: renderValue };
        };
        return _this;
    }
    Pill.prototype.render = function () {
        var _a = this.props, name = _a.name, children = _a.children;
        var _b = this.getRenderTypeAndValue(), type = _b.type, renderValue = _b.renderValue;
        return (<StyledPill>
        <PillName>{name}</PillName>
        <PillValue type={type}>{children || renderValue}</PillValue>
      </StyledPill>);
    };
    return Pill;
}(React.PureComponent));
var StyledPill = styled('li')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  white-space: nowrap;\n  margin: 0 10px 10px 0;\n  display: flex;\n  border: 1px solid ", ";\n  border-radius: ", ";\n  box-shadow: ", ";\n  line-height: 1.2;\n  max-width: 100%;\n  &:last-child {\n    margin-right: 0;\n  }\n"], ["\n  white-space: nowrap;\n  margin: 0 10px 10px 0;\n  display: flex;\n  border: 1px solid ", ";\n  border-radius: ", ";\n  box-shadow: ", ";\n  line-height: 1.2;\n  max-width: 100%;\n  &:last-child {\n    margin-right: 0;\n  }\n"])), function (p) { return p.theme.gray400; }, function (p) { return p.theme.button.borderRadius; }, function (p) { return p.theme.dropShadowLightest; });
var PillName = styled('span')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  padding: ", " ", ";\n  min-width: 0;\n  white-space: nowrap;\n"], ["\n  padding: ", " ", ";\n  min-width: 0;\n  white-space: nowrap;\n"])), space(0.5), space(1));
var PillValue = styled(PillName)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  ", "\n\n  border-left: 1px solid ", ";\n  border-radius: ", ";\n  font-family: ", ";\n  max-width: 100%;\n\n  > a {\n    max-width: 100%;\n    text-overflow: ellipsis;\n    overflow: hidden;\n    white-space: nowrap;\n    display: inline-block;\n    vertical-align: text-bottom;\n  }\n\n  .pill-icon,\n  .external-icon {\n    display: inline;\n    margin: 0 0 0 ", ";\n    color: ", ";\n    line-height: 1.2;\n    &:hover {\n      color: ", ";\n    }\n  }\n"], ["\n  ",
    "\n\n  border-left: 1px solid ", ";\n  border-radius: ",
    ";\n  font-family: ", ";\n  max-width: 100%;\n\n  > a {\n    max-width: 100%;\n    text-overflow: ellipsis;\n    overflow: hidden;\n    white-space: nowrap;\n    display: inline-block;\n    vertical-align: text-bottom;\n  }\n\n  .pill-icon,\n  .external-icon {\n    display: inline;\n    margin: 0 0 0 ", ";\n    color: ", ";\n    line-height: 1.2;\n    &:hover {\n      color: ", ";\n    }\n  }\n"])), function (p) {
    switch (p.type) {
        case 'positive':
            return "\n          background: " + p.theme.green100 + ";\n          border: 1px solid " + p.theme.green400 + ";\n          margin: -1px;\n        ";
        case 'negative':
            return "\n          background: " + p.theme.redLightest + ";\n          border: 1px solid " + p.theme.red + ";\n          margin: -1px;\n        ";
        default:
            return "\n          background: " + p.theme.gray100 + ";\n        ";
    }
}, function (p) { return p.theme.gray400; }, function (p) {
    return "0 " + p.theme.button.borderRadius + " " + p.theme.button.borderRadius + " 0";
}, function (p) { return p.theme.text.familyMono; }, space(1), function (p) { return p.theme.gray500; }, function (p) { return p.theme.gray700; });
export default Pill;
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=pill.jsx.map