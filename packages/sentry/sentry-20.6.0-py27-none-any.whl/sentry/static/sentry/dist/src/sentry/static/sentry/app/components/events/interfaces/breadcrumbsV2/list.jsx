import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import space from 'app/styles/space';
import ListHeader from './listHeader';
import ListBody from './listBody';
import { aroundContentStyle } from './styles';
var List = React.forwardRef(function (_a, ref) {
    var displayRelativeTime = _a.displayRelativeTime, onSwitchTimeFormat = _a.onSwitchTimeFormat, orgId = _a.orgId, event = _a.event, breadcrumbs = _a.breadcrumbs;
    var _b;
    return (<Grid ref={ref}>
      <ListHeader onSwitchTimeFormat={onSwitchTimeFormat} displayRelativeTime={!!displayRelativeTime}/>
      <ListBody event={event} orgId={orgId} breadcrumbs={breadcrumbs} relativeTime={(_b = breadcrumbs[breadcrumbs.length - 1]) === null || _b === void 0 ? void 0 : _b.timestamp} displayRelativeTime={!!displayRelativeTime}/>
    </Grid>);
});
export default List;
var Grid = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  max-height: 500px;\n  overflow-y: auto;\n  display: grid;\n  > *:nth-last-child(5):before {\n    bottom: calc(100% - ", ");\n  }\n  grid-template-columns: max-content minmax(55px, 1fr) 6fr max-content 65px;\n  @media (min-width: ", ") {\n    grid-template-columns: max-content minmax(132px, 1fr) 6fr max-content max-content;\n  }\n  ", "\n"], ["\n  max-height: 500px;\n  overflow-y: auto;\n  display: grid;\n  > *:nth-last-child(5):before {\n    bottom: calc(100% - ", ");\n  }\n  grid-template-columns: max-content minmax(55px, 1fr) 6fr max-content 65px;\n  @media (min-width: ", ") {\n    grid-template-columns: max-content minmax(132px, 1fr) 6fr max-content max-content;\n  }\n  ", "\n"])), space(1), function (p) { return p.theme.breakpoints[0]; }, aroundContentStyle);
var templateObject_1;
//# sourceMappingURL=list.jsx.map