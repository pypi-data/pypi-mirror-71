import React from 'react';
import { getMeta } from 'app/components/events/meta/metaProxy';
import withProjects from 'app/utils/withProjects';
import { generateEventSlug, eventDetailsRoute } from 'app/utils/discover/urls';
import Link from 'app/components/links/link';
import getBreadcrumbCustomRendererValue from '../../breadcrumbs/getBreadcrumbCustomRendererValue';
import Summary from './summary';
var Default = function (_a) {
    var breadcrumb = _a.breadcrumb, event = _a.event, orgId = _a.orgId;
    return (<Summary kvData={breadcrumb.data}>
    {(breadcrumb === null || breadcrumb === void 0 ? void 0 : breadcrumb.message) &&
        getBreadcrumbCustomRendererValue({
            value: (<FormatMessage event={event} orgId={orgId} breadcrumb={breadcrumb} message={breadcrumb.message}/>),
            meta: getMeta(breadcrumb, 'message'),
        })}
  </Summary>);
};
function isEventId(maybeEventId) {
    // maybeEventId is an event id if it's a hex string of 32 characters long
    return /^[a-fA-F0-9]{32}$/.test(maybeEventId);
}
var FormatMessage = withProjects(function FormatMessageInner(_a) {
    var event = _a.event, message = _a.message, breadcrumb = _a.breadcrumb, projects = _a.projects, loadingProjects = _a.loadingProjects, orgId = _a.orgId;
    if (!loadingProjects &&
        typeof orgId === 'string' &&
        breadcrumb.category === 'sentry.transaction' &&
        isEventId(message)) {
        var maybeProject = projects.find(function (project) {
            return project.id === event.projectID;
        });
        if (!maybeProject) {
            return <React.Fragment>{message}</React.Fragment>;
        }
        var projectSlug = maybeProject.slug;
        var eventSlug = generateEventSlug({ project: projectSlug, id: message });
        return <Link to={eventDetailsRoute({ orgSlug: orgId, eventSlug: eventSlug })}>{message}</Link>;
    }
    return <React.Fragment>{message}</React.Fragment>;
});
export default Default;
//# sourceMappingURL=default.jsx.map