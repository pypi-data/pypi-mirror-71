import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Tag from 'app/views/settings/components/tag';
import { t } from 'app/locale';
import { BreadcrumbLevelType } from './types';
var Level = React.memo(function (_a) {
    var level = _a.level;
    switch (level) {
        case BreadcrumbLevelType.FATAL:
            return <StyledTag color="red500">{level}</StyledTag>;
        case BreadcrumbLevelType.ERROR:
            return <StyledTag color="red400">{level}</StyledTag>;
        case BreadcrumbLevelType.INFO:
            return <StyledTag color="blue400">{level}</StyledTag>;
        case BreadcrumbLevelType.WARNING:
            return <StyledTag color="orange400">{level}</StyledTag>;
        default:
            return <Tag>{level || t('undefined')}</Tag>;
    }
});
export default Level;
// TODO(style): Update the tag component with the new colors
var StyledTag = styled(Tag)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  background-color: ", ";\n  color: ", ";\n"], ["\n  background-color: ", ";\n  color: ", ";\n"])), function (p) { return p.theme[p.color]; }, function (p) { return p.theme.white; });
var templateObject_1;
//# sourceMappingURL=level.jsx.map