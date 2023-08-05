import { __read, __spread } from "tslib";
import React from 'react';
import moment from 'moment';
import { t } from 'app/locale';
import space from 'app/styles/space';
import theme from 'app/utils/theme';
import LineChart from 'app/components/charts/lineChart';
import MarkPoint from 'app/components/charts/components/markPoint';
import MarkLine from 'app/components/charts/components/markLine';
import closedSymbol from './closedSymbol';
import detectedSymbol from './detectedSymbol';
/**
 * So we'll have to see how this looks with real data, but echarts requires
 * an explicit (x,y) value to draw a symbol (incident detected/closed bubble).
 *
 * This uses the closest date *without* going over.
 *
 * AFAICT we can't give it an x-axis value and have it draw on the line,
 * so we probably need to calculate the y-axis value ourselves if we want it placed
 * at the exact time.
 *
 * @param data Data array
 * @param needle the target timestamp
 */
function getNearbyIndex(data, needle) {
    // `data` is sorted, return the first index whose value (timestamp) is > `needle`
    var index = data.findIndex(function (_a) {
        var _b = __read(_a, 1), ts = _b[0];
        return ts > needle;
    });
    // this shouldn't happen, as we try to buffer dates before start/end dates
    if (index === 0) {
        return 0;
    }
    return index !== -1 ? index - 1 : data.length - 1;
}
var Chart = function (props) {
    var aggregate = props.aggregate, data = props.data, detected = props.detected, closed = props.closed, triggers = props.triggers;
    var detectedTs = detected && moment.utc(detected).unix();
    var closedTs = closed && moment.utc(closed).unix();
    var chartData = data.map(function (_a) {
        var _b = __read(_a, 2), ts = _b[0], val = _b[1];
        return [
            ts * 1000,
            val.length ? val.reduce(function (acc, _a) {
                var count = (_a === void 0 ? { count: 0 } : _a).count;
                return acc + count;
            }, 0) : 0,
        ];
    });
    var detectedCoordinate = detectedTs
        ? chartData[getNearbyIndex(data, detectedTs)]
        : undefined;
    var showClosedMarker = data && closedTs && data[data.length - 1] && data[data.length - 1][0] >= closedTs
        ? true
        : false;
    var closedCoordinate = closedTs && showClosedMarker ? chartData[getNearbyIndex(data, closedTs)] : undefined;
    var seriesName = aggregate;
    var warningTrigger = triggers === null || triggers === void 0 ? void 0 : triggers.find(function (trig) { return trig.label === 'warning'; });
    var criticalTrigger = triggers === null || triggers === void 0 ? void 0 : triggers.find(function (trig) { return trig.label === 'critical'; });
    var warningTriggerAlertThreshold = typeof (warningTrigger === null || warningTrigger === void 0 ? void 0 : warningTrigger.alertThreshold) === 'number'
        ? warningTrigger === null || warningTrigger === void 0 ? void 0 : warningTrigger.alertThreshold : undefined;
    var warningTriggerResolveThreshold = typeof (warningTrigger === null || warningTrigger === void 0 ? void 0 : warningTrigger.resolveThreshold) === 'number'
        ? warningTrigger === null || warningTrigger === void 0 ? void 0 : warningTrigger.resolveThreshold : undefined;
    var criticalTriggerAlertThreshold = typeof (criticalTrigger === null || criticalTrigger === void 0 ? void 0 : criticalTrigger.alertThreshold) === 'number'
        ? criticalTrigger === null || criticalTrigger === void 0 ? void 0 : criticalTrigger.alertThreshold : undefined;
    var criticalTriggerResolveThreshold = typeof (criticalTrigger === null || criticalTrigger === void 0 ? void 0 : criticalTrigger.resolveThreshold) === 'number'
        ? criticalTrigger === null || criticalTrigger === void 0 ? void 0 : criticalTrigger.resolveThreshold : undefined;
    return (<LineChart isGroupedByDate showTimeInTooltip grid={{
        left: 0,
        right: 0,
        top: space(2),
        bottom: 0,
    }} series={[
        {
            // e.g. Events or Users
            seriesName: seriesName,
            dataArray: chartData,
            markPoint: MarkPoint({
                data: __spread([
                    {
                        labelForValue: seriesName,
                        seriesName: seriesName,
                        symbol: "image://" + detectedSymbol,
                        name: t('Alert Triggered'),
                        coord: detectedCoordinate,
                    }
                ], (closedTs
                    ? [
                        {
                            labelForValue: seriesName,
                            seriesName: seriesName,
                            symbol: "image://" + closedSymbol,
                            symbolSize: 24,
                            name: t('Alert Resolved'),
                            coord: closedCoordinate,
                        },
                    ]
                    : [])),
            }),
        },
        warningTrigger &&
            warningTriggerAlertThreshold && {
            name: 'Warning Alert',
            type: 'line',
            markLine: MarkLine({
                silent: true,
                lineStyle: { color: theme.yellow400 },
                data: [
                    {
                        yAxis: warningTriggerAlertThreshold,
                    },
                ],
                label: {
                    show: true,
                    position: 'insideEndTop',
                    formatter: 'WARNING',
                    color: theme.yellow400,
                    fontSize: 10,
                },
            }),
            data: [],
        },
        warningTrigger &&
            warningTriggerResolveThreshold && {
            name: 'Warning Resolve',
            type: 'line',
            markLine: MarkLine({
                silent: true,
                lineStyle: { color: theme.gray400 },
                data: [
                    {
                        yAxis: warningTriggerResolveThreshold,
                    },
                ],
                label: {
                    show: true,
                    position: 'insideEndBottom',
                    formatter: 'WARNING RESOLUTION',
                    color: theme.gray400,
                    fontSize: 10,
                },
            }),
            data: [],
        },
        criticalTrigger &&
            criticalTriggerAlertThreshold && {
            name: 'Critical Alert',
            type: 'line',
            markLine: MarkLine({
                silent: true,
                lineStyle: { color: theme.red300 },
                data: [
                    {
                        yAxis: criticalTriggerAlertThreshold,
                    },
                ],
                label: {
                    show: true,
                    position: 'insideEndTop',
                    formatter: 'CRITICAL',
                    color: theme.red400,
                    fontSize: 10,
                },
            }),
            data: [],
        },
        criticalTrigger &&
            criticalTriggerResolveThreshold && {
            name: 'Critical Resolve',
            type: 'line',
            markLine: MarkLine({
                silent: true,
                lineStyle: { color: theme.gray400 },
                data: [
                    {
                        yAxis: criticalTriggerResolveThreshold,
                    },
                ],
                label: {
                    show: true,
                    position: 'insideEndBottom',
                    formatter: 'CRITICAL RESOLUTION',
                    color: theme.gray400,
                    fontSize: 10,
                },
            }),
            data: [],
        },
    ].filter(Boolean)}/>);
};
export default Chart;
//# sourceMappingURL=chart.jsx.map