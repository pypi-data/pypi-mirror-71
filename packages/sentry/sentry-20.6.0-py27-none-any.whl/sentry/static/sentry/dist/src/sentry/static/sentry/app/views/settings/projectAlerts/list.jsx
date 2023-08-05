import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { IconAdd, IconSettings } from 'app/icons';
import { PanelTable } from 'app/components/panels';
import { t } from 'app/locale';
import AsyncView from 'app/views/asyncView';
import Button from 'app/components/button';
import OnboardingHovercard from 'app/views/settings/projectAlerts/onboardingHovercard';
import Pagination from 'app/components/pagination';
import PermissionAlert from 'app/views/settings/project/permissionAlert';
import RuleRow from 'app/views/settings/projectAlerts/ruleRow';
import SettingsPageHeader from 'app/views/settings/components/settingsPageHeader';
import Tooltip from 'app/components/tooltip';
import routeTitle from 'app/utils/routeTitle';
import space from 'app/styles/space';
var ProjectAlertRules = /** @class */ (function (_super) {
    __extends(ProjectAlertRules, _super);
    function ProjectAlertRules() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    ProjectAlertRules.prototype.getEndpoints = function () {
        var _a = this.props.params, orgId = _a.orgId, projectId = _a.projectId;
        return [['rules', "/projects/" + orgId + "/" + projectId + "/combined-rules/"]];
    };
    ProjectAlertRules.prototype.getTitle = function () {
        var projectId = this.props.params.projectId;
        return routeTitle(t('Alert Rules'), projectId);
    };
    ProjectAlertRules.prototype.renderResults = function () {
        var _this = this;
        var _a = this.props, canEditRule = _a.canEditRule, params = _a.params;
        var orgId = params.orgId, projectId = params.projectId;
        return (<React.Fragment>
        {this.state.rules.map(function (rule) { return (<RuleRow type={rule.type === 'alert_rule' ? 'issue' : 'metric'} api={_this.api} key={rule.type + "-" + rule.id} data={rule} orgId={orgId} projectId={projectId} params={_this.props.params} location={_this.props.location} routes={_this.props.routes} canEdit={canEditRule}/>); })}
      </React.Fragment>);
    };
    ProjectAlertRules.prototype.renderLoading = function () {
        return this.renderBody();
    };
    ProjectAlertRules.prototype.renderBody = function () {
        var _this = this;
        var _a = this.props, canEditRule = _a.canEditRule, location = _a.location, organization = _a.organization, params = _a.params;
        var orgId = params.orgId, projectId = params.projectId;
        var _b = this.state, loading = _b.loading, rules = _b.rules, rulesPageLinks = _b.rulesPageLinks;
        var basePath = "/settings/" + orgId + "/projects/" + projectId + "/alerts/";
        return (<React.Fragment>
        <SettingsPageHeader title={t('Alerts')} action={<HeaderActions>
              <Button to={basePath + "settings/"} size="small" icon={<IconSettings />}>
                {t('Settings')}
              </Button>
              <OnboardingHovercard organization={organization} location={location}>
                <Tooltip disabled={canEditRule} title={t('You do not have permission to edit alert rules.')}>
                  <Button to={basePath + "new/"} disabled={!canEditRule} priority="primary" size="small" icon={<IconAdd size="xs" isCircled/>}>
                    {t('New Alert Rule')}
                  </Button>
                </Tooltip>
              </OnboardingHovercard>
            </HeaderActions>}/>
        <PermissionAlert />

        <ScrollWrapper>
          <StyledPanelTable isLoading={loading} isEmpty={!loading && !rules.length} emptyMessage={t('There are no alerts configured for this project.')} headers={[
            <div key="type">{t('Type')}</div>,
            <div key="name">{t('Name')}</div>,
            <div key="conditions">{t('Conditions/Triggers')}</div>,
            <div key="actions">{t('Action(s)')}</div>,
        ]}>
            {function () { return _this.renderResults(); }}
          </StyledPanelTable>
        </ScrollWrapper>

        <Pagination pageLinks={rulesPageLinks}/>
      </React.Fragment>);
    };
    return ProjectAlertRules;
}(AsyncView));
export default ProjectAlertRules;
var ScrollWrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  width: 100%;\n  overflow-x: auto;\n"], ["\n  width: 100%;\n  overflow-x: auto;\n"])));
/**
 * TODO(billy): Not sure if this should be default for PanelTable or not
 */
var StyledPanelTable = styled(PanelTable)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  width: fit-content;\n  min-width: 100%;\n"], ["\n  width: fit-content;\n  min-width: 100%;\n"])));
var HeaderActions = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: grid;\n  grid-auto-flow: column;\n  grid-gap: ", ";\n"], ["\n  display: grid;\n  grid-auto-flow: column;\n  grid-gap: ", ";\n"])), space(1));
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=list.jsx.map