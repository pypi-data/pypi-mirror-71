import { __makeTemplateObject } from "tslib";
import styled from '@emotion/styled';
import space from 'app/styles/space';
import theme from 'app/utils/theme';
export var zIndex = {
    minimapContainer: theme.zIndex.traceView.minimapContainer,
    rowInfoMessage: theme.zIndex.traceView.rowInfoMessage,
    dividerLine: theme.zIndex.traceView.dividerLine,
    spanTreeToggler: theme.zIndex.traceView.spanTreeToggler,
};
export var SPAN_ROW_HEIGHT = 24;
export var SpanRow = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: ", ";\n  border-top: ", ";\n  margin-top: ", "; /* to prevent offset on toggle */\n  position: relative;\n  overflow: hidden;\n  min-height: ", "px;\n  cursor: pointer;\n  transition: background-color 0.15s ease-in-out;\n\n  &:last-child {\n    & > [data-component='span-detail'] {\n      border-bottom: none !important;\n    }\n  }\n"], ["\n  display: ", ";\n  border-top: ", ";\n  margin-top: ", "; /* to prevent offset on toggle */\n  position: relative;\n  overflow: hidden;\n  min-height: ", "px;\n  cursor: pointer;\n  transition: background-color 0.15s ease-in-out;\n\n  &:last-child {\n    & > [data-component='span-detail'] {\n      border-bottom: none !important;\n    }\n  }\n"])), function (p) { return (p.visible ? 'block' : 'none'); }, function (p) { return (p.showBorder ? "1px solid " + p.theme.gray400 : null); }, function (p) { return (p.showBorder ? '-1px' : null); }, SPAN_ROW_HEIGHT);
export var SpanRowMessage = styled(SpanRow)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: block;\n  cursor: auto;\n  line-height: ", "px;\n  padding-left: ", ";\n  padding-right: ", ";\n  color: ", ";\n  background-color: ", ";\n  outline: 1px solid ", ";\n  font-size: ", ";\n\n  z-index: ", ";\n\n  > * + * {\n    margin-left: ", ";\n  }\n"], ["\n  display: block;\n  cursor: auto;\n  line-height: ", "px;\n  padding-left: ", ";\n  padding-right: ", ";\n  color: ", ";\n  background-color: ", ";\n  outline: 1px solid ", ";\n  font-size: ", ";\n\n  z-index: ", ";\n\n  > * + * {\n    margin-left: ", ";\n  }\n"])), SPAN_ROW_HEIGHT, space(1), space(1), function (p) { return p.theme.gray500; }, function (p) { return p.theme.gray200; }, function (p) { return p.theme.borderDark; }, function (p) { return p.theme.fontSizeSmall; }, zIndex.rowInfoMessage, space(2));
var templateObject_1, templateObject_2;
//# sourceMappingURL=styles.jsx.map