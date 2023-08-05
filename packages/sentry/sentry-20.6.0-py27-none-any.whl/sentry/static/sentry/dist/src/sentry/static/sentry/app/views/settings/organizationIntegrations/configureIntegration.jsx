import { __extends } from "tslib";
import React from 'react';
import { t } from 'app/locale';
import AsyncView from 'app/views/asyncView';
import AddIntegration from 'app/views/organizationIntegrations/addIntegration';
import BreadcrumbTitle from 'app/views/settings/components/settingsBreadcrumb/breadcrumbTitle';
import Button from 'app/components/button';
import { IconAdd } from 'app/icons';
import Form from 'app/views/settings/components/forms/form';
import IntegrationAlertRules from 'app/views/organizationIntegrations/integrationAlertRules';
import IntegrationItem from 'app/views/organizationIntegrations/integrationItem';
import IntegrationRepos from 'app/views/organizationIntegrations/integrationRepos';
import JsonForm from 'app/views/settings/components/forms/jsonForm';
import SettingsPageHeader from 'app/views/settings/components/settingsPageHeader';
import withOrganization from 'app/utils/withOrganization';
import { trackIntegrationEvent } from 'app/utils/integrationUtil';
var ConfigureIntegration = /** @class */ (function (_super) {
    __extends(ConfigureIntegration, _super);
    function ConfigureIntegration() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.onUpdateIntegration = function () {
            _this.setState(_this.getDefaultState(), _this.fetchData);
        };
        _this.getAction = function (provider) {
            var integration = _this.state.integration;
            var action = provider && provider.key === 'pagerduty' ? (<AddIntegration provider={provider} onInstall={_this.onUpdateIntegration} account={integration.domainName}>
          {function (onClick) { return (<Button priority="primary" size="small" icon={<IconAdd size="xs" isCircled/>} onClick={function () { return onClick(); }}>
              {t('Add Services')}
            </Button>); }}
        </AddIntegration>) : null;
            return action;
        };
        return _this;
    }
    ConfigureIntegration.prototype.getEndpoints = function () {
        var _a = this.props.params, orgId = _a.orgId, integrationId = _a.integrationId;
        return [
            ['config', "/organizations/" + orgId + "/config/integrations/"],
            ['integration', "/organizations/" + orgId + "/integrations/" + integrationId + "/"],
        ];
    };
    ConfigureIntegration.prototype.onRequestSuccess = function (_a) {
        var stateKey = _a.stateKey, data = _a.data;
        if (stateKey !== 'integration') {
            return;
        }
        trackIntegrationEvent({
            eventKey: 'integrations.details_viewed',
            eventName: 'Integrations: Details Viewed',
            integration: data.provider.key,
            integration_type: 'first_party',
        }, this.props.organization);
    };
    ConfigureIntegration.prototype.getTitle = function () {
        return this.state.integration
            ? this.state.integration.provider.name
            : 'Configure Integration';
    };
    ConfigureIntegration.prototype.renderBody = function () {
        var orgId = this.props.params.orgId;
        var integration = this.state.integration;
        var provider = this.state.config.providers.find(function (p) { return p.key === integration.provider.key; });
        var title = <IntegrationItem integration={integration}/>;
        return (<React.Fragment>
        <BreadcrumbTitle routes={this.props.routes} title={integration.provider.name}/>
        <SettingsPageHeader noTitleStyles title={title} action={this.getAction(provider)}/>

        {integration.configOrganization.length > 0 && (<Form hideFooter saveOnBlur allowUndo apiMethod="POST" initialData={integration.configData} apiEndpoint={"/organizations/" + orgId + "/integrations/" + integration.id + "/"}>
            <JsonForm fields={integration.configOrganization} title={t('Organization Integration Settings')}/>
          </Form>)}

        {provider && provider.features.includes('alert-rule') && (<IntegrationAlertRules integration={integration}/>)}

        {provider && provider.features.includes('commits') && (<IntegrationRepos {...this.props} integration={integration}/>)}
      </React.Fragment>);
    };
    return ConfigureIntegration;
}(AsyncView));
export default withOrganization(ConfigureIntegration);
//# sourceMappingURL=configureIntegration.jsx.map