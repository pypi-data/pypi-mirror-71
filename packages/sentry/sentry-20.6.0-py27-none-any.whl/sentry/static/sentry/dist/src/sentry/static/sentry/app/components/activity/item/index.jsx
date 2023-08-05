import { __makeTemplateObject } from "tslib";
import PropTypes from 'prop-types';
import React from 'react';
import styled from '@emotion/styled';
import DateTime from 'app/components/dateTime';
import TimeSince from 'app/components/timeSince';
import space from 'app/styles/space';
import textStyles from 'app/styles/text';
import { isRenderFunc } from 'app/utils/isRenderFunc';
import ActivityAvatar from './avatar';
import ActivityBubble from './bubble';
function ActivityItem(_a) {
    var author = _a.author, avatarSize = _a.avatarSize, bubbleProps = _a.bubbleProps, className = _a.className, children = _a.children, date = _a.date, footer = _a.footer, id = _a.id, header = _a.header, _b = _a.hideDate, hideDate = _b === void 0 ? false : _b, _c = _a.showTime, showTime = _c === void 0 ? false : _c;
    var showDate = !hideDate && date;
    return (<ActivityItemWrapper data-test-id="activity-item" className={className}>
      {id && <a id={id}/>}

      {author && (<StyledActivityAvatar type={author.type} user={author.user} size={avatarSize}/>)}

      <ActivityBubble {...bubbleProps}>
        {header && isRenderFunc(header) && header()}
        {header && !isRenderFunc(header) && (<ActivityHeader>
            <ActivityHeaderContent>{header}</ActivityHeaderContent>

            {date && showDate && !showTime && <StyledTimeSince date={date}/>}
            {date && showDate && showTime && <StyledDateTime timeOnly date={date}/>}
          </ActivityHeader>)}

        {children && isRenderFunc(children) && children()}
        {children && !isRenderFunc(children) && (<ActivityBody>{children}</ActivityBody>)}

        {footer && isRenderFunc(footer) && footer()}
        {footer && !isRenderFunc(footer) && (<ActivityFooter>{footer}</ActivityFooter>)}
      </ActivityBubble>
    </ActivityItemWrapper>);
}
ActivityItem.propTypes = {
    id: PropTypes.string,
    date: PropTypes.oneOfType([PropTypes.instanceOf(Date), PropTypes.string]),
    author: PropTypes.shape({
        type: ActivityAvatar.propTypes.type,
        user: ActivityAvatar.propTypes.user,
    }),
    avatarSize: PropTypes.number,
    hideDate: PropTypes.bool,
    showTime: PropTypes.bool,
    header: PropTypes.oneOfType([PropTypes.node, PropTypes.func]),
    footer: PropTypes.oneOfType([PropTypes.node, PropTypes.func]),
    bubbleProps: PropTypes.shape(ActivityBubble.propTypes),
};
var ActivityItemWrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  margin-bottom: ", ";\n"], ["\n  display: flex;\n  margin-bottom: ", ";\n"])), space(2));
var HeaderAndFooter = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  padding: 6px ", ";\n"], ["\n  padding: 6px ", ";\n"])), space(2));
var ActivityHeader = styled(HeaderAndFooter)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: flex;\n  border-bottom: 1px solid ", ";\n  font-size: ", ";\n\n  &:last-child {\n    border-bottom: none;\n  }\n"], ["\n  display: flex;\n  border-bottom: 1px solid ", ";\n  font-size: ", ";\n\n  &:last-child {\n    border-bottom: none;\n  }\n"])), function (p) { return p.theme.borderLight; }, function (p) { return p.theme.fontSizeMedium; });
var ActivityHeaderContent = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  flex: 1;\n"], ["\n  flex: 1;\n"])));
var ActivityFooter = styled(HeaderAndFooter)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  display: flex;\n  border-top: 1px solid ", ";\n  font-size: ", ";\n"], ["\n  display: flex;\n  border-top: 1px solid ", ";\n  font-size: ", ";\n"])), function (p) { return p.theme.borderLight; }, function (p) { return p.theme.fontSizeMedium; });
var ActivityBody = styled('div')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  padding: ", " ", ";\n  word-break: break-all;\n  ", "\n"], ["\n  padding: ", " ", ";\n  word-break: break-all;\n  ", "\n"])), space(2), space(2), textStyles);
var StyledActivityAvatar = styled(ActivityAvatar)(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  margin-right: ", ";\n"], ["\n  margin-right: ", ";\n"])), space(1));
var StyledTimeSince = styled(TimeSince)(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (p) { return p.theme.gray500; });
var StyledDateTime = styled(DateTime)(templateObject_9 || (templateObject_9 = __makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (p) { return p.theme.gray500; });
export default ActivityItem;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9;
//# sourceMappingURL=index.jsx.map