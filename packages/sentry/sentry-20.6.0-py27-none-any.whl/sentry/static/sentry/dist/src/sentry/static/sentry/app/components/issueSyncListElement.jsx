import { __extends, __makeTemplateObject } from "tslib";
import { ClassNames } from '@emotion/core';
import PropTypes from 'prop-types';
import React from 'react';
import styled from '@emotion/styled';
import capitalize from 'lodash/capitalize';
import InlineSvg from 'app/components/inlineSvg';
import { IconBitbucket, IconGeneric, IconGithub, IconGitlab, IconJira, IconVsts, } from 'app/icons';
import space from 'app/styles/space';
import Hovercard from 'app/components/hovercard';
import { callIfFunction } from 'app/utils/callIfFunction';
var IssueSyncListElement = /** @class */ (function (_super) {
    __extends(IssueSyncListElement, _super);
    function IssueSyncListElement() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleDelete = function () {
            callIfFunction(_this.props.onClose, _this.props.externalIssueId);
        };
        return _this;
    }
    IssueSyncListElement.prototype.isLinked = function () {
        return !!(this.props.externalIssueLink && this.props.externalIssueId);
    };
    IssueSyncListElement.prototype.getIcon = function () {
        switch (this.props.integrationType) {
            case 'bitbucket':
                return <IconBitbucket size="md"/>;
            case 'gitlab':
                return <IconGitlab size="md"/>;
            case 'github':
                return <IconGithub size="md"/>;
            case 'github_enterprise':
                return <IconGithub size="md"/>;
            case 'jira':
            case 'jira_server':
                return <IconJira size="md"/>;
            case 'vsts':
                return <IconVsts size="md"/>;
            default:
                return <IconGeneric size="md"/>;
        }
    };
    IssueSyncListElement.prototype.getPrettyName = function () {
        var type = this.props.integrationType;
        switch (type) {
            case 'gitlab':
                return 'GitLab';
            case 'github':
                return 'GitHub';
            case 'github_enterprise':
                return 'GitHub Enterprise';
            case 'vsts':
                return 'Azure DevOps';
            case 'jira_server':
                return 'Jira Server';
            default:
                return capitalize(type);
        }
    };
    IssueSyncListElement.prototype.getLink = function () {
        return (<IntegrationLink href={this.props.externalIssueLink || undefined} onClick={!this.isLinked() ? this.props.onOpen : undefined}>
        {this.getText()}
      </IntegrationLink>);
    };
    IssueSyncListElement.prototype.getText = function () {
        if (this.props.children) {
            return this.props.children;
        }
        if (this.props.externalIssueDisplayName) {
            return this.props.externalIssueDisplayName;
        }
        if (this.props.externalIssueKey) {
            return this.props.externalIssueKey;
        }
        return "Link " + this.getPrettyName() + " Issue";
    };
    IssueSyncListElement.prototype.render = function () {
        var _this = this;
        return (<IssueSyncListElementContainer>
        <ClassNames>
          {function (_a) {
            var css = _a.css;
            return (<Hovercard containerClassName={css(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n                display: flex;\n                align-items: center;\n                min-width: 0; /* flex-box overflow workaround */\n              "], ["\n                display: flex;\n                align-items: center;\n                min-width: 0; /* flex-box overflow workaround */\n              "])))} header={_this.props.hoverCardHeader} body={_this.props.hoverCardBody}>
              {_this.getIcon()}
              {_this.getLink()}
            </Hovercard>);
        }}
        </ClassNames>
        {this.props.onOpen && this.props.onClose && (<OpenCloseIcon src="icon-close" onClick={this.isLinked() ? this.handleDelete : this.props.onOpen} isLinked={this.isLinked()}/>)}
      </IssueSyncListElementContainer>);
    };
    IssueSyncListElement.propTypes = {
        externalIssueLink: PropTypes.string,
        externalIssueId: PropTypes.oneOfType([PropTypes.number, PropTypes.string]),
        externalIssueKey: PropTypes.string,
        externalIssueDisplayName: PropTypes.string,
        onOpen: PropTypes.func,
        onClose: PropTypes.func,
        integrationType: PropTypes.string,
        hoverCardHeader: PropTypes.node,
        hoverCardBody: PropTypes.node,
    };
    return IssueSyncListElement;
}(React.Component));
export var IssueSyncListElementContainer = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  line-height: 0;\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n\n  &:not(:last-child) {\n    margin-bottom: ", ";\n  }\n"], ["\n  line-height: 0;\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n\n  &:not(:last-child) {\n    margin-bottom: ", ";\n  }\n"])), space(2));
export var IntegrationLink = styled('a')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  text-decoration: none;\n  padding-bottom: ", ";\n  margin-left: ", ";\n  color: ", ";\n  border-bottom: 1px solid ", ";\n  cursor: pointer;\n  line-height: 1;\n  white-space: nowrap;\n  overflow: hidden;\n  text-overflow: ellipsis;\n\n  &,\n  &:hover {\n    border-bottom: 1px solid ", ";\n  }\n"], ["\n  text-decoration: none;\n  padding-bottom: ", ";\n  margin-left: ", ";\n  color: ", ";\n  border-bottom: 1px solid ", ";\n  cursor: pointer;\n  line-height: 1;\n  white-space: nowrap;\n  overflow: hidden;\n  text-overflow: ellipsis;\n\n  &,\n  &:hover {\n    border-bottom: 1px solid ", ";\n  }\n"])), space(0.25), space(1), function (p) { return p.theme.gray700; }, function (p) { return p.theme.gray700; }, function (p) { return p.theme.blue400; });
export var OpenCloseIcon = styled(InlineSvg)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  height: ", ";\n  color: ", ";\n  transition: 0.2s transform;\n  cursor: pointer;\n  box-sizing: content-box;\n  padding: ", ";\n  margin: -", ";\n  ", ";\n"], ["\n  height: ", ";\n  color: ", ";\n  transition: 0.2s transform;\n  cursor: pointer;\n  box-sizing: content-box;\n  padding: ", ";\n  margin: -", ";\n  ", ";\n"])), space(1.5), function (p) { return p.theme.gray700; }, space(1), space(1), function (p) { return (p.isLinked ? '' : 'transform: rotate(45deg) scale(0.9);'); });
export default IssueSyncListElement;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=issueSyncListElement.jsx.map