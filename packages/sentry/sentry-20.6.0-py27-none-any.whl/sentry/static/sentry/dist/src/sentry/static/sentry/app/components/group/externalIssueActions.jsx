import { __assign, __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import PropTypes from 'prop-types';
import Modal from 'react-bootstrap/lib/Modal';
import styled from '@emotion/styled';
import { addSuccessMessage, addErrorMessage } from 'app/actionCreators/indicator';
import AsyncComponent from 'app/components/asyncComponent';
import IssueSyncListElement from 'app/components/issueSyncListElement';
import ExternalIssueForm from 'app/components/group/externalIssueForm';
import IntegrationItem from 'app/views/organizationIntegrations/integrationItem';
import NavTabs from 'app/components/navTabs';
import { t } from 'app/locale';
import overflowEllipsis from 'app/styles/overflowEllipsis';
import space from 'app/styles/space';
var ExternalIssueActions = /** @class */ (function (_super) {
    __extends(ExternalIssueActions, _super);
    function ExternalIssueActions(props, context) {
        var _this = _super.call(this, props, context) || this;
        _this.openModal = function () {
            var integration = _this.props.integration;
            _this.setState({
                showModal: true,
                selectedIntegration: integration,
                action: 'create',
            });
        };
        _this.closeModal = function (data) {
            _this.setState({
                showModal: false,
                action: null,
                issue: data && data.id ? data : null,
            });
        };
        _this.handleClick = function (action) {
            _this.setState({ action: action });
        };
        _this.state = __assign({ showModal: false, action: 'create', selectedIntegration: _this.props.integration, issue: _this.getIssue() }, _this.getDefaultState());
        return _this;
    }
    ExternalIssueActions.prototype.getEndpoints = function () {
        return [];
    };
    ExternalIssueActions.prototype.getIssue = function () {
        return this.props.integration && this.props.integration.externalIssues
            ? this.props.integration.externalIssues[0]
            : null;
    };
    ExternalIssueActions.prototype.deleteIssue = function (issueId) {
        var _this = this;
        var _a = this.props, group = _a.group, integration = _a.integration;
        var endpoint = "/groups/" + group.id + "/integrations/" + integration.id + "/?externalIssue=" + issueId;
        this.api.request(endpoint, {
            method: 'DELETE',
            success: function () {
                addSuccessMessage(t('Successfully unlinked issue.'));
                _this.setState({
                    issue: null,
                });
            },
            error: function () {
                addErrorMessage(t('Unable to unlink issue.'));
            },
        });
    };
    ExternalIssueActions.prototype.renderBody = function () {
        var _this = this;
        var _a = this.state, action = _a.action, selectedIntegration = _a.selectedIntegration, issue = _a.issue;
        return (<React.Fragment>
        <IssueSyncListElement onOpen={this.openModal} externalIssueLink={issue ? issue.url : null} externalIssueId={issue ? issue.id : null} externalIssueKey={issue ? issue.key : null} externalIssueDisplayName={issue ? issue.displayName : null} onClose={this.deleteIssue.bind(this)} integrationType={selectedIntegration.provider.key} hoverCardHeader={t('Linked %s Integration', selectedIntegration.provider.name)} hoverCardBody={issue && issue.title ? (<div>
                <IssueTitle>{issue.title}</IssueTitle>
                {issue.description && (<IssueDescription>{issue.description}</IssueDescription>)}
              </div>) : (<IntegrationItem integration={selectedIntegration}/>)}/>
        {selectedIntegration && (<Modal show={this.state.showModal} onHide={this.closeModal} animation={false} enforceFocus={false} backdrop="static">
            <Modal.Header closeButton>
              <Modal.Title>{selectedIntegration.provider.name + " Issue"}</Modal.Title>
            </Modal.Header>
            <NavTabs underlined>
              <li className={action === 'create' ? 'active' : ''}>
                <a onClick={function () { return _this.handleClick('create'); }}>{t('Create')}</a>
              </li>
              <li className={action === 'link' ? 'active' : ''}>
                <a onClick={function () { return _this.handleClick('link'); }}>{t('Link')}</a>
              </li>
            </NavTabs>
            <Modal.Body>
              {action && (<ExternalIssueForm 
        // need the key here so React will re-render
        // with a new action prop
        key={action} group={this.props.group} integration={selectedIntegration} action={action} onSubmitSuccess={this.closeModal}/>)}
            </Modal.Body>
          </Modal>)}
      </React.Fragment>);
    };
    ExternalIssueActions.propTypes = {
        group: PropTypes.object.isRequired,
        integration: PropTypes.object.isRequired,
    };
    return ExternalIssueActions;
}(AsyncComponent));
var IssueTitle = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  font-size: 1.1em;\n  font-weight: 600;\n  ", ";\n"], ["\n  font-size: 1.1em;\n  font-weight: 600;\n  ", ";\n"])), overflowEllipsis);
var IssueDescription = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  margin-top: ", ";\n  ", ";\n"], ["\n  margin-top: ", ";\n  ", ";\n"])), space(1), overflowEllipsis);
export default ExternalIssueActions;
var templateObject_1, templateObject_2;
//# sourceMappingURL=externalIssueActions.jsx.map