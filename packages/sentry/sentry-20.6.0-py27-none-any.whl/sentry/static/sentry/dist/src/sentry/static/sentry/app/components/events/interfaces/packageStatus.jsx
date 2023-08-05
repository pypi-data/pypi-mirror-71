import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import InlineSvg from 'app/components/inlineSvg';
import Tooltip from 'app/components/tooltip';
import space from 'app/styles/space';
var PackageStatus = /** @class */ (function (_super) {
    __extends(PackageStatus, _super);
    function PackageStatus() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    PackageStatus.prototype.getIconTypeAndSource = function (status) {
        switch (status) {
            case 'success':
                return { iconType: 'success', iconSrc: 'icon-circle-check' };
            case 'empty':
                return { iconType: 'muted', iconSrc: 'icon-circle-empty' };
            case 'error':
            default:
                return { iconType: 'error', iconSrc: 'icon-circle-exclamation' };
        }
    };
    PackageStatus.prototype.render = function () {
        var _a = this.props, status = _a.status, tooltip = _a.tooltip;
        var _b = this.getIconTypeAndSource(status), iconType = _b.iconType, iconSrc = _b.iconSrc;
        if (status === 'empty') {
            return null;
        }
        return (<Tooltip title={tooltip} disabled={!(tooltip && tooltip.length)}>
        <PackageStatusIcon type={iconType} src={iconSrc} size="1em"/>
      </Tooltip>);
    };
    return PackageStatus;
}(React.Component));
export var PackageStatusIcon = styled(InlineSvg)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  color: ", ";\n  margin-left: ", ";\n  opacity: 0;\n"], ["\n  color: ", ";\n  margin-left: ", ";\n  opacity: 0;\n"])), function (p) { return p.theme.alert[p.type].iconColor; }, space(0.5));
export default PackageStatus;
var templateObject_1;
//# sourceMappingURL=packageStatus.jsx.map