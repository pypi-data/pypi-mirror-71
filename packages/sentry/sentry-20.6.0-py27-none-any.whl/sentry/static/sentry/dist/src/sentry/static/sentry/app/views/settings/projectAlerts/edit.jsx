import React from 'react';
import { t } from 'app/locale';
import IncidentRulesDetails from 'app/views/settings/incidentRules/details';
import IssueEditor from 'app/views/settings/projectAlerts/issueEditor';
import SentryDocumentTitle from 'app/components/sentryDocumentTitle';
import SettingsPageHeader from 'app/views/settings/components/settingsPageHeader';
function ProjectAlertsEditor(props) {
    var hasMetricAlerts = props.hasMetricAlerts, location = props.location, params = props.params;
    var projectId = params.projectId;
    var alertType = location.pathname.includes('/alerts/metric-rules/')
        ? 'metric'
        : 'issue';
    var title = t('Edit Alert');
    return (<React.Fragment>
      <SentryDocumentTitle title={title} objSlug={projectId}/>
      <SettingsPageHeader title={title}/>

      {(!hasMetricAlerts || alertType === 'issue') && <IssueEditor {...props}/>}

      {hasMetricAlerts && alertType === 'metric' && <IncidentRulesDetails {...props}/>}
    </React.Fragment>);
}
export default ProjectAlertsEditor;
//# sourceMappingURL=edit.jsx.map