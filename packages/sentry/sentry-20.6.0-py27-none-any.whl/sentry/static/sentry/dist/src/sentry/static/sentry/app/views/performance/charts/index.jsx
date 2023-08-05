import { __extends } from "tslib";
import React from 'react';
import withApi from 'app/utils/withApi';
import { getInterval } from 'app/components/charts/utils';
import LoadingPanel from 'app/components/charts/loadingPanel';
import QuestionTooltip from 'app/components/questionTooltip';
import getDynamicText from 'app/utils/getDynamicText';
import { getParams } from 'app/components/organizations/globalSelectionHeader/getParams';
import { Panel } from 'app/components/panels';
import EventsRequest from 'app/components/charts/eventsRequest';
import { getUtcToLocalDateObject } from 'app/utils/dates';
import { IconWarning } from 'app/icons';
import { AXIS_OPTIONS } from '../constants';
import { HeaderContainer, HeaderTitle, ErrorPanel } from '../styles';
import Chart from './chart';
import Footer from './footer';
var Container = /** @class */ (function (_super) {
    __extends(Container, _super);
    function Container() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    Container.prototype.getChartParameters = function () {
        var location = this.props.location;
        var left = AXIS_OPTIONS.find(function (opt) { return opt.value === location.query.left; }) || AXIS_OPTIONS[0];
        var right = AXIS_OPTIONS.find(function (opt) { return opt.value === location.query.right; }) || AXIS_OPTIONS[1];
        return [left, right];
    };
    Container.prototype.render = function () {
        var _a = this.props, api = _a.api, organization = _a.organization, location = _a.location, eventView = _a.eventView, router = _a.router, keyTransactions = _a.keyTransactions;
        // construct request parameters for fetching chart data
        var globalSelection = eventView.getGlobalSelection();
        var start = globalSelection.start
            ? getUtcToLocalDateObject(globalSelection.start)
            : undefined;
        var end = globalSelection.end
            ? getUtcToLocalDateObject(globalSelection.end)
            : undefined;
        var utc = getParams(location.query).utc;
        var axisOptions = this.getChartParameters();
        return (<Panel>
        <EventsRequest organization={organization} api={api} period={globalSelection.statsPeriod} project={globalSelection.project} environment={globalSelection.environment} start={start} end={end} interval={getInterval({
            start: start || null,
            end: end || null,
            period: globalSelection.statsPeriod,
        }, true)} showLoading={false} query={eventView.getEventsAPIPayload(location).query} includePrevious={false} yAxis={axisOptions.map(function (opt) { return opt.value; })} keyTransactions={keyTransactions}>
          {function (_a) {
            var loading = _a.loading, reloading = _a.reloading, errored = _a.errored, results = _a.results;
            if (errored) {
                return (<ErrorPanel>
                  <IconWarning color="gray500" size="lg"/>
                </ErrorPanel>);
            }
            return (<React.Fragment>
                <HeaderContainer>
                  {axisOptions.map(function (option, i) { return (<div key={option.label + ":" + i}>
                      <HeaderTitle>
                        {option.label}
                        <QuestionTooltip position="top" size="sm" title={option.tooltip}/>
                      </HeaderTitle>
                    </div>); })}
                </HeaderContainer>
                {results ? (getDynamicText({
                value: (<Chart data={results} loading={loading || reloading} router={router} statsPeriod={globalSelection.statsPeriod} utc={utc === 'true'} projects={globalSelection.project} environments={globalSelection.environment}/>),
                fixed: 'apdex and throughput charts',
            })) : (<LoadingPanel data-test-id="events-request-loading"/>)}
              </React.Fragment>);
        }}
        </EventsRequest>
        <Footer api={api} leftAxis={axisOptions[0].value} rightAxis={axisOptions[1].value} organization={organization} eventView={eventView} location={location}/>
      </Panel>);
    };
    return Container;
}(React.Component));
export default withApi(Container);
//# sourceMappingURL=index.jsx.map