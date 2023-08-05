import { __extends } from "tslib";
import React from 'react';
import { Client } from 'app/api';
import getDisplayName from 'app/utils/getDisplayName';
/**
 * HoC that provides "api" client when mounted, and clears API requests when
 * component is unmounted
 */
var withApi = function (WrappedComponent, _a) {
    var persistInFlight = (_a === void 0 ? {} : _a).persistInFlight;
    var _b;
    return _b = /** @class */ (function (_super) {
            __extends(class_1, _super);
            function class_1(props) {
                var _this = _super.call(this, props) || this;
                _this.api = new Client();
                return _this;
            }
            class_1.prototype.componentWillUnmount = function () {
                if (!persistInFlight) {
                    this.api.clear();
                }
            };
            class_1.prototype.render = function () {
                return <WrappedComponent api={this.api} {...this.props}/>;
            };
            return class_1;
        }(React.Component)),
        _b.displayName = "withApi(" + getDisplayName(WrappedComponent) + ")",
        _b;
};
export default withApi;
//# sourceMappingURL=withApi.jsx.map