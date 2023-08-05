import { __awaiter, __generator, __makeTemplateObject, __read, __spread } from "tslib";
import React from 'react';
import PropTypes from 'prop-types';
import { browserHistory } from 'react-router';
import styled from '@emotion/styled';
import { t } from 'app/locale';
import SentryTypes from 'app/sentryTypes';
import { getInterval } from 'app/components/charts/utils';
import { getFormattedDate, getUtcDateString, intervalToMilliseconds, } from 'app/utils/dates';
import EventsRequest from 'app/components/charts/eventsRequest';
import LineChart from 'app/components/charts/lineChart';
import MarkLine from 'app/components/charts/components/markLine';
import { Panel } from 'app/components/panels';
import withApi from 'app/utils/withApi';
import withGlobalSelection from 'app/utils/withGlobalSelection';
import { tokenizeSearch, stringifyQueryObject } from 'app/utils/tokenizeSearch';
import theme from 'app/utils/theme';
import { eventDetailsRouteWithEventView, generateEventSlug } from 'app/utils/discover/urls';
import { PIN_ICON } from '../data';
/**
 * Generate the data to display a vertical line for the current
 * event on the graph.
 */
var getCurrentEventMarker = function (currentEvent) {
    var title = t('Current Event');
    var eventTime = +new Date(currentEvent.dateCreated || (currentEvent.endTimestamp || 0) * 1000);
    return {
        type: 'line',
        data: [],
        markLine: MarkLine({
            symbol: [PIN_ICON, 'none'],
            symbolSize: [16, 150],
            lineStyle: {
                normal: {
                    color: theme.redLight,
                    type: 'solid',
                    width: 1,
                },
            },
            tooltip: {
                formatter: function () { return "<div>" + getFormattedDate(eventTime, 'MMM D, YYYY LT') + "</div>"; },
            },
            label: {
                show: false,
            },
            data: [
                {
                    xAxis: eventTime,
                    name: title,
                },
            ],
        }),
    };
};
/**
 * Handle click events on line markers
 *
 * When a user clicks on a marker we want to update the events details page
 * to display an event from that time slice. While each graph slice
 * could contain thousands of events, we do a search to get the latest
 * event in the slice.
 */
var handleClick = function (series, _a) {
    var api = _a.api, currentEvent = _a.currentEvent, organization = _a.organization, queryString = _a.queryString, field = _a.field, interval = _a.interval, selection = _a.selection, eventView = _a.eventView;
    return __awaiter(this, void 0, void 0, function () {
        var value, sortField, endValue, startValue, newQuery, query, url, response, e_1, event, eventSlug;
        return __generator(this, function (_b) {
            switch (_b.label) {
                case 0:
                    value = series.value[0];
                    sortField = field.includes('timestamp')
                        ? 'timestamp'
                        : field.includes('last_seen')
                            ? 'last_seen'
                            : null;
                    endValue = getUtcDateString(value + intervalToMilliseconds(interval));
                    startValue = getUtcDateString(value);
                    newQuery = tokenizeSearch(queryString);
                    newQuery.timestamp = [">" + startValue, "<=" + endValue];
                    query = {
                        environment: selection.environments,
                        limit: 1,
                        referenceEvent: currentEvent.projectSlug + ":" + currentEvent.eventID,
                        query: stringifyQueryObject(newQuery),
                        field: field,
                    };
                    // Perserve the current query window
                    if (selection.datetime.period) {
                        query.statsPeriod = selection.datetime.period;
                    }
                    else {
                        query.start = selection.datetime.start;
                        query.end = selection.datetime.end;
                    }
                    if (sortField !== null) {
                        query.sort = sortField;
                    }
                    url = "/organizations/" + organization.slug + "/eventsv2/";
                    _b.label = 1;
                case 1:
                    _b.trys.push([1, 3, , 4]);
                    return [4 /*yield*/, api.requestPromise(url, {
                            method: 'GET',
                            query: query,
                        })];
                case 2:
                    response = _b.sent();
                    return [3 /*break*/, 4];
                case 3:
                    e_1 = _b.sent();
                    // Do nothing, user could have clicked on a blank space.
                    return [2 /*return*/];
                case 4:
                    if (!response.data || !response.data.length) {
                        // Did not find anything.
                        return [2 /*return*/];
                    }
                    event = response.data[0];
                    eventSlug = generateEventSlug(event);
                    browserHistory.push(eventDetailsRouteWithEventView({ eventSlug: eventSlug, orgSlug: organization.slug, eventView: eventView }));
                    return [2 /*return*/];
            }
        });
    });
};
/**
 * Render a graph of event volumes for the current group + event.
 */
var LineGraph = function (props) {
    var api = props.api, organization = props.organization, location = props.location, selection = props.selection, currentEvent = props.currentEvent, eventView = props.eventView;
    var isUtc = selection.datetime.utc;
    var interval = getInterval(selection.datetime, true);
    var tooltip = {
        formatAxisLabel: function (value) { return getFormattedDate(value, 'lll', { local: !isUtc }); },
    };
    var queryString = eventView.getQuery(location.query.query);
    var referenceEvent = currentEvent.projectSlug + ":" + currentEvent.eventID;
    return (<StyledPanel>
      <EventsRequest api={api} organization={organization} period={selection.datetime.period} project={selection.projects} environment={selection.environments} 
    // TODO(ts): adjust. Expects date, got strings
    start={selection.datetime.start} end={selection.datetime.end} interval={interval} showLoading query={queryString} field={eventView.getFields()} referenceEvent={referenceEvent} includePrevious={false}>
        {function (_a) {
        var loading = _a.loading, reloading = _a.reloading, timeseriesData = _a.timeseriesData;
        return (<LineChart {...selection.datetime} isGroupedByDate loading={loading} reloading={reloading} series={__spread(timeseriesData, [getCurrentEventMarker(currentEvent)])} seriesOptions={{
            showSymbol: false,
        }} onClick={function (series) {
            return handleClick(series, {
                field: eventView.getFields(),
                api: api,
                organization: organization,
                currentEvent: currentEvent,
                interval: interval,
                selection: selection,
                queryString: queryString,
                eventView: eventView,
            });
        }} tooltip={tooltip} grid={{
            left: '24px',
            right: '24px',
            top: '24px',
            bottom: '12px',
        }}/>);
    }}
      </EventsRequest>
    </StyledPanel>);
};
// eChart does not recalculate width
var StyledPanel = styled(Panel)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  .echarts-for-react div:first-child {\n    width: 100% !important;\n  }\n  image {\n    y: 0px;\n  }\n"], ["\n  .echarts-for-react div:first-child {\n    width: 100% !important;\n  }\n  image {\n    y: 0px;\n  }\n"])));
LineGraph.propTypes = {
    api: PropTypes.object.isRequired,
    currentEvent: SentryTypes.Event.isRequired,
    location: PropTypes.object.isRequired,
    organization: SentryTypes.Organization.isRequired,
    selection: PropTypes.object.isRequired,
};
export default withGlobalSelection(withApi(LineGraph));
var templateObject_1;
//# sourceMappingURL=lineGraph.jsx.map