import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Tooltip from 'app/components/tooltip';
import space from 'app/styles/space';
import { t } from 'app/locale';
import { formatAddress, parseAddress } from 'app/components/events/interfaces/utils';
import overflowEllipsis from 'app/styles/overflowEllipsis';
var TogglableAddress = /** @class */ (function (_super) {
    __extends(TogglableAddress, _super);
    function TogglableAddress() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    TogglableAddress.prototype.convertAbsoluteAddressToRelative = function () {
        var _a = this.props, startingAddress = _a.startingAddress, address = _a.address, maxLengthOfRelativeAddress = _a.maxLengthOfRelativeAddress;
        if (!startingAddress) {
            return '';
        }
        var relativeAddress = formatAddress(parseAddress(address) - parseAddress(startingAddress), maxLengthOfRelativeAddress);
        return "+" + relativeAddress;
    };
    TogglableAddress.prototype.getAddressTooltip = function () {
        var _a = this.props, isInlineFrame = _a.isInlineFrame, isFoundByStackScanning = _a.isFoundByStackScanning;
        if (isInlineFrame && isFoundByStackScanning) {
            return t('Inline frame, found by stack scanning');
        }
        if (isInlineFrame) {
            return t('Inline frame');
        }
        if (isFoundByStackScanning) {
            return t('Found by stack scanning');
        }
        return null;
    };
    TogglableAddress.prototype.render = function () {
        var _a = this.props, address = _a.address, isAbsolute = _a.isAbsolute, onToggle = _a.onToggle, isFoundByStackScanning = _a.isFoundByStackScanning, isInlineFrame = _a.isInlineFrame;
        var relativeAddress = this.convertAbsoluteAddressToRelative();
        var canBeConverted = !!(onToggle && relativeAddress);
        var formattedAddress = !relativeAddress || isAbsolute ? address : relativeAddress;
        return (<Address>
        {canBeConverted && (<Tooltip title={isAbsolute ? t('Absolute') : t('Relative')}>
            <Toggle className="icon-filter" onClick={onToggle}/>
          </Tooltip>)}

        <Tooltip title={this.getAddressTooltip()} disabled={!(isFoundByStackScanning || isInlineFrame)}>
          <AddressText isFoundByStackScanning={isFoundByStackScanning} isInlineFrame={isInlineFrame} canBeConverted={canBeConverted}>
            {formattedAddress}
          </AddressText>
        </Tooltip>
      </Address>);
    };
    return TogglableAddress;
}(React.Component));
var Toggle = styled('span')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  opacity: 0.33;\n  margin-right: 1ex;\n  cursor: pointer;\n  visibility: hidden;\n  position: relative;\n  top: 1px;\n  display: none;\n\n  &:hover {\n    opacity: 1;\n  }\n\n  @media (min-width: ", ") {\n    display: inline;\n  }\n"], ["\n  opacity: 0.33;\n  margin-right: 1ex;\n  cursor: pointer;\n  visibility: hidden;\n  position: relative;\n  top: 1px;\n  display: none;\n\n  &:hover {\n    opacity: 1;\n  }\n\n  @media (min-width: ", ") {\n    display: inline;\n  }\n"])), function (props) { return props.theme.breakpoints[0]; });
var AddressText = styled('span')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  border-bottom: ", ";\n  padding-left: ", ";\n"], ["\n  border-bottom: ",
    ";\n  padding-left: ", ";\n"])), function (p) {
    if (p.isFoundByStackScanning) {
        return "1px dashed " + p.theme.red;
    }
    else if (p.isInlineFrame) {
        return "1px dashed " + p.theme.blue400;
    }
    else {
        return 'none';
    }
}, function (p) { return (p.canBeConverted ? null : '18px'); });
var Address = styled('span')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  font-family: ", ";\n  font-size: ", ";\n  color: ", ";\n  letter-spacing: -0.25px;\n  width: 100%;\n  flex-grow: 0;\n  flex-shrink: 0;\n  display: block;\n  padding: 0 ", " 0 0;\n  order: 1;\n\n  &:hover ", " {\n    visibility: visible;\n  }\n\n  @media (min-width: ", ") {\n    padding: 0 ", ";\n    width: 117px;\n    order: 0;\n  }\n  ", "\n"], ["\n  font-family: ", ";\n  font-size: ", ";\n  color: ", ";\n  letter-spacing: -0.25px;\n  width: 100%;\n  flex-grow: 0;\n  flex-shrink: 0;\n  display: block;\n  padding: 0 ", " 0 0;\n  order: 1;\n\n  &:hover ", " {\n    visibility: visible;\n  }\n\n  @media (min-width: ", ") {\n    padding: 0 ", ";\n    width: 117px;\n    order: 0;\n  }\n  ", "\n"])), function (p) { return p.theme.text.familyMono; }, function (p) { return p.theme.fontSizeExtraSmall; }, function (p) { return p.theme.gray700; }, space(0.5), Toggle, function (props) { return props.theme.breakpoints[0]; }, space(0.5), overflowEllipsis);
export default TogglableAddress;
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=togglableAddress.jsx.map