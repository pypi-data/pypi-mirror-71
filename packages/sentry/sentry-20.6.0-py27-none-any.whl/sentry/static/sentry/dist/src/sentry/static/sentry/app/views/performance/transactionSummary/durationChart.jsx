import { __assign, __extends, __read, __spread } from "tslib";
import React from 'react';
import * as ReactRouter from 'react-router';
import { t } from 'app/locale';
import AreaChart from 'app/components/charts/areaChart';
import ChartZoom from 'app/components/charts/chartZoom';
import ErrorPanel from 'app/components/charts/errorPanel';
import TransparentLoadingMask from 'app/components/charts/transparentLoadingMask';
import TransitionChart from 'app/components/charts/transitionChart';
import EventsRequest from 'app/components/charts/eventsRequest';
import ReleaseSeries from 'app/components/charts/releaseSeries';
import QuestionTooltip from 'app/components/questionTooltip';
import { getInterval } from 'app/components/charts/utils';
import { IconWarning } from 'app/icons';
import { getUtcToLocalDateObject } from 'app/utils/dates';
import withApi from 'app/utils/withApi';
import { decodeScalar } from 'app/utils/queryString';
import theme from 'app/utils/theme';
import { getDuration } from 'app/utils/formatters';
import getDynamicText from 'app/utils/getDynamicText';
import { HeaderTitleLegend } from '../styles';
var QUERY_KEYS = [
    'environment',
    'project',
    'query',
    'start',
    'end',
    'statsPeriod',
];
var YAXIS_VALUES = ['p50()', 'p75()', 'p95()', 'p99()', 'p100()'];
/**
 * Fetch and render a stacked area chart that shows duration
 * percentiles over the past 7 days
 */
var DurationChart = /** @class */ (function (_super) {
    __extends(DurationChart, _super);
    function DurationChart() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    DurationChart.prototype.render = function () {
        var _a = this.props, api = _a.api, project = _a.project, environment = _a.environment, organization = _a.organization, query = _a.query, statsPeriod = _a.statsPeriod, router = _a.router;
        var start = this.props.start
            ? getUtcToLocalDateObject(this.props.start)
            : undefined;
        var end = this.props.end ? getUtcToLocalDateObject(this.props.end) : undefined;
        var utc = decodeScalar(router.location.query.utc);
        var legend = {
            right: 10,
            top: 0,
            icon: 'circle',
            itemHeight: 8,
            itemWidth: 8,
            itemGap: 12,
            align: 'left',
            textStyle: {
                verticalAlign: 'top',
                fontSize: 11,
                fontFamily: 'Rubik',
            },
        };
        var tooltip = {
            valueFormatter: function (value) {
                return getDuration(value / 1000, 2);
            },
        };
        var datetimeSelection = {
            start: start || null,
            end: end || null,
            period: statsPeriod,
        };
        return (<React.Fragment>
        <HeaderTitleLegend>
          {t('Duration Breakdown')}
          <QuestionTooltip size="sm" position="top" title={t("Duration Breakdown reflects transaction durations by percentile over time.")}/>
        </HeaderTitleLegend>
        <ChartZoom router={router} period={statsPeriod} projects={project} environments={environment}>
          {function (zoomRenderProps) { return (<EventsRequest api={api} organization={organization} period={statsPeriod} project={__spread(project)} environment={__spread(environment)} start={start} end={end} interval={getInterval(datetimeSelection, true)} showLoading={false} query={query} includePrevious={false} yAxis={YAXIS_VALUES}>
              {function (_a) {
            var results = _a.results, errored = _a.errored, loading = _a.loading, reloading = _a.reloading;
            if (errored) {
                return (<ErrorPanel>
                      <IconWarning color="gray500" size="lg"/>
                    </ErrorPanel>);
            }
            var colors = (results && theme.charts.getColorPalette(results.length - 2)) || [];
            // Create a list of series based on the order of the fields,
            // We need to flip it at the end to ensure the series stack right.
            var series = results
                ? results
                    .map(function (values, i) {
                    return __assign(__assign({}, values), { color: colors[i], lineStyle: {
                            opacity: 0,
                        } });
                })
                    .reverse()
                : [];
            return (<ReleaseSeries start={start} end={end} period={statsPeriod} utc={utc} api={api} projects={project}>
                    {function (_a) {
                var releaseSeries = _a.releaseSeries;
                return (<TransitionChart loading={loading} reloading={reloading}>
                        <TransparentLoadingMask visible={reloading}/>
                        {getDynamicText({
                    value: (<AreaChart {...zoomRenderProps} legend={legend} series={__spread(series, releaseSeries)} seriesOptions={{
                        showSymbol: false,
                    }} tooltip={tooltip} grid={{
                        left: '10px',
                        right: '10px',
                        top: '40px',
                        bottom: '0px',
                    }}/>),
                    fixed: 'Duration Chart',
                })}
                      </TransitionChart>);
            }}
                  </ReleaseSeries>);
        }}
            </EventsRequest>); }}
        </ChartZoom>
      </React.Fragment>);
    };
    return DurationChart;
}(React.Component));
export default withApi(ReactRouter.withRouter(DurationChart));
//# sourceMappingURL=durationChart.jsx.map