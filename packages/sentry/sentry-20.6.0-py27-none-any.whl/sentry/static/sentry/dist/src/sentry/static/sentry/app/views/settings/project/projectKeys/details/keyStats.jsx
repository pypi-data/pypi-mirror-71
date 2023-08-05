import { __extends, __read } from "tslib";
import React from 'react';
import { Panel, PanelBody, PanelHeader } from 'app/components/panels';
import { t } from 'app/locale';
import EmptyMessage from 'app/views/settings/components/emptyMessage';
import LoadingError from 'app/components/loadingError';
import Placeholder from 'app/components/placeholder';
import StackedBarChart from 'app/components/stackedBarChart';
var getInitialState = function () {
    var until = Math.floor(new Date().getTime() / 1000);
    return {
        since: until - 3600 * 24 * 30,
        until: until,
        loading: true,
        error: false,
        stats: null,
        emptyStats: false,
    };
};
var KeyStats = /** @class */ (function (_super) {
    __extends(KeyStats, _super);
    function KeyStats() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = getInitialState();
        _this.fetchData = function () {
            var _a = _this.props.params, keyId = _a.keyId, orgId = _a.orgId, projectId = _a.projectId;
            _this.props.api.request("/projects/" + orgId + "/" + projectId + "/keys/" + keyId + "/stats/", {
                query: {
                    since: _this.state.since,
                    until: _this.state.until,
                    resolution: '1d',
                },
                success: function (data) {
                    var emptyStats = true;
                    var stats = data.map(function (p) {
                        if (p.total) {
                            emptyStats = false;
                        }
                        return {
                            x: p.ts,
                            y: [p.accepted, p.dropped],
                        };
                    });
                    _this.setState({
                        stats: stats,
                        emptyStats: emptyStats,
                        error: false,
                        loading: false,
                    });
                },
                error: function () {
                    _this.setState({ error: true, loading: false });
                },
            });
        };
        _this.renderTooltip = function (point, _pointIdx, chart) {
            var timeLabel = chart.getTimeLabel(point);
            var _a = __read(point.y, 3), accepted = _a[0], dropped = _a[1], filtered = _a[2];
            return (<div style={{ width: '150px' }}>
        <div className="time-label">{timeLabel}</div>
        <div className="value-label">
          {accepted.toLocaleString()} accepted
          {dropped > 0 && (<React.Fragment>
              <br />
              {dropped.toLocaleString()} rate limited
            </React.Fragment>)}
          {filtered > 0 && (<React.Fragment>
              <br />
              {filtered.toLocaleString()} filtered
            </React.Fragment>)}
        </div>
      </div>);
        };
        return _this;
    }
    KeyStats.prototype.componentDidMount = function () {
        this.fetchData();
    };
    KeyStats.prototype.render = function () {
        if (this.state.error) {
            return <LoadingError onRetry={this.fetchData}/>;
        }
        return (<Panel>
        <PanelHeader>{t('Key usage in the last 30 days (by day)')}</PanelHeader>
        <PanelBody>
          {this.state.loading ? (<Placeholder height="150px"/>) : !this.state.emptyStats ? (<StackedBarChart points={this.state.stats} height={150} label="events" barClasses={['accepted', 'rate-limited']} minHeights={[1, 0]} className="standard-barchart" style={{ border: 'none' }} tooltip={this.renderTooltip}/>) : (<EmptyMessage title={t('Nothing recorded in the last 30 days.')} description={t('Total events captured using these credentials.')}/>)}
        </PanelBody>
      </Panel>);
    };
    return KeyStats;
}(React.Component));
export default KeyStats;
//# sourceMappingURL=keyStats.jsx.map