var _a, _b;
import { __assign, __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import * as Sentry from '@sentry/browser';
import styled from '@emotion/styled';
import { ActionType, TargetType, } from 'app/views/settings/incidentRules/types';
import { PanelItem } from 'app/components/panels';
import { addErrorMessage } from 'app/actionCreators/indicator';
import { removeAtArrayIndex } from 'app/utils/removeAtArrayIndex';
import { replaceAtArrayIndex } from 'app/utils/replaceAtArrayIndex';
import { t } from 'app/locale';
import DeleteActionButton from 'app/views/settings/incidentRules/triggers/actionsPanel/deleteActionButton';
import Input from 'app/views/settings/components/forms/controls/input';
import LoadingIndicator from 'app/components/loadingIndicator';
import PanelSubHeader from 'app/views/settings/incidentRules/triggers/panelSubHeader';
import SelectControl from 'app/components/forms/selectControl';
import SelectMembers from 'app/components/selectMembers';
import space from 'app/styles/space';
import withOrganization from 'app/utils/withOrganization';
var ActionLabel = (_a = {},
    _a[ActionType.EMAIL] = t('E-mail'),
    _a[ActionType.SLACK] = t('Slack'),
    _a[ActionType.PAGER_DUTY] = t('Pagerduty'),
    _a);
var TargetLabel = (_b = {},
    _b[TargetType.USER] = t('Member'),
    _b[TargetType.TEAM] = t('Team'),
    _b);
/**
 * Lists saved actions as well as control to add a new action
 */
var ActionsPanel = /** @class */ (function (_super) {
    __extends(ActionsPanel, _super);
    function ActionsPanel() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleAddAction = function (value) {
            var availableActions = _this.props.availableActions;
            var actionConfig = availableActions &&
                availableActions.find(function (availableAction) { return _this.getActionUniqueKey(availableAction) === value.value; });
            if (!actionConfig) {
                addErrorMessage(t('There was a problem adding an action'));
                Sentry.setExtras({
                    integrationId: value,
                });
                Sentry.captureException(new Error('Unable to add an action'));
                return;
            }
            var action = {
                type: actionConfig.type,
                targetType: actionConfig &&
                    actionConfig.allowedTargetTypes &&
                    actionConfig.allowedTargetTypes.length > 0
                    ? actionConfig.allowedTargetTypes[0]
                    : null,
                targetIdentifier: '',
                integrationId: actionConfig.integrationId,
            };
            _this.props.onAdd(action);
        };
        _this.handleDeleteAction = function (index) {
            var _a = _this.props, actions = _a.actions, onChange = _a.onChange;
            onChange(removeAtArrayIndex(actions, index));
        };
        _this.handleChangeTarget = function (index, value) {
            var _a = _this.props, actions = _a.actions, onChange = _a.onChange;
            var newAction = __assign(__assign({}, actions[index]), { targetType: value.value, targetIdentifier: '' });
            onChange(replaceAtArrayIndex(actions, index, newAction));
        };
        _this.handleChangeTargetIdentifier = function (index, value) {
            _this.doChangeTargetIdentifier(index, value.value);
        };
        _this.handleChangeSpecificTargetIdentifier = function (index, e) {
            _this.doChangeTargetIdentifier(index, e.target.value);
        };
        return _this;
    }
    /**
     * Actions have a type (e.g. email, slack, etc), but only some have
     * an integrationId (e.g. email is null). This helper creates a unique
     * id based on the type and integrationId so that we know what action
     * a user's saved action corresponds to.
     */
    ActionsPanel.prototype.getActionUniqueKey = function (_a) {
        var type = _a.type, integrationId = _a.integrationId;
        return type + "-" + integrationId;
    };
    /**
     * Creates a human-friendly display name for the integration based on type and
     * server provided `integrationName`
     *
     * e.g. for slack we show that it is slack and the `integrationName` is the workspace name
     */
    ActionsPanel.prototype.getFullActionTitle = function (_a) {
        var type = _a.type, integrationName = _a.integrationName;
        return "" + ActionLabel[type] + (integrationName ? " - " + integrationName : '');
    };
    ActionsPanel.prototype.doChangeTargetIdentifier = function (index, value) {
        var _a = this.props, actions = _a.actions, onChange = _a.onChange;
        var newAction = __assign(__assign({}, actions[index]), { targetIdentifier: value });
        onChange(replaceAtArrayIndex(actions, index, newAction));
    };
    ActionsPanel.prototype.render = function () {
        var _this = this;
        var _a = this.props, actions = _a.actions, availableActions = _a.availableActions, currentProject = _a.currentProject, disabled = _a.disabled, loading = _a.loading, organization = _a.organization, projects = _a.projects;
        var items = availableActions &&
            availableActions.map(function (availableAction) { return ({
                value: _this.getActionUniqueKey(availableAction),
                label: _this.getFullActionTitle(availableAction),
            }); });
        return (<React.Fragment>
        <PanelSubHeader>{t('Actions')}</PanelSubHeader>
        <React.Fragment>
          {loading && <LoadingIndicator />}
          {actions &&
            actions.map(function (action, i) {
                var _a, _b;
                var isUser = action.targetType === TargetType.USER;
                var isTeam = action.targetType === TargetType.TEAM;
                var availableAction = availableActions === null || availableActions === void 0 ? void 0 : availableActions.find(function (a) { return _this.getActionUniqueKey(a) === _this.getActionUniqueKey(action); });
                return (<PanelItemGrid key={i}>
                  {_this.getFullActionTitle({
                    type: action.type,
                    integrationName: (_a = availableAction === null || availableAction === void 0 ? void 0 : availableAction.integrationName) !== null && _a !== void 0 ? _a : '',
                })}

                  {availableAction && availableAction.allowedTargetTypes.length > 1 ? (<SelectControl disabled={disabled || loading} value={action.targetType} options={(_b = availableAction === null || availableAction === void 0 ? void 0 : availableAction.allowedTargetTypes) === null || _b === void 0 ? void 0 : _b.map(function (allowedType) { return ({
                    value: allowedType,
                    label: TargetLabel[allowedType],
                }); })} onChange={_this.handleChangeTarget.bind(_this, i)}/>) : (<span />)}

                  {isUser || isTeam ? (<SelectMembers disabled={disabled} key={isTeam ? 'team' : 'member'} showTeam={isTeam} project={projects.find(function (_a) {
                    var slug = _a.slug;
                    return slug === currentProject;
                })} organization={organization} value={action.targetIdentifier} onChange={_this.handleChangeTargetIdentifier.bind(_this, i)}/>) : (<Input disabled={disabled} key={action.type} value={action.targetIdentifier} onChange={_this.handleChangeSpecificTargetIdentifier.bind(_this, i)} placeholder="@username or #channel"/>)}
                  <DeleteActionButton index={i} onClick={_this.handleDeleteAction} disabled={disabled}/>
                </PanelItemGrid>);
            })}
          <PanelItem>
            <StyledSelectControl name="add-action" aria-label={t('Add an Action')} isDisabled={disabled || loading} placeholder={t('Add an Action')} onChange={this.handleAddAction} value={null} options={items !== null && items !== void 0 ? items : []}/>
          </PanelItem>
        </React.Fragment>
      </React.Fragment>);
    };
    return ActionsPanel;
}(React.PureComponent));
var ActionsPanelWithSpace = styled(ActionsPanel)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-top: ", ";\n"], ["\n  margin-top: ", ";\n"])), space(4));
var PanelItemGrid = styled(PanelItem)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 1fr 1fr 1fr min-content;\n  align-items: center;\n  grid-gap: ", ";\n"], ["\n  display: grid;\n  grid-template-columns: 1fr 1fr 1fr min-content;\n  align-items: center;\n  grid-gap: ", ";\n"])), space(2));
var StyledSelectControl = styled(SelectControl)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  width: 100%;\n"], ["\n  width: 100%;\n"])));
export default withOrganization(ActionsPanelWithSpace);
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=index.jsx.map