import { __assign, __awaiter, __extends, __generator, __makeTemplateObject, __read, __spread } from "tslib";
import { browserHistory } from 'react-router';
import React from 'react';
import classNames from 'classnames';
import styled from '@emotion/styled';
import { ALL_ENVIRONMENTS_KEY } from 'app/constants';
import { OnboardingTaskKey } from 'app/types';
import { Panel, PanelBody, PanelHeader } from 'app/components/panels';
import { addErrorMessage, addLoadingMessage, addSuccessMessage, } from 'app/actionCreators/indicator';
import { getDisplayName } from 'app/utils/environment';
import { t } from 'app/locale';
import AsyncView from 'app/views/asyncView';
import Button from 'app/components/button';
import Confirm from 'app/components/confirm';
import Form from 'app/views/settings/components/forms/form';
import LoadingMask from 'app/components/loadingMask';
import PanelAlert from 'app/components/panels/panelAlert';
import PanelItem from 'app/components/panels/panelItem';
import PanelSubHeader from 'app/views/settings/incidentRules/triggers/panelSubHeader';
import SelectField from 'app/views/settings/components/forms/selectField';
import TextField from 'app/views/settings/components/forms/textField';
import recreateRoute from 'app/utils/recreateRoute';
import space from 'app/styles/space';
import withOrganization from 'app/utils/withOrganization';
import withProject from 'app/utils/withProject';
import { updateOnboardingTask } from 'app/actionCreators/onboardingTasks';
import RuleNodeList from './ruleNodeList';
var FREQUENCY_CHOICES = [
    ['5', t('5 minutes')],
    ['10', t('10 minutes')],
    ['30', t('30 minutes')],
    ['60', t('60 minutes')],
    ['180', t('3 hours')],
    ['720', t('12 hours')],
    ['1440', t('24 hours')],
    ['10080', t('one week')],
    ['43200', t('30 days')],
];
var ACTION_MATCH_CHOICES = [
    ['all', t('all')],
    ['any', t('any')],
    ['none', t('none')],
];
var defaultRule = {
    actionMatch: 'all',
    actions: [],
    conditions: [],
    name: '',
    frequency: 30,
    environment: ALL_ENVIRONMENTS_KEY,
};
var POLLING_MAX_TIME_LIMIT = 3 * 60000;
function isSavedAlertRule(rule) {
    return rule.hasOwnProperty('id');
}
var IssueRuleEditor = /** @class */ (function (_super) {
    __extends(IssueRuleEditor, _super);
    function IssueRuleEditor() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.pollHandler = function (quitTime) { return __awaiter(_this, void 0, void 0, function () {
            var _a, organization, project, uuid, origRule, response, status_1, rule, error, ruleId, isNew, _b;
            var _this = this;
            return __generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        if (Date.now() > quitTime) {
                            addErrorMessage(t('Looking for that channel took too long :('));
                            this.setState({ loading: false });
                            return [2 /*return*/];
                        }
                        _a = this.props, organization = _a.organization, project = _a.project;
                        uuid = this.state.uuid;
                        origRule = this.state.rule;
                        _c.label = 1;
                    case 1:
                        _c.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, this.api.requestPromise("/projects/" + organization.slug + "/" + project.slug + "/rule-task/" + uuid + "/")];
                    case 2:
                        response = _c.sent();
                        status_1 = response.status, rule = response.rule, error = response.error;
                        if (status_1 === 'pending') {
                            setTimeout(function () {
                                _this.pollHandler(quitTime);
                            }, 1000);
                            return [2 /*return*/];
                        }
                        if (status_1 === 'failed') {
                            this.setState({
                                detailedError: { actions: [error ? error : t('An error occurred')] },
                                loading: false,
                            });
                            addErrorMessage(t('An error occurred'));
                        }
                        if (rule) {
                            ruleId = isSavedAlertRule(origRule) ? origRule.id + "/" : '';
                            isNew = !ruleId;
                            this.handleRuleSuccess(isNew, rule);
                        }
                        return [3 /*break*/, 4];
                    case 3:
                        _b = _c.sent();
                        addErrorMessage(t('An error occurred'));
                        this.setState({ loading: false });
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        _this.handleRuleSuccess = function (isNew, rule) {
            var organization = _this.props.organization;
            _this.setState({ detailedError: null, loading: false, rule: rule });
            // The onboarding task will be completed on the server side when the alert
            // is created
            updateOnboardingTask(null, organization, {
                task: OnboardingTaskKey.ALERT_RULE,
                status: 'complete',
            });
            // When editing, there is an extra route to move back from
            var stepBack = isNew ? -1 : -2;
            browserHistory.replace(recreateRoute('', __assign(__assign({}, _this.props), { stepBack: stepBack })));
            addSuccessMessage(isNew ? t('Created alert rule') : t('Updated alert rule'));
        };
        _this.handleSubmit = function () { return __awaiter(_this, void 0, void 0, function () {
            var rule, ruleId, isNew, _a, project, organization, endpoint, _b, resp, xhr, err_1;
            return __generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        rule = this.state.rule;
                        ruleId = isSavedAlertRule(rule) ? rule.id + "/" : '';
                        isNew = !ruleId;
                        _a = this.props, project = _a.project, organization = _a.organization;
                        endpoint = "/projects/" + organization.slug + "/" + project.slug + "/rules/" + ruleId;
                        if (rule && rule.environment === ALL_ENVIRONMENTS_KEY) {
                            delete rule.environment;
                        }
                        addLoadingMessage();
                        _c.label = 1;
                    case 1:
                        _c.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, this.api.requestPromise(endpoint, {
                                includeAllArgs: true,
                                method: isNew ? 'POST' : 'PUT',
                                data: rule,
                            })];
                    case 2:
                        _b = __read.apply(void 0, [_c.sent(), 3]), resp = _b[0], xhr = _b[2];
                        // if we get a 202 back it means that we have an async task
                        // running to lookup and verify the channel id for Slack.
                        if (xhr && xhr.status === 202) {
                            this.setState({ detailedError: null, loading: true, uuid: resp.uuid });
                            this.fetchStatus();
                            addLoadingMessage(t('Looking through all your channels...'));
                        }
                        else {
                            this.handleRuleSuccess(isNew, resp);
                        }
                        return [3 /*break*/, 4];
                    case 3:
                        err_1 = _c.sent();
                        this.setState({
                            detailedError: err_1.responseJSON || { __all__: 'Unknown error' },
                            loading: false,
                        });
                        addErrorMessage(t('An error occurred'));
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        _this.handleDeleteRule = function () { return __awaiter(_this, void 0, void 0, function () {
            var rule, ruleId, isNew, _a, project, organization, endpoint, err_2;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        rule = this.state.rule;
                        ruleId = isSavedAlertRule(rule) ? rule.id + "/" : '';
                        isNew = !ruleId;
                        _a = this.props, project = _a.project, organization = _a.organization;
                        if (isNew) {
                            return [2 /*return*/];
                        }
                        endpoint = "/projects/" + organization.slug + "/" + project.slug + "/rules/" + ruleId;
                        addLoadingMessage(t('Deleting...'));
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, this.api.requestPromise(endpoint, {
                                method: 'DELETE',
                            })];
                    case 2:
                        _b.sent();
                        addSuccessMessage(t('Deleted alert rule'));
                        browserHistory.replace(recreateRoute('', __assign(__assign({}, this.props), { stepBack: -2 })));
                        return [3 /*break*/, 4];
                    case 3:
                        err_2 = _b.sent();
                        this.setState({
                            detailedError: err_2.responseJSON || { __all__: 'Unknown error' },
                        });
                        addErrorMessage(t('There was a problem deleting the alert'));
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        _this.handleCancel = function () {
            var router = _this.props.router;
            router.push(recreateRoute('', __assign(__assign({}, _this.props), { stepBack: -1 })));
        };
        _this.hasError = function (field) {
            var detailedError = _this.state.detailedError;
            if (!detailedError) {
                return false;
            }
            return detailedError.hasOwnProperty(field);
        };
        _this.handleEnvironmentChange = function (val) {
            // If 'All Environments' is selected the value should be null
            if (val === ALL_ENVIRONMENTS_KEY) {
                _this.handleChange('environment', null);
            }
            else {
                _this.handleChange('environment', val);
            }
        };
        _this.handleChange = function (prop, val) {
            _this.setState(function (state) {
                var rule = __assign({}, state.rule);
                rule[prop] = val;
                return { rule: rule };
            });
        };
        _this.handlePropertyChange = function (type, idx, prop, val) {
            _this.setState(function (state) {
                var rule = __assign({}, state.rule);
                rule[type][idx][prop] = val;
                return { rule: rule };
            });
        };
        _this.handleAddRow = function (type, id) {
            _this.setState(function (state) {
                var _a;
                var _b, _c;
                var configuration = (_c = (_b = _this.state.configs) === null || _b === void 0 ? void 0 : _b[type]) === null || _c === void 0 ? void 0 : _c.find(function (c) { return c.id === id; });
                // Set initial configuration
                var initialValue = (configuration === null || configuration === void 0 ? void 0 : configuration.formFields) ? Object.fromEntries(Object.entries(configuration.formFields)
                    // TODO(ts): Doesn't work if I cast formField as IssueAlertRuleFormField
                    .map(function (_a) {
                    var _b = __read(_a, 2), key = _b[0], formField = _b[1];
                    var _c, _d, _e;
                    return [
                        key,
                        (_c = formField === null || formField === void 0 ? void 0 : formField.initial) !== null && _c !== void 0 ? _c : (_e = (_d = formField === null || formField === void 0 ? void 0 : formField.choices) === null || _d === void 0 ? void 0 : _d[0]) === null || _e === void 0 ? void 0 : _e[0],
                    ];
                })
                    .filter(function (_a) {
                    var _b = __read(_a, 2), initial = _b[1];
                    return !!initial;
                }))
                    : {};
                var newRule = __assign({ id: id }, initialValue);
                var rule = __assign(__assign({}, state.rule), (_a = {}, _a[type] = __spread((state.rule ? state.rule[type] : []), [newRule]), _a));
                return {
                    rule: rule,
                };
            });
        };
        _this.handleDeleteRow = function (type, idx) {
            _this.setState(function (prevState) {
                var _a;
                var newTypeList = prevState.rule ? __spread(prevState.rule[type]) : [];
                if (prevState.rule) {
                    newTypeList.splice(idx, 1);
                }
                var rule = __assign(__assign({}, prevState.rule), (_a = {}, _a[type] = newTypeList, _a));
                return {
                    rule: rule,
                };
            });
        };
        _this.handleAddCondition = function (id) { return _this.handleAddRow('conditions', id); };
        _this.handleAddAction = function (id) { return _this.handleAddRow('actions', id); };
        _this.handleDeleteCondition = function (ruleIndex) {
            return _this.handleDeleteRow('conditions', ruleIndex);
        };
        _this.handleDeleteAction = function (ruleIndex) { return _this.handleDeleteRow('actions', ruleIndex); };
        _this.handleChangeConditionProperty = function (ruleIndex, prop, val) {
            return _this.handlePropertyChange('conditions', ruleIndex, prop, val);
        };
        _this.handleChangeActionProperty = function (ruleIndex, prop, val) {
            return _this.handlePropertyChange('actions', ruleIndex, prop, val);
        };
        return _this;
    }
    IssueRuleEditor.prototype.getDefaultState = function () {
        return __assign(__assign({}, _super.prototype.getDefaultState.call(this)), { configs: null, detailedError: null, rule: __assign({}, defaultRule), environments: [], uuid: null });
    };
    IssueRuleEditor.prototype.getEndpoints = function () {
        var _a;
        var _b = this.props, params = _b.params, location = _b.location;
        var ruleId = params.ruleId, projectId = params.projectId, orgId = params.orgId;
        var _c = ((_a = location.query) !== null && _a !== void 0 ? _a : {}).issue_alerts_targeting, issue_alerts_targeting = _c === void 0 ? 0 : _c;
        var endpoints = [
            ['environments', "/projects/" + orgId + "/" + projectId + "/environments/"],
            [
                'configs',
                "/projects/" + orgId + "/" + projectId + "/rules/configuration/?issue_alerts_targeting=" + issue_alerts_targeting,
            ],
        ];
        if (ruleId) {
            endpoints.push(['rule', "/projects/" + orgId + "/" + projectId + "/rules/" + ruleId + "/"]);
        }
        return endpoints;
    };
    IssueRuleEditor.prototype.fetchStatus = function () {
        var _this = this;
        // pollHandler calls itself until it gets either a success
        // or failed status but we don't want to poll forever so we pass
        // in a hard stop time of 3 minutes before we bail.
        var quitTime = Date.now() + POLLING_MAX_TIME_LIMIT;
        setTimeout(function () {
            _this.pollHandler(quitTime);
        }, 1000);
    };
    IssueRuleEditor.prototype.renderLoading = function () {
        return this.renderBody();
    };
    IssueRuleEditor.prototype.renderBody = function () {
        var _this = this;
        var _a, _b, _c, _d, _e, _f;
        var _g = this.props, project = _g.project, organization = _g.organization;
        var environments = this.state.environments;
        var environmentChoices = __spread([
            [ALL_ENVIRONMENTS_KEY, t('All Environments')]
        ], environments.map(function (env) { return [env.name, getDisplayName(env)]; }));
        var _h = this.state, rule = _h.rule, detailedError = _h.detailedError;
        var _j = rule || {}, actionMatch = _j.actionMatch, actions = _j.actions, conditions = _j.conditions, frequency = _j.frequency, name = _j.name;
        var environment = !rule || !rule.environment ? ALL_ENVIRONMENTS_KEY : rule.environment;
        // Note `key` on `<Form>` below is so that on initial load, we show
        // the form with a loading mask on top of it, but force a re-render by using
        // a different key when we have fetched the rule so that form inputs are filled in
        return (<React.Fragment>
        <StyledForm key={isSavedAlertRule(rule) ? rule.id : undefined} onCancel={this.handleCancel} onSubmit={this.handleSubmit} initialData={__assign(__assign({}, rule), { environment: environment, actionMatch: actionMatch, frequency: "" + frequency })} submitLabel={t('Save Rule')} extraButton={isSavedAlertRule(rule) ? (<Confirm priority="danger" confirmText={t('Delete Rule')} onConfirm={this.handleDeleteRule} header={t('Delete Rule')} message={t('Are you sure you want to delete this rule?')}>
                <Button priority="danger" type="button">
                  {t('Delete Rule')}
                </Button>
              </Confirm>) : null}>
          {this.state.loading && <SemiTransparentLoadingMask />}
          <Panel>
            <PanelHeader>{t('Configure Rule Conditions')}</PanelHeader>
            <PanelBody>
              {detailedError && (<PanelAlert type="error">
                  {t('There was an error saving your changes. Make sure all fields are valid and try again.')}
                </PanelAlert>)}
              <SelectField className={classNames({
            error: this.hasError('environment'),
        })} label={t('Environment')} help={t('Choose an environment for these conditions to apply to')} placeholder={t('Select an Environment')} clearable={false} name="environment" choices={environmentChoices} onChange={function (val) { return _this.handleEnvironmentChange(val); }}/>

              <PanelSubHeader>
                {t('Whenever %s of these conditions are met for an issue', <EmbeddedWrapper>
                    <EmbeddedSelectField className={classNames({
            error: this.hasError('actionMatch'),
        })} inline={false} styles={{
            control: function (provided) { return (__assign(__assign({}, provided), { minHeight: '20px', height: '20px' })); },
        }} isSearchable={false} isClearable={false} name="actionMatch" required flexibleControlStateSize choices={ACTION_MATCH_CHOICES} onChange={function (val) { return _this.handleChange('actionMatch', val); }}/>
                  </EmbeddedWrapper>)}
              </PanelSubHeader>

              {this.hasError('conditions') && (<PanelAlert type="error">
                  {(_a = this.state.detailedError) === null || _a === void 0 ? void 0 : _a.conditions[0]}
                </PanelAlert>)}

              <PanelRuleItem>
                <RuleNodeList nodes={(_c = (_b = this.state.configs) === null || _b === void 0 ? void 0 : _b.conditions) !== null && _c !== void 0 ? _c : null} items={conditions || []} placeholder={t('Add a condition...')} onPropertyChange={this.handleChangeConditionProperty} onAddRow={this.handleAddCondition} onDeleteRow={this.handleDeleteCondition} organization={organization} project={project}/>
              </PanelRuleItem>

              <PanelSubHeader>{t('Perform these actions')}</PanelSubHeader>

              {this.hasError('actions') && (<PanelAlert type="error">
                  {(_d = this.state.detailedError) === null || _d === void 0 ? void 0 : _d.actions[0]}
                </PanelAlert>)}

              <PanelRuleItem>
                <RuleNodeList nodes={(_f = (_e = this.state.configs) === null || _e === void 0 ? void 0 : _e.actions) !== null && _f !== void 0 ? _f : null} items={actions || []} placeholder={t('Add an action...')} onPropertyChange={this.handleChangeActionProperty} onAddRow={this.handleAddAction} onDeleteRow={this.handleDeleteAction} organization={organization} project={project}/>
              </PanelRuleItem>
            </PanelBody>
          </Panel>

          <Panel>
            <PanelHeader>{t('Rate Limit')}</PanelHeader>
            <PanelBody>
              <SelectField label={t('Action Interval')} help={t('Perform these actions once this often for an issue')} clearable={false} name="frequency" className={this.hasError('frequency') ? ' error' : ''} value={frequency} required choices={FREQUENCY_CHOICES} onChange={function (val) { return _this.handleChange('frequency', val); }}/>
            </PanelBody>
          </Panel>

          <Panel>
            <PanelHeader>{t('Give your rule a name')}</PanelHeader>

            {this.hasError('name') && (<PanelAlert type="error">{t('Must enter a rule name')}</PanelAlert>)}

            <PanelBody>
              <TextField label={t('Rule name')} help={t('Give your rule a name so it is easy to manage later')} name="name" defaultValue={name} required placeholder={t('My Rule Name')} onChange={function (val) { return _this.handleChange('name', val); }}/>
            </PanelBody>
          </Panel>
        </StyledForm>
      </React.Fragment>);
    };
    return IssueRuleEditor;
}(AsyncView));
export default withProject(withOrganization(IssueRuleEditor));
var StyledForm = styled(Form)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  position: relative;\n"], ["\n  position: relative;\n"])));
var PanelRuleItem = styled(PanelItem)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  flex-direction: column;\n"], ["\n  flex-direction: column;\n"])));
var EmbeddedWrapper = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  margin: 0 ", ";\n  width: 80px;\n"], ["\n  margin: 0 ", ";\n  width: 80px;\n"])), space(1));
var EmbeddedSelectField = styled(SelectField)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  padding: 0;\n  font-weight: normal;\n  text-transform: none;\n"], ["\n  padding: 0;\n  font-weight: normal;\n  text-transform: none;\n"])));
var SemiTransparentLoadingMask = styled(LoadingMask)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  opacity: 0.6;\n  z-index: 1; /* Needed so that it sits above form elements */\n"], ["\n  opacity: 0.6;\n  z-index: 1; /* Needed so that it sits above form elements */\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=index.jsx.map