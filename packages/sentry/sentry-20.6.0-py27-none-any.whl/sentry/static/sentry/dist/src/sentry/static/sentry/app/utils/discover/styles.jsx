import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import DateTime from 'app/components/dateTime';
import Link from 'app/components/links/link';
import ShortId from 'app/components/shortId';
import overflowEllipsis from 'app/styles/overflowEllipsis';
import space from 'app/styles/space';
/**
 * Styled components used to render discover result sets.
 */
export var Container = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  ", ";\n"], ["\n  ", ";\n"])), overflowEllipsis);
export var VersionContainer = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  ", ";\n  max-width: 100%;\n  width: auto;\n  display: inline-block;\n"], ["\n  ", ";\n  max-width: 100%;\n  width: auto;\n  display: inline-block;\n"])), overflowEllipsis);
export var NumberContainer = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  text-align: right;\n  ", ";\n"], ["\n  text-align: right;\n  ", ";\n"])), overflowEllipsis);
export var StyledDateTime = styled(DateTime)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  color: ", ";\n  ", ";\n"], ["\n  color: ", ";\n  ", ";\n"])), function (p) { return p.theme.gray500; }, overflowEllipsis);
export var OverflowLink = styled(Link)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  ", ";\n"], ["\n  ", ";\n"])), overflowEllipsis);
/* Layout containers for discover and performance views */
export var ContentBox = styled('div')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  padding: ", " ", ";\n  margin: 0;\n  background-color: ", ";\n  flex-grow: 1;\n\n  @media (min-width: ", ") {\n    display: grid;\n    grid-template-columns: 66% auto;\n    align-content: start;\n    grid-gap: ", ";\n  }\n\n  @media (min-width: ", ") {\n    grid-template-columns: minmax(100px, auto) 325px;\n  }\n"], ["\n  padding: ", " ", ";\n  margin: 0;\n  background-color: ", ";\n  flex-grow: 1;\n\n  @media (min-width: ", ") {\n    display: grid;\n    grid-template-columns: 66% auto;\n    align-content: start;\n    grid-gap: ", ";\n  }\n\n  @media (min-width: ", ") {\n    grid-template-columns: minmax(100px, auto) 325px;\n  }\n"])), space(2), space(4), function (p) { return p.theme.white; }, function (p) { return p.theme.breakpoints[1]; }, space(3), function (p) { return p.theme.breakpoints[2]; });
export var Main = styled('div')(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  grid-column: 1/2;\n  max-width: 100%;\n  overflow: hidden;\n"], ["\n  grid-column: 1/2;\n  max-width: 100%;\n  overflow: hidden;\n"])));
export var Side = styled('div')(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  grid-column: 2/3;\n"], ["\n  grid-column: 2/3;\n"])));
export var HeaderBox = styled(ContentBox)(templateObject_9 || (templateObject_9 = __makeTemplateObject(["\n  border-bottom: 1px solid ", ";\n  grid-row-gap: ", ";\n  background-color: transparent;\n  flex-grow: 0;\n"], ["\n  border-bottom: 1px solid ", ";\n  grid-row-gap: ", ";\n  background-color: transparent;\n  flex-grow: 0;\n"])), function (p) { return p.theme.borderDark; }, space(1));
export var HeaderTopControls = styled('div')(templateObject_10 || (templateObject_10 = __makeTemplateObject(["\n  display: flex;\n  justify-self: end;\n  grid-row: 1/2;\n  grid-column: 2/3;\n"], ["\n  display: flex;\n  justify-self: end;\n  grid-row: 1/2;\n  grid-column: 2/3;\n"])));
export var HeaderBottomControls = styled('div')(templateObject_11 || (templateObject_11 = __makeTemplateObject(["\n  display: flex;\n  justify-self: end;\n  justify-content: flex-end;\n  grid-row: 2/3;\n  grid-column: 2/3;\n"], ["\n  display: flex;\n  justify-self: end;\n  justify-content: flex-end;\n  grid-row: 2/3;\n  grid-column: 2/3;\n"])));
export var StyledShortId = styled(ShortId)(templateObject_12 || (templateObject_12 = __makeTemplateObject(["\n  justify-content: flex-start;\n"], ["\n  justify-content: flex-start;\n"])));
export var BarContainer = styled('div')(templateObject_13 || (templateObject_13 = __makeTemplateObject(["\n  max-width: 80px;\n  margin-left: auto;\n"], ["\n  max-width: 80px;\n  margin-left: auto;\n"])));
export var EventId = function (_a) {
    var value = _a.value;
    var shortId = value.substring(0, 8);
    return <React.Fragment>{shortId}</React.Fragment>;
};
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10, templateObject_11, templateObject_12, templateObject_13;
//# sourceMappingURL=styles.jsx.map