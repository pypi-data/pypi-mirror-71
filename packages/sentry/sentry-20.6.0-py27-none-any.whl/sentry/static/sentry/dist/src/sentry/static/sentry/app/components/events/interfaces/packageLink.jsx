import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Tooltip from 'app/components/tooltip';
import space from 'app/styles/space';
import { defined } from 'app/utils';
import { trimPackage } from 'app/components/events/interfaces/frame/utils';
import InlineSvg from 'app/components/inlineSvg';
import { PackageStatusIcon } from 'app/components/events/interfaces/packageStatus';
import overflowEllipsis from 'app/styles/overflowEllipsis';
var PackageLink = /** @class */ (function (_super) {
    __extends(PackageLink, _super);
    function PackageLink() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleClick = function (event) {
            var _a = _this.props, isClickable = _a.isClickable, onClick = _a.onClick;
            if (isClickable) {
                onClick(event);
            }
        };
        return _this;
    }
    PackageLink.prototype.render = function () {
        var _a = this.props, packagePath = _a.packagePath, isClickable = _a.isClickable, withLeadHint = _a.withLeadHint, children = _a.children;
        return (<Package onClick={this.handleClick} isClickable={isClickable} withLeadHint={withLeadHint}>
        {defined(packagePath) ? (<Tooltip title={packagePath}>
            <PackageName isClickable={isClickable} withLeadHint={withLeadHint}>
              {trimPackage(packagePath)}
            </PackageName>
          </Tooltip>) : (<span>{'<unknown>'}</span>)}
        {children}
        {isClickable && <LinkChevron src="icon-chevron-right"/>}
      </Package>);
    };
    return PackageLink;
}(React.Component));
var LinkChevron = styled(InlineSvg)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  opacity: 0;\n  transform: translateX(", ");\n  transition: all 0.2s ease-in-out;\n  vertical-align: top;\n"], ["\n  opacity: 0;\n  transform: translateX(", ");\n  transition: all 0.2s ease-in-out;\n  vertical-align: top;\n"])), space(0.25));
var Package = styled('a')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  font-size: 13px;\n  font-weight: bold;\n  padding: 0 0 0 ", ";\n  color: ", ";\n  cursor: ", ";\n  ", " {\n    opacity: 0;\n  }\n  &:hover {\n    color: ", ";\n    ", " {\n      opacity: 1;\n      transform: translateX(", ");\n    }\n    ", " {\n      opacity: 1;\n    }\n  }\n  display: flex;\n\n  align-items: flex-start;\n\n  ", "\n\n  @media (min-width: ", ") and (max-width: ", ")  {\n    ", "\n  }\n\n"], ["\n  font-size: 13px;\n  font-weight: bold;\n  padding: 0 0 0 ", ";\n  color: ", ";\n  cursor: ", ";\n  ", " {\n    opacity: 0;\n  }\n  &:hover {\n    color: ", ";\n    ", " {\n      opacity: 1;\n      transform: translateX(", ");\n    }\n    ", " {\n      opacity: 1;\n    }\n  }\n  display: flex;\n\n  align-items: flex-start;\n\n  ", "\n\n  @media (min-width: ", ") and (max-width: ",
    ")  {\n    ", "\n  }\n\n"])), space(0.5), function (p) { return p.theme.gray700; }, function (p) { return (p.isClickable ? 'pointer' : 'default'); }, PackageStatusIcon, function (p) { return p.theme.gray700; }, LinkChevron, space(0.5), PackageStatusIcon, function (p) { return p.withLeadHint && "max-width: 76px;"; }, function (p) { return p.theme.breakpoints[2]; }, function (p) {
    return p.theme.breakpoints[3];
}, function (p) { return p.withLeadHint && "max-width: 63px;"; });
var PackageName = styled('span')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  max-width: ", ";\n  ", "\n"], ["\n  max-width: ", ";\n  ", "\n"])), function (p) { return (p.withLeadHint && p.isClickable ? '45px' : '104px'); }, overflowEllipsis);
export default PackageLink;
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=packageLink.jsx.map