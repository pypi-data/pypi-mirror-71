import { __assign, __extends, __read, __spread } from "tslib";
import React from 'react';
import { fetchOrgMembers } from 'app/actionCreators/members';
import { t, tct } from 'app/locale';
import ActionsPanel from 'app/views/settings/incidentRules/triggers/actionsPanel';
import Field from 'app/views/settings/components/forms/field';
import ThresholdControl from 'app/views/settings/incidentRules/triggers/thresholdControl';
import withApi from 'app/utils/withApi';
import withConfig from 'app/utils/withConfig';
import { AlertRuleThreshold, } from '../types';
var TriggerForm = /** @class */ (function (_super) {
    __extends(TriggerForm, _super);
    function TriggerForm() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.getThresholdKey = function (type) {
            return type === AlertRuleThreshold.RESOLUTION ? 'resolveThreshold' : 'alertThreshold';
        };
        /**
         * Handler for threshold changes coming from slider or chart.
         * Needs to sync state with the form.
         */
        _this.handleChangeThreshold = function (type, value) {
            var _a, _b;
            var _c = _this.props, onChange = _c.onChange, trigger = _c.trigger;
            var thresholdKey = _this.getThresholdKey(type);
            onChange(__assign(__assign({}, trigger), (_a = {}, _a[thresholdKey] = value.threshold, _a.thresholdType = value.thresholdType, _a)), (_b = {}, _b[thresholdKey] = value.threshold, _b));
        };
        return _this;
    }
    TriggerForm.prototype.render = function () {
        var _a = this.props, disabled = _a.disabled, error = _a.error, trigger = _a.trigger, isCritical = _a.isCritical;
        var triggerLabel = isCritical
            ? t('Critical Trigger Threshold')
            : t('Warning Trigger Threshold');
        var resolutionLabel = isCritical
            ? t('Critical Resolution Threshold')
            : t('Warning Resolution Threshold');
        return (<React.Fragment>
        <Field label={triggerLabel} help={tct('The threshold that will activate the [severity] status', {
            severity: isCritical ? t('critical') : t('warning'),
        })} required error={error && error.alertThreshold}>
          <ThresholdControl disabled={disabled} type={AlertRuleThreshold.INCIDENT} thresholdType={trigger.thresholdType} threshold={trigger.alertThreshold} onChange={this.handleChangeThreshold}/>
        </Field>

        <Field label={resolutionLabel} help={tct('The threshold that will de-activate the [severity] status', {
            severity: isCritical ? t('critical') : t('warning'),
        })} error={error && error.resolveThreshold}>
          <ThresholdControl disabled={disabled} type={AlertRuleThreshold.RESOLUTION} thresholdType={trigger.thresholdType} threshold={trigger.resolveThreshold} onChange={this.handleChangeThreshold}/>
        </Field>
      </React.Fragment>);
    };
    return TriggerForm;
}(React.PureComponent));
var TriggerFormContainer = /** @class */ (function (_super) {
    __extends(TriggerFormContainer, _super);
    function TriggerFormContainer() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleChangeTrigger = function (trigger, changeObj) {
            var _a = _this.props, onChange = _a.onChange, triggerIndex = _a.triggerIndex;
            onChange(triggerIndex, trigger, changeObj);
        };
        _this.handleAddAction = function (action) {
            var _a = _this.props, onChange = _a.onChange, trigger = _a.trigger, triggerIndex = _a.triggerIndex;
            var actions = __spread(trigger.actions, [action]);
            onChange(triggerIndex, __assign(__assign({}, trigger), { actions: actions }), { actions: actions });
        };
        _this.handleChangeActions = function (actions) {
            var _a = _this.props, onChange = _a.onChange, trigger = _a.trigger, triggerIndex = _a.triggerIndex;
            onChange(triggerIndex, __assign(__assign({}, trigger), { actions: actions }), { actions: actions });
        };
        return _this;
    }
    TriggerFormContainer.prototype.componentDidMount = function () {
        var _a = this.props, api = _a.api, organization = _a.organization;
        fetchOrgMembers(api, organization.slug);
    };
    TriggerFormContainer.prototype.render = function () {
        var _a = this.props, api = _a.api, availableActions = _a.availableActions, config = _a.config, currentProject = _a.currentProject, disabled = _a.disabled, error = _a.error, isCritical = _a.isCritical, organization = _a.organization, trigger = _a.trigger, triggerIndex = _a.triggerIndex, projects = _a.projects;
        return (<React.Fragment>
        <TriggerForm api={api} config={config} disabled={disabled} error={error} trigger={trigger} organization={organization} projects={projects} triggerIndex={triggerIndex} isCritical={isCritical} onChange={this.handleChangeTrigger}/>
        <ActionsPanel disabled={disabled} loading={availableActions === null} error={false} availableActions={availableActions} currentProject={currentProject} organization={organization} projects={projects} triggerIndex={triggerIndex} actions={trigger.actions} onChange={this.handleChangeActions} onAdd={this.handleAddAction}/>
      </React.Fragment>);
    };
    return TriggerFormContainer;
}(React.Component));
export default withConfig(withApi(TriggerFormContainer));
//# sourceMappingURL=form.jsx.map