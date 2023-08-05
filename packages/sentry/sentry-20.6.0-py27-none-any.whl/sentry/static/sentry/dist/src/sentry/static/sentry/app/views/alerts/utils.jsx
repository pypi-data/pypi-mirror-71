import { __assign, __rest } from "tslib";
import { getAggregateAlias } from 'app/utils/discover/fields';
import { getUtcDateString } from 'app/utils/dates';
import EventView from 'app/utils/discover/eventView';
import { Dataset } from 'app/views/settings/incidentRules/types';
import { PRESET_AGGREGATES } from 'app/views/settings/incidentRules/presets';
import { IncidentStatus } from './types';
export function fetchIncident(api, orgId, alertId) {
    return api.requestPromise("/organizations/" + orgId + "/incidents/" + alertId + "/");
}
export function fetchIncidentStats(api, orgId, alertId) {
    return api.requestPromise("/organizations/" + orgId + "/incidents/" + alertId + "/stats/");
}
export function updateSubscription(api, orgId, alertId, isSubscribed) {
    var method = isSubscribed ? 'POST' : 'DELETE';
    return api.requestPromise("/organizations/" + orgId + "/incidents/" + alertId + "/subscriptions/", {
        method: method,
    });
}
export function updateStatus(api, orgId, alertId, status) {
    return api.requestPromise("/organizations/" + orgId + "/incidents/" + alertId + "/", {
        method: 'PUT',
        data: {
            status: status,
        },
    });
}
/**
 * Is incident open?
 *
 * @param {Object} incident Incident object
 * @returns {Boolean}
 */
export function isOpen(incident) {
    switch (incident.status) {
        case IncidentStatus.CLOSED:
            return false;
        default:
            return true;
    }
}
export function getIncidentMetricPreset(incident) {
    var _a, _b;
    var alertRule = incident === null || incident === void 0 ? void 0 : incident.alertRule;
    var aggregate = (_a = alertRule === null || alertRule === void 0 ? void 0 : alertRule.aggregate) !== null && _a !== void 0 ? _a : '';
    var dataset = (_b = alertRule === null || alertRule === void 0 ? void 0 : alertRule.dataset) !== null && _b !== void 0 ? _b : Dataset.ERRORS;
    return PRESET_AGGREGATES.find(function (p) { return p.validDataset.includes(dataset) && p.match.test(aggregate); });
}
/**
 * Gets start and end date query parameters from stats
 */
export function getStartEndFromStats(stats) {
    var start = getUtcDateString(stats.eventStats.data[0][0] * 1000);
    var end = getUtcDateString(stats.eventStats.data[stats.eventStats.data.length - 1][0] * 1000);
    return { start: start, end: end };
}
/**
 * Gets the URL for a discover view of the incident with the following default
 * parameters:
 *
 * - Ordered by the incident aggregate, descending
 * - yAxis maps to the aggregate
 * - The following fields are displayed:
 *   - For Error dataset alerts: [issue, count(), count_unique(user)]
 *   - For Transaction dataset alerts: [transaction, count()]
 * - Start and end are scoped to the same period as the alert rule
 */
export function getIncidentDiscoverUrl(opts) {
    var _a;
    var orgSlug = opts.orgSlug, projects = opts.projects, incident = opts.incident, stats = opts.stats, extraQueryParams = opts.extraQueryParams;
    if (!projects || !projects.length || !incident || !stats) {
        return '';
    }
    var timeWindowString = incident.alertRule.timeWindow + "m";
    var _b = getStartEndFromStats(stats), start = _b.start, end = _b.end;
    var discoverQuery = __assign({ id: undefined, name: (incident && incident.title) || '', orderby: "-" + getAggregateAlias(incident.alertRule.aggregate), yAxis: incident.alertRule.aggregate, query: (_a = incident === null || incident === void 0 ? void 0 : incident.discoverQuery) !== null && _a !== void 0 ? _a : '', projects: projects
            .filter(function (_a) {
            var slug = _a.slug;
            return incident.projects.includes(slug);
        })
            .map(function (_a) {
            var id = _a.id;
            return Number(id);
        }), version: 2, fields: incident.alertRule.dataset === Dataset.ERRORS
            ? ['issue', 'count()', 'count_unique(user)']
            : ['transaction', incident.alertRule.aggregate], start: start,
        end: end }, extraQueryParams);
    var discoverView = EventView.fromSavedQuery(discoverQuery);
    var _c = discoverView.getResultsViewUrlTarget(orgSlug), query = _c.query, toObject = __rest(_c, ["query"]);
    return __assign({ query: __assign(__assign({}, query), { interval: timeWindowString }) }, toObject);
}
//# sourceMappingURL=utils.jsx.map