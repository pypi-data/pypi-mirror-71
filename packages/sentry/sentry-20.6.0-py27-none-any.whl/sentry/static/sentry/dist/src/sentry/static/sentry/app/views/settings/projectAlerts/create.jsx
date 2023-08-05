import { __extends } from "tslib";
import React from 'react';
import { t } from 'app/locale';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import IncidentRulesCreate from 'app/views/settings/incidentRules/create';
import IssueEditor from 'app/views/settings/projectAlerts/issueEditor';
import SentryDocumentTitle from 'app/components/sentryDocumentTitle';
import SettingsPageHeader from 'app/views/settings/components/settingsPageHeader';
import withProject from 'app/utils/withProject';
import AlertTypeChooser from './alertTypeChooser';
var Create = /** @class */ (function (_super) {
    __extends(Create, _super);
    function Create() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            alertType: _this.props.location.pathname.includes('/alerts/rules/')
                ? 'issue'
                : _this.props.location.pathname.includes('/alerts/metric-rules/')
                    ? 'metric'
                    : null,
        };
        _this.handleChangeAlertType = function (alertType) {
            // alertType should be `issue` or `metric`
            _this.setState({ alertType: alertType });
        };
        return _this;
    }
    Create.prototype.componentDidMount = function () {
        var _a = this.props, organization = _a.organization, project = _a.project;
        trackAnalyticsEvent({
            eventKey: 'new_alert_rule.viewed',
            eventName: 'New Alert Rule: Viewed',
            organization_id: parseInt(organization.id, 10),
            project_id: parseInt(project.id, 10),
        });
    };
    Create.prototype.render = function () {
        var _a = this.props, hasMetricAlerts = _a.hasMetricAlerts, organization = _a.organization;
        var projectId = this.props.params.projectId;
        var alertType = this.state.alertType;
        var shouldShowAlertTypeChooser = hasMetricAlerts;
        var title = t('New Alert');
        return (<React.Fragment>
        <SentryDocumentTitle title={title} objSlug={projectId}/>
        <SettingsPageHeader title={title}/>

        {shouldShowAlertTypeChooser && (<AlertTypeChooser organization={organization} selected={alertType} onChange={this.handleChangeAlertType}/>)}

        {(!hasMetricAlerts || alertType === 'issue') && <IssueEditor {...this.props}/>}

        {hasMetricAlerts && alertType === 'metric' && (<IncidentRulesCreate {...this.props}/>)}
      </React.Fragment>);
    };
    return Create;
}(React.Component));
export default withProject(Create);
//# sourceMappingURL=create.jsx.map