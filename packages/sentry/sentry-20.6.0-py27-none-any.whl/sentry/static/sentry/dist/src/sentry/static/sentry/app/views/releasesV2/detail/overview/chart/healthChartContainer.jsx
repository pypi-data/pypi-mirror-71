import React from 'react';
import ChartZoom from 'app/components/charts/chartZoom';
import { IconWarning } from 'app/icons';
import TransitionChart from 'app/components/charts/transitionChart';
import TransparentLoadingMask from 'app/components/charts/transparentLoadingMask';
import ErrorPanel from 'app/components/charts/errorPanel';
import HealthChart from './healthChart';
var ReleaseChartContainer = function (_a) {
    var loading = _a.loading, errored = _a.errored, reloading = _a.reloading, chartData = _a.chartData, selection = _a.selection, yAxis = _a.yAxis, router = _a.router;
    var datetime = selection.datetime;
    var utc = datetime.utc, period = datetime.period, start = datetime.start, end = datetime.end;
    return (<React.Fragment>
      <ChartZoom router={router} period={period} utc={utc} start={start} end={end}>
        {function (zoomRenderProps) {
        if (errored) {
            return (<ErrorPanel>
                <IconWarning color="gray500" size="lg"/>
              </ErrorPanel>);
        }
        return (<TransitionChart loading={loading} reloading={reloading}>
              <TransparentLoadingMask visible={reloading}/>
              <HealthChart utc={utc} timeseriesData={chartData} zoomRenderProps={zoomRenderProps} reloading={reloading} yAxis={yAxis}/>
            </TransitionChart>);
    }}
      </ChartZoom>
    </React.Fragment>);
};
export default ReleaseChartContainer;
//# sourceMappingURL=healthChartContainer.jsx.map