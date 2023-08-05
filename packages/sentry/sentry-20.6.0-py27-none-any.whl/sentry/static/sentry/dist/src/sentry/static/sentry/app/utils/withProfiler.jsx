import { __extends } from "tslib";
import React from 'react';
import { Integrations } from '@sentry/apm';
import getDisplayName from 'app/utils/getDisplayName';
export default function withProfiler(WrappedComponent) {
    var _a;
    var componentDisplayName = getDisplayName(WrappedComponent);
    return _a = /** @class */ (function (_super) {
            __extends(class_1, _super);
            function class_1() {
                var _this = _super !== null && _super.apply(this, arguments) || this;
                _this.activity = Integrations.Tracing.pushActivity(componentDisplayName, {
                    data: {},
                    op: 'react',
                    description: "<" + componentDisplayName + ">",
                }, {
                    // After this timeout we'll pop this activity regardless
                    // Set to 30s because that's the length of our longest requests
                    autoPopAfter: 30000,
                });
                // For whatever reason it's not guaranteed that `finishProfile` will be
                // called, that's why we need the previously described timeout to make
                // sure our transaction will be finished.
                _this.finishProfile = function () {
                    if (!_this.activity) {
                        return;
                    }
                    Integrations.Tracing.popActivity(_this.activity);
                    _this.activity = null;
                };
                return _this;
            }
            class_1.prototype.componentWillUnmount = function () {
                this.finishProfile();
            };
            class_1.prototype.render = function () {
                return (<WrappedComponent {...this.props} finishProfile={this.finishProfile}/>);
            };
            return class_1;
        }(React.Component)),
        _a.displayName = "profiler(" + componentDisplayName + ")",
        _a;
}
//# sourceMappingURL=withProfiler.jsx.map