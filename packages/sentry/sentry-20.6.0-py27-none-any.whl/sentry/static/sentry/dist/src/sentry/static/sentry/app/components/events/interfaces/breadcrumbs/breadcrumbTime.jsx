import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import moment from 'moment';
import { defined } from 'app/utils';
import Tooltip from 'app/components/tooltip';
import getDynamicText from 'app/utils/getDynamicText';
var getBreadcrumbTimeTooltipTitle = function (timestamp) {
    var parsedTimestamp = moment(timestamp);
    var timestampFormat = parsedTimestamp.milliseconds() ? 'll H:mm:ss.SSS A' : 'lll';
    return parsedTimestamp.format(timestampFormat);
};
var BreadcrumbTime = function (_a) {
    var timestamp = _a.timestamp;
    return defined(timestamp) ? (<Tooltip title={getBreadcrumbTimeTooltipTitle(timestamp)}>
      <Time>
        {getDynamicText({
        value: moment(timestamp).format('HH:mm:ss'),
        fixed: '00:00:00',
    })}
      </Time>
    </Tooltip>) : null;
};
export default BreadcrumbTime;
var Time = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  font-size: ", ";\n  color: ", ";\n"], ["\n  font-size: ", ";\n  color: ", ";\n"])), function (p) { return p.theme.fontSizeSmall; }, function (p) { return p.theme.gray700; });
var templateObject_1;
//# sourceMappingURL=breadcrumbTime.jsx.map