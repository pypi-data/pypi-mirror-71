import { __makeTemplateObject } from "tslib";
import PropTypes from 'prop-types';
import React from 'react';
import styled from '@emotion/styled';
import HeroIcon from 'app/components/heroIcon';
import EmptyMessage from 'app/views/settings/components/emptyMessage';
import { IconWarning } from 'app/icons';
import space from 'app/styles/space';
var EmptyStateWarning = function (_a) {
    var _b = _a.small, small = _b === void 0 ? false : _b, _c = _a.withIcon, withIcon = _c === void 0 ? true : _c, children = _a.children, className = _a.className;
    return small ? (<EmptyMessage className={className}>
      <SmallMessage>
        {withIcon && <StyledIconWarning color="gray500" size="lg"/>}
        {children}
      </SmallMessage>
    </EmptyMessage>) : (<EmptyStreamWrapper data-test-id="empty-state" className={className}>
      {withIcon && <HeroIcon src="icon-circle-exclamation" size="54"/>}
      {children}
    </EmptyStreamWrapper>);
};
EmptyStateWarning.propTypes = {
    small: PropTypes.bool,
};
var EmptyStreamWrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  text-align: center;\n  font-size: 22px;\n  padding: 48px 0;\n\n  p {\n    line-height: 1.2;\n    margin: 0 auto 20px;\n    &:last-child {\n      margin-bottom: 0;\n    }\n  }\n\n  ", " {\n    margin-bottom: 20px;\n  }\n"], ["\n  text-align: center;\n  font-size: 22px;\n  padding: 48px 0;\n\n  p {\n    line-height: 1.2;\n    margin: 0 auto 20px;\n    &:last-child {\n      margin-bottom: 0;\n    }\n  }\n\n  ", " {\n    margin-bottom: 20px;\n  }\n"])), HeroIcon);
var SmallMessage = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  color: ", ";\n  font-size: ", ";\n  line-height: 1em;\n"], ["\n  display: flex;\n  align-items: center;\n  color: ", ";\n  font-size: ", ";\n  line-height: 1em;\n"])), function (p) { return p.theme.gray500; }, function (p) { return p.theme.fontSizeExtraLarge; });
var StyledIconWarning = styled(IconWarning)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  margin-right: ", ";\n"], ["\n  margin-right: ", ";\n"])), space(1));
export default EmptyStateWarning;
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=emptyStateWarning.jsx.map