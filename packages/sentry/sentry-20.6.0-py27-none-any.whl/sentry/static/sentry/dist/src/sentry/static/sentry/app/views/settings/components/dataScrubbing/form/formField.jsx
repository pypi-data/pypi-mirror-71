import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import QuestionTooltip from 'app/components/questionTooltip';
import space from 'app/styles/space';
var FormField = function (_a) {
    var label = _a.label, tooltipInfo = _a.tooltipInfo, children = _a.children, isFullWidth = _a.isFullWidth;
    return (<Wrapper isFullWidth={isFullWidth}>
    <Label>
      <LabelDescription>{label}</LabelDescription>
      <QuestionTooltip title={tooltipInfo} position="top" size="sm"/>
    </Label>
    {children}
  </Wrapper>);
};
export default FormField;
var Wrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  ", "\n"], ["\n  ",
    "\n"])), function (p) {
    return p.isFullWidth &&
        "\n      grid-column-start: 1;\n      grid-column-end: -1;\n    ";
});
var Label = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  margin-bottom: ", ";\n"], ["\n  display: flex;\n  align-items: center;\n  margin-bottom: ", ";\n"])), space(0.5));
var LabelDescription = styled('span')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  margin-right: ", ";\n"], ["\n  margin-right: ", ";\n"])), space(1));
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=formField.jsx.map