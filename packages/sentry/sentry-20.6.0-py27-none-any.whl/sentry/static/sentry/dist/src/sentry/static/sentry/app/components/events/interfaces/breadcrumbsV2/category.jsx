import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import TextOverflow from 'app/components/textOverflow';
import Tooltip from 'app/components/tooltip';
import { defined } from 'app/utils';
import { t } from 'app/locale';
var Category = React.memo(function (_a) {
    var category = _a.category;
    var title = !defined(category) ? t('generic') : category;
    return (<Wrapper title={title}>
      <Tooltip title={title} containerDisplayMode="inline-flex">
        <TextOverflow>{title}</TextOverflow>
      </Tooltip>
    </Wrapper>);
});
export default Category;
var Wrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  color: ", ";\n  font-size: ", ";\n  font-weight: 700;\n"], ["\n  color: ", ";\n  font-size: ", ";\n  font-weight: 700;\n"])), function (p) { return p.theme.gray800; }, function (p) { return p.theme.fontSizeSmall; });
var templateObject_1;
//# sourceMappingURL=category.jsx.map