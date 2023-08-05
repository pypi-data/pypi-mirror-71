import { __extends, __rest } from "tslib";
import isNumber from 'lodash/isNumber';
import isString from 'lodash/isString';
import PropTypes from 'prop-types';
import React from 'react';
import moment from 'moment-timezone';
import ConfigStore from 'app/stores/configStore';
import { t } from 'app/locale';
var ONE_MINUTE_IN_MS = 60000;
var TimeSince = /** @class */ (function (_super) {
    __extends(TimeSince, _super);
    function TimeSince() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            relative: '',
        };
        _this.ticker = null;
        _this.setRelativeDateTicker = function () {
            _this.ticker = window.setTimeout(function () {
                _this.setState({
                    relative: getRelativeDate(_this.props.date, _this.props.suffix),
                });
                _this.setRelativeDateTicker();
            }, ONE_MINUTE_IN_MS);
        };
        return _this;
    }
    // TODO(ts) TODO(emotion): defining the props type breaks emotion's typings
    // See: https://github.com/emotion-js/emotion/pull/1514
    TimeSince.getDerivedStateFromProps = function (props) {
        return {
            relative: getRelativeDate(props.date, props.suffix),
        };
    };
    TimeSince.prototype.componentDidMount = function () {
        this.setRelativeDateTicker();
    };
    TimeSince.prototype.componentWillUnmount = function () {
        if (this.ticker) {
            window.clearTimeout(this.ticker);
            this.ticker = null;
        }
    };
    TimeSince.prototype.render = function () {
        var _a;
        var _b = this.props, date = _b.date, _suffix = _b.suffix, className = _b.className, props = __rest(_b, ["date", "suffix", "className"]);
        var dateObj = getDateObj(date);
        var user = ConfigStore.get('user');
        var options = user ? user.options : null;
        var format = (options === null || options === void 0 ? void 0 : options.clock24Hours) ? 'MMMM D YYYY HH:mm:ss z' : 'LLL z';
        return (<time dateTime={dateObj.toISOString()} title={moment.tz(dateObj, (_a = options === null || options === void 0 ? void 0 : options.timezone) !== null && _a !== void 0 ? _a : '').format(format)} className={className} {...props}>
        {this.state.relative}
      </time>);
    };
    TimeSince.propTypes = {
        date: PropTypes.any.isRequired,
        suffix: PropTypes.string,
    };
    TimeSince.defaultProps = {
        suffix: 'ago',
    };
    return TimeSince;
}(React.PureComponent));
export default TimeSince;
function getDateObj(date) {
    if (isString(date) || isNumber(date)) {
        date = new Date(date);
    }
    return date;
}
function getRelativeDate(currentDateTime, suffix) {
    var date = getDateObj(currentDateTime);
    if (!suffix) {
        return moment(date).fromNow(true);
    }
    else if (suffix === 'ago') {
        return moment(date).fromNow();
    }
    else if (suffix === 'old') {
        return t('%(time)s old', { time: moment(date).fromNow(true) });
    }
    else {
        throw new Error('Unsupported time format suffix');
    }
}
//# sourceMappingURL=timeSince.jsx.map