import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import space from 'app/styles/space';
import { t } from 'app/locale';
import Button from 'app/components/button';
import { IconChevron } from 'app/icons';
import RulesList from './rulesList';
var OrganizationRules = /** @class */ (function (_super) {
    __extends(OrganizationRules, _super);
    function OrganizationRules() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            isCollapsed: true,
        };
        _this.rulesListRef = React.createRef();
        _this.loadContentHeight = function () {
            var _a;
            if (!_this.state.contentHeight) {
                var contentHeight = (_a = _this.rulesListRef.current) === null || _a === void 0 ? void 0 : _a.offsetHeight;
                if (contentHeight) {
                    _this.setState({ contentHeight: contentHeight + "px" });
                }
            }
        };
        _this.handleToggleCollapsed = function () {
            _this.setState(function (prevState) { return ({
                isCollapsed: !prevState.isCollapsed,
            }); });
        };
        return _this;
    }
    OrganizationRules.prototype.componentDidUpdate = function () {
        this.loadContentHeight();
    };
    OrganizationRules.prototype.render = function () {
        var rules = this.props.rules;
        var _a = this.state, isCollapsed = _a.isCollapsed, contentHeight = _a.contentHeight;
        if (rules.length === 0) {
            return (<Wrapper>
          {t('There are no data scrubbing rules at the organization level')}
        </Wrapper>);
        }
        return (<Wrapper isCollapsed={isCollapsed} contentHeight={contentHeight}>
        <Header onClick={this.handleToggleCollapsed}>
          <div>{t('Organization Rules')}</div>
          <Button label={isCollapsed
            ? t('Expand Organization Rules')
            : t('Collapse Organization Rules')} icon={<IconChevron size="xs" direction={isCollapsed ? 'down' : 'up'}/>} size="xsmall"/>
        </Header>
        <Content>
          <RulesList rules={rules} ref={this.rulesListRef}/>
        </Content>
      </Wrapper>);
    };
    return OrganizationRules;
}(React.Component));
export default OrganizationRules;
var Content = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  transition: height 300ms cubic-bezier(0.4, 0, 0.2, 1) 0ms;\n  height: 0;\n  overflow: hidden;\n"], ["\n  transition: height 300ms cubic-bezier(0.4, 0, 0.2, 1) 0ms;\n  height: 0;\n  overflow: hidden;\n"])));
var Header = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  cursor: pointer;\n  display: grid;\n  grid-template-columns: 1fr auto;\n  align-items: center;\n  border-bottom: 1px solid ", ";\n  padding: ", " ", ";\n"], ["\n  cursor: pointer;\n  display: grid;\n  grid-template-columns: 1fr auto;\n  align-items: center;\n  border-bottom: 1px solid ", ";\n  padding: ", " ", ";\n"])), function (p) { return p.theme.borderDark; }, space(1), space(2));
var Wrapper = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  color: ", ";\n  background: ", ";\n  ", ";\n  ", ";\n  ", "\n"], ["\n  color: ", ";\n  background: ", ";\n  ", ";\n  ", ";\n  ",
    "\n"])), function (p) { return p.theme.gray400; }, function (p) { return p.theme.gray100; }, function (p) { return !p.contentHeight && "padding: " + space(1) + " " + space(2); }, function (p) { return !p.isCollapsed && " border-bottom: 1px solid " + p.theme.borderDark; }, function (p) {
    return !p.isCollapsed &&
        p.contentHeight &&
        "\n      " + Content + " {\n        height: " + p.contentHeight + ";\n      }\n    ";
});
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=organizationRules.jsx.map