import { __extends } from "tslib";
import React from 'react';
import { t } from 'app/locale';
import SettingsPageHeader from 'app/views/settings/components/settingsPageHeader';
import JsonForm from 'app/views/settings/components/forms/jsonForm';
import Form from 'app/views/settings/components/forms/form';
import AsyncView from 'app/views/asyncView';
import { addErrorMessage } from 'app/actionCreators/indicator';
import { updateOrganization } from 'app/actionCreators/organizations';
import organizationSecurityAndPrivacy from 'app/data/forms/organizationSecurityAndPrivacy';
import DataScrubbing from '../components/dataScrubbing';
var OrganizationSecurityAndPrivacyContent = /** @class */ (function (_super) {
    __extends(OrganizationSecurityAndPrivacyContent, _super);
    function OrganizationSecurityAndPrivacyContent() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleUpdateOrganization = function (data) {
            // This will update OrganizationStore (as well as OrganizationsStore
            // which is slightly incorrect because it has summaries vs a detailed org)
            updateOrganization(data);
        };
        return _this;
    }
    OrganizationSecurityAndPrivacyContent.prototype.getEndpoints = function () {
        var orgId = this.props.params.orgId;
        return [
            ['data', "/organizations/" + orgId + "/"],
            ['authProvider', "/organizations/" + orgId + "/auth-provider/"],
        ];
    };
    OrganizationSecurityAndPrivacyContent.prototype.renderBody = function () {
        var _this = this;
        var _a;
        var organization = this.props.organization;
        var orgId = this.props.params.orgId;
        var authProvider = this.state.authProvider;
        var initialData = this.props.organization;
        var endpoint = "/organizations/" + orgId + "/";
        var access = new Set(organization.access);
        var features = new Set(organization.features);
        var relayPiiConfig = (_a = this.state.data) === null || _a === void 0 ? void 0 : _a.relayPiiConfig;
        return (<React.Fragment>
        <SettingsPageHeader title={t('Security & Privacy')}/>
        <Form data-test-id="organization-settings-security-and-privacy" apiMethod="PUT" apiEndpoint={endpoint} initialData={initialData} additionalFieldProps={{ hasSsoEnabled: !!authProvider }} onSubmitSuccess={function (_resp, model) {
            _this.handleUpdateOrganization(model.initialData);
        }} onSubmitError={function () { return addErrorMessage('Unable to save change'); }} saveOnBlur allowUndo>
          <JsonForm features={features} forms={organizationSecurityAndPrivacy} disabled={!access.has('org:write')}/>
        </Form>
        <DataScrubbing additionalContext={t('These rules can be configured for each project.')} endpoint={endpoint} relayPiiConfig={relayPiiConfig} disabled={!access.has('org:write')} organization={organization} onSubmitSuccess={this.handleUpdateOrganization}/>
      </React.Fragment>);
    };
    return OrganizationSecurityAndPrivacyContent;
}(AsyncView));
export default OrganizationSecurityAndPrivacyContent;
//# sourceMappingURL=organizationSecurityAndPrivacyContent.jsx.map