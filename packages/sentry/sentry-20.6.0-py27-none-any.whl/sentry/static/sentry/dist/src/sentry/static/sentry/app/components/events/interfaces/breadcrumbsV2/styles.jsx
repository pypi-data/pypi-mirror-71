import { __makeTemplateObject } from "tslib";
import styled from '@emotion/styled';
import { css } from '@emotion/core';
import theme from 'app/utils/theme';
import space from 'app/styles/space';
var IconWrapper = styled('div', {
    shouldForwardProp: function (prop) { return prop !== 'color'; },
})(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  width: 26px;\n  height: 26px;\n  background: ", ";\n  box-shadow: ", ";\n  border-radius: 32px;\n  z-index: ", ";\n  position: relative;\n  border: 1px solid ", ";\n  color: ", ";\n  ", "\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  width: 26px;\n  height: 26px;\n  background: ", ";\n  box-shadow: ", ";\n  border-radius: 32px;\n  z-index: ", ";\n  position: relative;\n  border: 1px solid ", ";\n  color: ", ";\n  ",
    "\n"])), function (p) { return p.theme.white; }, function (p) { return p.theme.dropShadowLightest; }, function (p) { return p.theme.zIndex.breadcrumbs.iconWrapper; }, function (p) { return p.theme.gray400; }, function (p) { return p.theme.gray800; }, function (p) {
    return p.color &&
        "\n      color: " + (p.theme[p.color] || p.color) + ";\n      border-color: " + (p.theme[p.color] || p.color) + ";\n    ";
});
var GridCell = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  position: relative;\n  border-bottom: 1px solid ", ";\n  margin-bottom: -1px;\n  text-overflow: ellipsis;\n  overflow: hidden;\n  padding: ", ";\n  @media (min-width: ", ") {\n    padding: ", " ", ";\n  }\n  ", "\n  ", ";\n"], ["\n  position: relative;\n  border-bottom: 1px solid ", ";\n  margin-bottom: -1px;\n  text-overflow: ellipsis;\n  overflow: hidden;\n  padding: ", ";\n  @media (min-width: ", ") {\n    padding: ", " ", ";\n  }\n  ",
    "\n  ", ";\n"])), function (p) { return p.theme.borderLight; }, space(1), function (p) { return p.theme.breakpoints[0]; }, space(1), space(2), function (p) {
    return p.hasError &&
        "\n      background: #fffcfb;\n      border-top: 1px solid #fa4747;\n      border-bottom: 1px solid #fa4747;\n      z-index: " + p.theme.zIndex.breadcrumbs.gridCellError + ";\n    ";
}, function (p) { return p.isLastItem && "border-bottom: none"; });
var GridCellLeft = styled(GridCell)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  align-items: center;\n  line-height: 1;\n  padding: ", " ", " ", " ", ";\n  :before {\n    content: '';\n    display: block;\n    width: 1px;\n    top: 0;\n    bottom: 0;\n    left: 21px;\n    background: ", ";\n    position: absolute;\n    @media (min-width: ", ") {\n      left: 29px;\n    }\n  }\n"], ["\n  align-items: center;\n  line-height: 1;\n  padding: ", " ", " ", " ", ";\n  :before {\n    content: '';\n    display: block;\n    width: 1px;\n    top: 0;\n    bottom: 0;\n    left: 21px;\n    background: ", ";\n    position: absolute;\n    @media (min-width: ", ") {\n      left: 29px;\n    }\n  }\n"])), space(1), space(0.5), space(1), space(1), function (p) { return (p.hasError ? '#fa4747' : p.theme.borderLight); }, function (p) { return p.theme.breakpoints[0]; });
var aroundContentStyle = css(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  border: 1px solid ", ";\n  border-radius: ", ";\n  box-shadow: ", ";\n"], ["\n  border: 1px solid ", ";\n  border-radius: ", ";\n  box-shadow: ", ";\n"])), theme.borderDark, theme.borderRadius, theme.dropShadowLightest);
export { GridCell, GridCellLeft, IconWrapper, aroundContentStyle };
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=styles.jsx.map