import { __makeTemplateObject } from "tslib";
import React from 'react';
import PropTypes from 'prop-types';
import styled from '@emotion/styled';
import DropdownButton from 'app/components/dropdownButton';
import { InlineContainer, SectionHeading } from 'app/components/charts/styles';
import DropdownControl, { DropdownItem } from 'app/components/dropdownControl';
import space from 'app/styles/space';
function OptionSelector(_a) {
    var options = _a.options, onChange = _a.onChange, selected = _a.selected, title = _a.title, _b = _a.menuWidth, menuWidth = _b === void 0 ? 'auto' : _b;
    var selectedOption = options.find(function (opt) { return selected === opt.value; }) || options[0];
    return (<InlineContainer>
      <SectionHeading>{title}</SectionHeading>
      <DropdownControl menuWidth={menuWidth} alignRight button={function (_a) {
        var getActorProps = _a.getActorProps;
        return (<StyledDropdownButton {...getActorProps()} size="zero" isOpen={false}>
            {selectedOption.label}
          </StyledDropdownButton>);
    }}>
        {options.map(function (opt) { return (<DropdownItem key={opt.value} onSelect={onChange} eventKey={opt.value} disabled={opt.disabled} isActive={selected === opt.value} data-test-id={"option-" + opt.value}>
            {opt.label}
          </DropdownItem>); })}
      </DropdownControl>
    </InlineContainer>);
}
var StyledDropdownButton = styled(DropdownButton)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  padding: ", " ", ";\n  font-weight: normal;\n  color: ", ";\n\n  &:hover,\n  &:focus,\n  &:active {\n    color: ", ";\n  }\n"], ["\n  padding: ", " ", ";\n  font-weight: normal;\n  color: ", ";\n\n  &:hover,\n  &:focus,\n  &:active {\n    color: ", ";\n  }\n"])), space(1), space(2), function (p) { return p.theme.gray600; }, function (p) { return p.theme.gray700; });
OptionSelector.propTypes = {
    options: PropTypes.array.isRequired,
    onChange: PropTypes.func.isRequired,
    title: PropTypes.string.isRequired,
    selected: PropTypes.string,
};
export default OptionSelector;
var templateObject_1;
//# sourceMappingURL=optionSelector.jsx.map