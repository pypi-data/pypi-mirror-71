import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import PropTypes from 'prop-types';
import Modal from 'react-bootstrap/lib/Modal';
import styled from '@emotion/styled';
import withApi from 'app/utils/withApi';
import InlineSvg from 'app/components/inlineSvg';
import { addSuccessMessage, addErrorMessage } from 'app/actionCreators/indicator';
import { IntegrationLink } from 'app/components/issueSyncListElement';
import { SentryAppIcon } from 'app/components/sentryAppIcon';
import SentryAppExternalIssueForm from 'app/components/group/sentryAppExternalIssueForm';
import NavTabs from 'app/components/navTabs';
import { t, tct } from 'app/locale';
import SentryTypes from 'app/sentryTypes';
import space from 'app/styles/space';
import { deleteExternalIssue } from 'app/actionCreators/platformExternalIssues';
import { recordInteraction } from 'app/utils/recordSentryAppInteraction';
var SentryAppExternalIssueActions = /** @class */ (function (_super) {
    __extends(SentryAppExternalIssueActions, _super);
    function SentryAppExternalIssueActions(props) {
        var _this = _super.call(this, props) || this;
        _this.showModal = function () {
            // Only show the modal when we don't have a linked issue
            if (!_this.state.externalIssue) {
                var sentryAppComponent = _this.props.sentryAppComponent;
                recordInteraction(sentryAppComponent.sentryApp.slug, 'sentry_app_component_interacted', {
                    componentType: 'issue-link',
                });
                _this.setState({ showModal: true });
            }
        };
        _this.hideModal = function () {
            _this.setState({ showModal: false });
        };
        _this.showLink = function () {
            _this.setState({ action: 'link' });
        };
        _this.showCreate = function () {
            _this.setState({ action: 'create' });
        };
        _this.deleteIssue = function () {
            var _a = _this.props, api = _a.api, group = _a.group;
            var externalIssue = _this.state.externalIssue;
            externalIssue &&
                deleteExternalIssue(api, group.id, externalIssue.id)
                    .then(function (_data) {
                    _this.setState({ externalIssue: undefined });
                    addSuccessMessage(t('Successfully unlinked issue.'));
                })
                    .catch(function (_error) {
                    addErrorMessage(t('Unable to unlink issue.'));
                });
        };
        _this.onAddRemoveClick = function () {
            var externalIssue = _this.state.externalIssue;
            if (!externalIssue) {
                _this.showModal();
            }
            else {
                _this.deleteIssue();
            }
        };
        _this.onSubmitSuccess = function (externalIssue) {
            _this.setState({ externalIssue: externalIssue });
            _this.hideModal();
        };
        _this.state = {
            action: 'create',
            externalIssue: props.externalIssue,
            showModal: false,
        };
        return _this;
    }
    SentryAppExternalIssueActions.prototype.componentDidUpdate = function (prevProps) {
        if (this.props.externalIssue !== prevProps.externalIssue) {
            this.updateExternalIssue(this.props.externalIssue);
        }
    };
    SentryAppExternalIssueActions.prototype.updateExternalIssue = function (externalIssue) {
        this.setState({ externalIssue: externalIssue });
    };
    Object.defineProperty(SentryAppExternalIssueActions.prototype, "link", {
        get: function () {
            var sentryAppComponent = this.props.sentryAppComponent;
            var externalIssue = this.state.externalIssue;
            var name = sentryAppComponent.sentryApp.name;
            var url = '#';
            var displayName = tct('Link [name] Issue', { name: name });
            if (externalIssue) {
                url = externalIssue.webUrl;
                displayName = externalIssue.displayName;
            }
            return (<IssueLinkContainer>
        <IssueLink>
          <StyledSentryAppIcon slug={sentryAppComponent.sentryApp.slug}/>
          <IntegrationLink onClick={this.showModal} href={url}>
            {displayName}
          </IntegrationLink>
        </IssueLink>
        <AddRemoveIcon src="icon-close" isLinked={!!externalIssue} onClick={this.onAddRemoveClick}/>
      </IssueLinkContainer>);
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(SentryAppExternalIssueActions.prototype, "modal", {
        get: function () {
            var _a = this.props, sentryAppComponent = _a.sentryAppComponent, sentryAppInstallation = _a.sentryAppInstallation, group = _a.group;
            var _b = this.state, action = _b.action, showModal = _b.showModal;
            var name = sentryAppComponent.sentryApp.name;
            var config = sentryAppComponent.schema[action];
            return (<Modal show={showModal} onHide={this.hideModal} animation={false}>
        <Modal.Header closeButton>
          <Modal.Title>{tct('[name] Issue', { name: name })}</Modal.Title>
        </Modal.Header>
        <NavTabs underlined>
          <li className={action === 'create' ? 'active create' : 'create'}>
            <a onClick={this.showCreate}>{t('Create')}</a>
          </li>
          <li className={action === 'link' ? 'active link' : 'link'}>
            <a onClick={this.showLink}>{t('Link')}</a>
          </li>
        </NavTabs>
        <Modal.Body>
          <SentryAppExternalIssueForm group={group} sentryAppInstallation={sentryAppInstallation} appName={name} config={config} action={action} onSubmitSuccess={this.onSubmitSuccess} event={this.props.event}/>
        </Modal.Body>
      </Modal>);
        },
        enumerable: true,
        configurable: true
    });
    SentryAppExternalIssueActions.prototype.render = function () {
        return (<React.Fragment>
        {this.link}
        {this.modal}
      </React.Fragment>);
    };
    SentryAppExternalIssueActions.propTypes = {
        api: PropTypes.object.isRequired,
        group: SentryTypes.Group.isRequired,
        sentryAppComponent: PropTypes.object.isRequired,
        sentryAppInstallation: PropTypes.object.isRequired,
        externalIssue: PropTypes.object,
        event: SentryTypes.Event,
    };
    return SentryAppExternalIssueActions;
}(React.Component));
// @ts-ignore ; TS2589: Type instantiation is excessively deep and possibly infinite.
var StyledSentryAppIcon = styled(SentryAppIcon)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  color: ", ";\n  width: ", ";\n  height: ", ";\n  cursor: pointer;\n  flex-shrink: 0;\n"], ["\n  color: ", ";\n  width: ", ";\n  height: ", ";\n  cursor: pointer;\n  flex-shrink: 0;\n"])), function (p) { return p.theme.gray700; }, space(3), space(3));
var IssueLink = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  min-width: 0;\n"], ["\n  display: flex;\n  align-items: center;\n  min-width: 0;\n"])));
var IssueLinkContainer = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  line-height: 0;\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  margin-bottom: 16px;\n"], ["\n  line-height: 0;\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  margin-bottom: 16px;\n"])));
var AddRemoveIcon = styled(InlineSvg)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  height: ", ";\n  color: ", ";\n  transition: 0.2s transform;\n  cursor: pointer;\n  box-sizing: content-box;\n  padding: ", ";\n  margin: -", ";\n  ", ";\n"], ["\n  height: ", ";\n  color: ", ";\n  transition: 0.2s transform;\n  cursor: pointer;\n  box-sizing: content-box;\n  padding: ", ";\n  margin: -", ";\n  ", ";\n"])), space(1.5), function (p) { return p.theme.gray700; }, space(1), space(1), function (p) { return (p.isLinked ? '' : 'transform: rotate(45deg) scale(0.9);'); });
export default withApi(SentryAppExternalIssueActions);
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=sentryAppExternalIssueActions.jsx.map