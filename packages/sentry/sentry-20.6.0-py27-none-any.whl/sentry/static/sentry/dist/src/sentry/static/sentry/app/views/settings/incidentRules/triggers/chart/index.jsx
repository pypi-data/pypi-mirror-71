var _a;
import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import maxBy from 'lodash/maxBy';
import styled from '@emotion/styled';
import EventsRequest from 'app/components/charts/eventsRequest';
import LoadingMask from 'app/components/loadingMask';
import Placeholder from 'app/components/placeholder';
import space from 'app/styles/space';
import { TimeWindow } from '../../types';
import ThresholdsChart from './thresholdsChart';
/**
 * This is a chart to be used in Metric Alert rules that fetches events based on
 * query, timewindow, and aggregations.
 */
var TriggersChart = /** @class */ (function (_super) {
    __extends(TriggersChart, _super);
    function TriggersChart() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    TriggersChart.prototype.render = function () {
        var _a = this.props, api = _a.api, organization = _a.organization, projects = _a.projects, timeWindow = _a.timeWindow, query = _a.query, aggregate = _a.aggregate, triggers = _a.triggers, environment = _a.environment;
        var period = getPeriodForTimeWindow(timeWindow);
        return (<EventsRequest api={api} organization={organization} query={query} environment={environment ? [environment] : undefined} project={projects.map(function (_a) {
            var id = _a.id;
            return Number(id);
        })} interval={timeWindow + "m"} period={period} yAxis={aggregate} includePrevious={false} currentSeriesName={aggregate}>
        {function (_a) {
            var loading = _a.loading, reloading = _a.reloading, timeseriesData = _a.timeseriesData;
            var maxValue;
            if (timeseriesData && timeseriesData.length && timeseriesData[0].data) {
                maxValue = maxBy(timeseriesData[0].data, function (_a) {
                    var value = _a.value;
                    return value;
                });
            }
            return (<StickyWrapper>
              {loading ? (<ChartPlaceholder />) : (<React.Fragment>
                  <TransparentLoadingMask visible={reloading}/>
                  <ThresholdsChart period={period} maxValue={maxValue ? maxValue.value : maxValue} data={timeseriesData} triggers={triggers}/>
                </React.Fragment>)}
            </StickyWrapper>);
        }}
      </EventsRequest>);
    };
    return TriggersChart;
}(React.PureComponent));
export default TriggersChart;
var TIME_WINDOW_TO_PERIOD = (_a = {},
    _a[TimeWindow.ONE_MINUTE] = '12h',
    _a[TimeWindow.FIVE_MINUTES] = '12h',
    _a[TimeWindow.TEN_MINUTES] = '1d',
    _a[TimeWindow.FIFTEEN_MINUTES] = '3d',
    _a[TimeWindow.THIRTY_MINUTES] = '3d',
    _a[TimeWindow.ONE_HOUR] = '7d',
    _a[TimeWindow.TWO_HOURS] = '7d',
    _a[TimeWindow.FOUR_HOURS] = '7d',
    _a[TimeWindow.ONE_DAY] = '14d',
    _a);
/**
 * Gets a reasonable period given a time window (in minutes)
 *
 * @param timeWindow The time window in minutes
 * @return period The period string to use (e.g. 14d)
 */
function getPeriodForTimeWindow(timeWindow) {
    return TIME_WINDOW_TO_PERIOD[timeWindow];
}
var TransparentLoadingMask = styled(LoadingMask)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  ", ";\n  opacity: 0.4;\n  z-index: 1;\n"], ["\n  ", ";\n  opacity: 0.4;\n  z-index: 1;\n"])), function (p) { return !p.visible && 'display: none;'; });
var ChartPlaceholder = styled(Placeholder)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  margin: ", " 0;\n  height: 184px;\n"], ["\n  margin: ", " 0;\n  height: 184px;\n"])), space(2));
var StickyWrapper = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  position: sticky;\n  top: 69px; /* Height of settings breadcrumb 69px */\n  z-index: ", ";\n  padding: ", " ", " 0;\n  border-bottom: 1px solid ", ";\n  background: rgba(255, 255, 255, 0.9);\n"], ["\n  position: sticky;\n  top: 69px; /* Height of settings breadcrumb 69px */\n  z-index: ", ";\n  padding: ", " ", " 0;\n  border-bottom: 1px solid ", ";\n  background: rgba(255, 255, 255, 0.9);\n"])), function (p) { return p.theme.zIndex.dropdown - 1; }, space(2), space(2), function (p) { return p.theme.borderLight; });
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=index.jsx.map