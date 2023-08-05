import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import ActivityItem from 'app/components/activity/item';
import space from 'app/styles/space';
import theme from 'app/utils/theme';
var ActivityPlaceholder = function () { return (<ActivityItem bubbleProps={{
    backgroundColor: theme.placeholderBackground,
    borderColor: theme.placeholderBackground,
}}>
    {function () { return <Placeholder />; }}
  </ActivityItem>); };
var Placeholder = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  padding: ", ";\n"], ["\n  padding: ", ";\n"])), space(4));
export default ActivityPlaceholder;
var templateObject_1;
//# sourceMappingURL=activityPlaceholder.jsx.map