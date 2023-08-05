import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import space from 'app/styles/space';
import { IconFire, IconWarning, IconCheckmark } from 'app/icons';
import { displayCrashFreePercent } from '../utils';
var CRASH_FREE_DANGER_THRESHOLD = 98;
var CRASH_FREE_WARNING_THRESHOLD = 99.5;
var getIcon = function (percent) {
    if (percent < CRASH_FREE_DANGER_THRESHOLD) {
        return <IconFire color="red400"/>;
    }
    if (percent < CRASH_FREE_WARNING_THRESHOLD) {
        return <IconWarning color="yellow400"/>;
    }
    return <IconCheckmark isCircled color="green400"/>;
};
var CrashFree = function (_a) {
    var percent = _a.percent;
    return (<Wrapper>
      {getIcon(percent)}
      {displayCrashFreePercent(percent)}
    </Wrapper>);
};
var Wrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: inline-grid;\n  grid-auto-flow: column;\n  grid-gap: ", ";\n  align-items: center;\n"], ["\n  display: inline-grid;\n  grid-auto-flow: column;\n  grid-gap: ", ";\n  align-items: center;\n"])), space(0.75));
export default CrashFree;
var templateObject_1;
//# sourceMappingURL=crashFree.jsx.map