import { __extends } from "tslib";
import React from 'react';
import isEqual from 'lodash/isEqual';
import LineChart from 'app/components/charts/lineChart';
import AreaChart from 'app/components/charts/areaChart';
import StackedAreaChart from 'app/components/charts/stackedAreaChart';
import theme from 'app/utils/theme';
import { defined } from 'app/utils';
import { getExactDuration } from 'app/utils/formatters';
import { YAxis } from './releaseChartControls';
var HealthChart = /** @class */ (function (_super) {
    __extends(HealthChart, _super);
    function HealthChart() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.formatTooltipValue = function (value) {
            var yAxis = _this.props.yAxis;
            switch (yAxis) {
                case YAxis.SESSION_DURATION:
                    return typeof value === 'number' ? getExactDuration(value, true) : '\u2015';
                case YAxis.CRASH_FREE:
                    return defined(value) ? value + "%" : '\u2015';
                case YAxis.SESSIONS:
                case YAxis.USERS:
                default:
                    return typeof value === 'number' ? value.toLocaleString() : value;
            }
        };
        _this.configureYAxis = function () {
            var yAxis = _this.props.yAxis;
            switch (yAxis) {
                case YAxis.CRASH_FREE:
                    return {
                        max: 100,
                        scale: true,
                        axisLabel: {
                            formatter: '{value}%',
                            color: theme.gray400,
                        },
                    };
                case YAxis.SESSION_DURATION:
                    return {
                        scale: true,
                    };
                case YAxis.SESSIONS:
                case YAxis.USERS:
                default:
                    return undefined;
            }
        };
        _this.getChart = function () {
            var yAxis = _this.props.yAxis;
            switch (yAxis) {
                case YAxis.SESSION_DURATION:
                    return AreaChart;
                case YAxis.SESSIONS:
                case YAxis.USERS:
                    return StackedAreaChart;
                case YAxis.CRASH_FREE:
                default:
                    return LineChart;
            }
        };
        return _this;
    }
    HealthChart.prototype.shouldComponentUpdate = function (nextProps) {
        if (nextProps.reloading || !nextProps.timeseriesData) {
            return false;
        }
        if (isEqual(this.props.timeseriesData, nextProps.timeseriesData)) {
            return false;
        }
        return true;
    };
    HealthChart.prototype.render = function () {
        var _a = this.props, utc = _a.utc, timeseriesData = _a.timeseriesData, zoomRenderProps = _a.zoomRenderProps;
        var Chart = this.getChart();
        var legend = {
            right: 16,
            top: 12,
            selectedMode: false,
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
            data: timeseriesData.map(function (d) { return d.seriesName; }),
        };
        return (<Chart legend={legend} utc={utc} {...zoomRenderProps} series={timeseriesData} isGroupedByDate seriesOptions={{
            showSymbol: false,
        }} grid={{
            left: '24px',
            right: '24px',
            top: '32px',
            bottom: '12px',
        }} yAxis={this.configureYAxis()} tooltip={{ valueFormatter: this.formatTooltipValue }}/>);
    };
    return HealthChart;
}(React.Component));
export default HealthChart;
//# sourceMappingURL=healthChart.jsx.map