import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { tct } from 'app/locale';
import { IconEllipsis } from 'app/icons';
import { BreadCrumb, BreadCrumbIconWrapper } from './styles';
var BreadcrumbCollapsed = function (_a) {
    var quantity = _a.quantity, onClick = _a.onClick;
    return (<StyledBreadCrumb data-test-id="breadcrumb-collapsed" onClick={onClick}>
    <BreadCrumbIconWrapper>
      <IconEllipsis />
    </BreadCrumbIconWrapper>
    {tct('Show [quantity] collapsed crumbs', { quantity: quantity })}
  </StyledBreadCrumb>);
};
export default BreadcrumbCollapsed;
var StyledBreadCrumb = styled(BreadCrumb)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  cursor: pointer;\n  background: ", ";\n  margin: 0 -1px;\n  border-right: 1px solid ", ";\n  border-left: 1px solid ", ";\n"], ["\n  cursor: pointer;\n  background: ", ";\n  margin: 0 -1px;\n  border-right: 1px solid ", ";\n  border-left: 1px solid ", ";\n"])), function (p) { return p.theme.gray100; }, function (p) { return p.theme.borderLight; }, function (p) { return p.theme.borderLight; });
var templateObject_1;
//# sourceMappingURL=breadcrumbCollapsed.jsx.map