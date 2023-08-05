import { __assign, __awaiter, __extends, __generator, __makeTemplateObject, __read, __spread } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import space from 'app/styles/space';
import { t, tct } from 'app/locale';
import { Panel, PanelAlert, PanelBody, PanelHeader } from 'app/components/panels';
import { Client } from 'app/api';
import { addErrorMessage, addSuccessMessage } from 'app/actionCreators/indicator';
import ExternalLink from 'app/components/links/externalLink';
import Button from 'app/components/button';
import { valueSuggestions } from './utils';
import Dialog from './dialog';
import Content from './content';
import OrganizationRules from './organizationRules';
import { EventIdStatus, RequestError, } from './types';
import convertRelayPiiConfig from './convertRelayPiiConfig';
import submitRules from './submitRules';
import handleError from './handleError';
var ADVANCED_DATASCRUBBING_LINK = 'https://docs.sentry.io/data-management/advanced-datascrubbing/';
var DataScrubbing = /** @class */ (function (_super) {
    __extends(DataScrubbing, _super);
    function DataScrubbing() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            rules: [],
            savedRules: [],
            relayPiiConfig: _this.props.relayPiiConfig,
            sourceSuggestions: [],
            eventId: {
                value: '',
            },
            orgRules: [],
            errors: {},
            isProjectLevel: _this.props.endpoint.includes('projects'),
        };
        _this.api = new Client();
        _this.loadOrganizationRules = function () {
            var isProjectLevel = _this.state.isProjectLevel;
            var organization = _this.props.organization;
            if (isProjectLevel) {
                try {
                    _this.setState({
                        orgRules: convertRelayPiiConfig(organization.relayPiiConfig),
                    });
                }
                catch (_a) {
                    addErrorMessage(t('Unable to load organization rules'));
                }
            }
        };
        _this.loadSourceSuggestions = function () { return __awaiter(_this, void 0, void 0, function () {
            var _a, organization, projectId, eventId, query, rawSuggestions, sourceSuggestions_1, _b;
            return __generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        _a = this.props, organization = _a.organization, projectId = _a.projectId;
                        eventId = this.state.eventId;
                        if (!eventId.value) {
                            this.setState(function (prevState) { return ({
                                sourceSuggestions: valueSuggestions,
                                eventId: __assign(__assign({}, prevState.eventId), { status: undefined }),
                            }); });
                            return [2 /*return*/];
                        }
                        this.setState(function (prevState) { return ({
                            sourceSuggestions: valueSuggestions,
                            eventId: __assign(__assign({}, prevState.eventId), { status: EventIdStatus.LOADING }),
                        }); });
                        _c.label = 1;
                    case 1:
                        _c.trys.push([1, 3, , 4]);
                        query = { eventId: eventId.value };
                        if (projectId) {
                            query.projectId = projectId;
                        }
                        return [4 /*yield*/, this.api.requestPromise("/organizations/" + organization.slug + "/data-scrubbing-selector-suggestions/", { query: query })];
                    case 2:
                        rawSuggestions = _c.sent();
                        sourceSuggestions_1 = rawSuggestions.suggestions;
                        if (sourceSuggestions_1 && sourceSuggestions_1.length > 0) {
                            this.setState(function (prevState) { return ({
                                sourceSuggestions: sourceSuggestions_1,
                                eventId: __assign(__assign({}, prevState.eventId), { status: EventIdStatus.LOADED }),
                            }); });
                            return [2 /*return*/];
                        }
                        this.setState(function (prevState) { return ({
                            sourceSuggestions: valueSuggestions,
                            eventId: __assign(__assign({}, prevState.eventId), { status: EventIdStatus.NOT_FOUND }),
                        }); });
                        return [3 /*break*/, 4];
                    case 3:
                        _b = _c.sent();
                        this.setState(function (prevState) { return ({
                            eventId: __assign(__assign({}, prevState.eventId), { status: EventIdStatus.ERROR }),
                        }); });
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        _this.convertRequestError = function (error) {
            switch (error.type) {
                case RequestError.InvalidSelector:
                    _this.setState(function (prevState) { return ({
                        errors: __assign(__assign({}, prevState.errors), { source: error.message }),
                    }); });
                    break;
                case RequestError.RegexParse:
                    _this.setState(function (prevState) { return ({
                        errors: __assign(__assign({}, prevState.errors), { pattern: error.message }),
                    }); });
                    break;
                default:
                    addErrorMessage(error.message);
            }
        };
        _this.handleSave = function (rules, successMessage) { return __awaiter(_this, void 0, void 0, function () {
            var _a, endpoint, onSubmitSuccess, data, convertedRules, error_1;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.props, endpoint = _a.endpoint, onSubmitSuccess = _a.onSubmitSuccess;
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, submitRules(this.api, endpoint, rules)];
                    case 2:
                        data = _b.sent();
                        if (data === null || data === void 0 ? void 0 : data.relayPiiConfig) {
                            convertedRules = convertRelayPiiConfig(data.relayPiiConfig);
                            this.setState({ rules: convertedRules, showAddRuleModal: undefined });
                            addSuccessMessage(successMessage);
                            if (onSubmitSuccess) {
                                onSubmitSuccess(data);
                            }
                        }
                        return [3 /*break*/, 4];
                    case 3:
                        error_1 = _b.sent();
                        this.convertRequestError(handleError(error_1));
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        _this.handleAddRule = function (rule) {
            var newRule = __assign(__assign({}, rule), { id: _this.state.rules.length });
            var rules = __spread(_this.state.rules, [newRule]);
            _this.handleSave(rules, t('Successfully added rule'));
        };
        _this.handleUpdateRule = function (updatedRule) {
            var rules = _this.state.rules.map(function (rule) {
                if (rule.id === updatedRule.id) {
                    return updatedRule;
                }
                return rule;
            });
            _this.handleSave(rules, t('Successfully updated rule'));
        };
        _this.handleDeleteRule = function (rulesToBeDeleted) {
            var rules = _this.state.rules.filter(function (rule) { return !rulesToBeDeleted.includes(rule.id); });
            _this.handleSave(rules, t('Successfully deleted rule'));
        };
        _this.handleToggleAddRuleModal = function (showAddRuleModal) { return function () {
            _this.setState({ showAddRuleModal: showAddRuleModal });
        }; };
        _this.handleUpdateEventId = function (eventId) {
            _this.setState({
                eventId: {
                    value: eventId,
                },
            }, _this.loadSourceSuggestions);
        };
        return _this;
    }
    DataScrubbing.prototype.componentDidMount = function () {
        this.loadRules();
        this.loadSourceSuggestions();
        this.loadOrganizationRules();
    };
    DataScrubbing.prototype.componentDidUpdate = function (_prevProps, prevState) {
        if (prevState.relayPiiConfig !== this.state.relayPiiConfig) {
            this.loadRules();
        }
    };
    DataScrubbing.prototype.componentWillUnmount = function () {
        this.api.clear();
    };
    DataScrubbing.prototype.loadRules = function () {
        try {
            var convertedRules = convertRelayPiiConfig(this.state.relayPiiConfig);
            this.setState({
                rules: convertedRules,
                savedRules: convertedRules,
            });
        }
        catch (_a) {
            addErrorMessage(t('Unable to load project rules'));
        }
    };
    DataScrubbing.prototype.render = function () {
        var _a = this.props, additionalContext = _a.additionalContext, disabled = _a.disabled;
        var _b = this.state, rules = _b.rules, sourceSuggestions = _b.sourceSuggestions, showAddRuleModal = _b.showAddRuleModal, eventId = _b.eventId, orgRules = _b.orgRules, isProjectLevel = _b.isProjectLevel, errors = _b.errors;
        return (<React.Fragment>
        <Panel>
          <PanelHeader>
            <div>{t('Advanced Data Scrubbing')}</div>
          </PanelHeader>
          <PanelAlert type="info">
            {additionalContext}{' '}
            {"" + t('The new rules will only apply to upcoming events. ')}{' '}
            {tct('For more details, see [linkToDocs].', {
            linkToDocs: (<ExternalLink href={ADVANCED_DATASCRUBBING_LINK}>
                  {t('full documentation on data scrubbing')}
                </ExternalLink>),
        })}
          </PanelAlert>
          <PanelBody>
            {isProjectLevel && <OrganizationRules rules={orgRules}/>}
            <Content errors={errors} rules={rules} onDeleteRule={this.handleDeleteRule} onUpdateRule={this.handleUpdateRule} onUpdateEventId={this.handleUpdateEventId} eventId={eventId} sourceSuggestions={sourceSuggestions} disabled={disabled}/>
            <PanelAction>
              <Button href={ADVANCED_DATASCRUBBING_LINK} target="_blank">
                {t('Read the docs')}
              </Button>
              <Button disabled={disabled} onClick={this.handleToggleAddRuleModal(true)} priority="primary">
                {t('Add Rule')}
              </Button>
            </PanelAction>
          </PanelBody>
        </Panel>
        {showAddRuleModal && (<Dialog errors={errors} sourceSuggestions={sourceSuggestions} onSaveRule={this.handleAddRule} onClose={this.handleToggleAddRuleModal(false)} onUpdateEventId={this.handleUpdateEventId} eventId={eventId}/>)}
      </React.Fragment>);
    };
    return DataScrubbing;
}(React.Component));
export default DataScrubbing;
var PanelAction = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  padding: ", " ", ";\n  position: relative;\n  display: grid;\n  grid-gap: ", ";\n  grid-template-columns: auto auto;\n  justify-content: flex-end;\n  border-top: 1px solid ", ";\n"], ["\n  padding: ", " ", ";\n  position: relative;\n  display: grid;\n  grid-gap: ", ";\n  grid-template-columns: auto auto;\n  justify-content: flex-end;\n  border-top: 1px solid ", ";\n"])), space(1), space(2), space(1), function (p) { return p.theme.borderDark; });
var templateObject_1;
//# sourceMappingURL=index.jsx.map