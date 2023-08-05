import { __extends } from "tslib";
// TODO(matej): this is very similar to app/components/stream/groupChart, will refactor to reusable component in a follow-up PR
import React from 'react';
import LazyLoad from 'react-lazyload';
import { t } from 'app/locale';
import BarChart from 'app/components/barChart';
var HealthStatsChart = /** @class */ (function (_super) {
    __extends(HealthStatsChart, _super);
    function HealthStatsChart() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    HealthStatsChart.prototype.shouldComponentUpdate = function (nextProps) {
        // Sometimes statsPeriod updates before graph data has been
        // pulled from server / propagated down to components ...
        // don't update until data is available
        var data = nextProps.data, period = nextProps.period;
        return data.hasOwnProperty(period);
    };
    HealthStatsChart.prototype.getChartLabel = function () {
        var subject = this.props.subject;
        if (subject === 'users') {
            return t('users');
        }
        return t('sessions');
    };
    HealthStatsChart.prototype.render = function () {
        var _a = this.props, height = _a.height, period = _a.period, data = _a.data;
        var stats = period ? data[period] : null;
        if (!stats || !stats.length) {
            return null;
        }
        var chartData = stats.map(function (point) { return ({ x: point[0], y: point[1] }); });
        return (<LazyLoad debounce={50} height={height}>
        <BarChart points={chartData} height={height} label={this.getChartLabel()} minHeights={[3]} gap={1}/>
      </LazyLoad>);
    };
    HealthStatsChart.defaultProps = {
        height: 24,
    };
    return HealthStatsChart;
}(React.Component));
export default HealthStatsChart;
//# sourceMappingURL=healthStatsChart.jsx.map