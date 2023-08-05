import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import space from 'app/styles/space';
import { t, tct } from 'app/locale';
import CheckboxFancy from 'app/components/checkboxFancy/checkboxFancy';
var Header = function (_a) {
    var checkedQuantity = _a.checkedQuantity, isAllChecked = _a.isAllChecked, onCheckAll = _a.onCheckAll;
    var handleClick = function (event) {
        event.stopPropagation();
        if (isAllChecked) {
            onCheckAll(false);
            return;
        }
        onCheckAll(true);
    };
    var getCheckboxLabel = function () {
        if (isAllChecked) {
            return t('Uncheck All');
        }
        if (checkedQuantity === 0) {
            return t('Check All');
        }
        return tct('[checkedQuantity] checked', { checkedQuantity: checkedQuantity });
    };
    return (<Wrapper>
      <CheckboxWrapper onClick={handleClick}>
        <span>{getCheckboxLabel()}</span>
        <CheckboxFancy isChecked={isAllChecked} isIndeterminate={!isAllChecked && checkedQuantity > 0}/>
      </CheckboxWrapper>
    </Wrapper>);
};
export default Header;
var Wrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  background-color: ", ";\n  padding: ", " ", ";\n  border-bottom: 1px solid ", ";\n  justify-content: flex-end;\n"], ["\n  display: flex;\n  background-color: ", ";\n  padding: ", " ", ";\n  border-bottom: 1px solid ", ";\n  justify-content: flex-end;\n"])), function (p) { return p.theme.gray100; }, space(1), space(2), function (p) { return p.theme.borderDark; });
var CheckboxWrapper = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  text-align: right;\n  align-items: center;\n  display: grid;\n  grid-gap: ", ";\n  grid-template-columns: minmax(100px, auto) 16px;\n  font-size: ", ";\n"], ["\n  text-align: right;\n  align-items: center;\n  display: grid;\n  grid-gap: ", ";\n  grid-template-columns: minmax(100px, auto) 16px;\n  font-size: ", ";\n"])), space(1), function (p) { return p.theme.fontSizeMedium; });
var templateObject_1, templateObject_2;
//# sourceMappingURL=header.jsx.map