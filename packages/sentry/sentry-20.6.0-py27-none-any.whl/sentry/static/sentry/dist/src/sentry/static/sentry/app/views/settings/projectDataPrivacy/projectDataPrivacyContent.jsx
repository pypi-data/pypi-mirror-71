import { __extends } from "tslib";
import React from 'react';
import Link from 'app/components/links/link';
import { t, tct } from 'app/locale';
import SettingsPageHeader from 'app/views/settings/components/settingsPageHeader';
import JsonForm from 'app/views/settings/components/forms/jsonForm';
import Form from 'app/views/settings/components/forms/form';
import { fields } from 'app/data/forms/projectGeneralSettings';
import AsyncView from 'app/views/asyncView';
import ProjectActions from 'app/actions/projectActions';
import DataScrubbing from '../components/dataScrubbing';
var ProjectDataPrivacyContent = /** @class */ (function (_super) {
    __extends(ProjectDataPrivacyContent, _super);
    function ProjectDataPrivacyContent() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleUpdateProject = function (data) {
            // This will update our project global state
            ProjectActions.updateSuccess(data);
        };
        return _this;
    }
    ProjectDataPrivacyContent.prototype.getEndpoints = function () {
        var _a = this.props, organization = _a.organization, project = _a.project;
        return [['data', "/projects/" + organization.slug + "/" + project.slug + "/"]];
    };
    ProjectDataPrivacyContent.prototype.renderBody = function () {
        var _a = this.props, organization = _a.organization, project = _a.project;
        var initialData = this.state.data;
        var endpoint = "/projects/" + organization.slug + "/" + project.slug + "/";
        var access = new Set(organization.access);
        var features = new Set(organization.features);
        var relayPiiConfig = initialData === null || initialData === void 0 ? void 0 : initialData.relayPiiConfig;
        var apiMethod = 'PUT';
        return (<React.Fragment>
        <SettingsPageHeader title={t('Security & Privacy')}/>
        <Form saveOnBlur allowUndo initialData={initialData} apiMethod={apiMethod} apiEndpoint={endpoint} onSubmitSuccess={this.handleUpdateProject}>
          <JsonForm title={t('Security & Privacy')} additionalFieldProps={{
            organization: organization,
        }} features={features} disabled={!access.has('project:write')} fields={[fields.storeCrashReports]}/>
          <JsonForm title={t('Data Scrubbing')} additionalFieldProps={{
            organization: organization,
        }} features={features} disabled={!access.has('project:write')} fields={[
            fields.dataScrubber,
            fields.dataScrubberDefaults,
            fields.scrubIPAddresses,
            fields.sensitiveFields,
            fields.safeFields,
        ]}/>
        </Form>
        <DataScrubbing additionalContext={<span>
              {tct('These rules can be configured at the organization level in [linkToOrganizationSecurityAndPrivacy].', {
            linkToOrganizationSecurityAndPrivacy: (<Link to={"/settings/" + organization.slug + "/security-and-privacy/"}>
                      {t('Security and Privacy')}
                    </Link>),
        })}
            </span>} endpoint={endpoint} relayPiiConfig={relayPiiConfig} disabled={!access.has('project:write')} organization={organization} projectId={project.id} onSubmitSuccess={this.handleUpdateProject}/>
      </React.Fragment>);
    };
    return ProjectDataPrivacyContent;
}(AsyncView));
export default ProjectDataPrivacyContent;
//# sourceMappingURL=projectDataPrivacyContent.jsx.map