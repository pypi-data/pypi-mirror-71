import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { t } from 'app/locale';
import TimeSince from 'app/components/timeSince';
import space from 'app/styles/space';
import { defined } from 'app/utils';
var Time = function (_a) {
    var label = _a.label, date = _a.date;
    return (<Wrapper>
    <TimeLabel>{label}</TimeLabel>
    {!defined(date) ? t('Unknown') : <TimeSince date={date}/>}
  </Wrapper>);
};
export default Time;
var Wrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: max-content 1fr;\n  grid-gap: ", ";\n  font-size: ", ";\n"], ["\n  display: grid;\n  grid-template-columns: max-content 1fr;\n  grid-gap: ", ";\n  font-size: ", ";\n"])), space(0.5), function (p) { return p.theme.fontSizeMedium; });
var TimeLabel = styled('h4')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  font-size: ", " !important;\n  text-transform: uppercase;\n  color: ", ";\n  margin-bottom: 0 !important;\n"], ["\n  font-size: ", " !important;\n  text-transform: uppercase;\n  color: ", ";\n  margin-bottom: 0 !important;\n"])), function (p) { return p.theme.fontSizeSmall; }, function (p) { return p.theme.gray500; });
var templateObject_1, templateObject_2;
//# sourceMappingURL=time.jsx.map