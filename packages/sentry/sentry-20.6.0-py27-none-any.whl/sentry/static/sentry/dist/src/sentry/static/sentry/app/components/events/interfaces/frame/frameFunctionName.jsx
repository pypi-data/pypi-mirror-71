import { __extends, __rest } from "tslib";
import React from 'react';
import PropTypes from 'prop-types';
import { t } from 'app/locale';
import { getMeta } from 'app/components/events/meta/metaProxy';
import AnnotatedText from 'app/components/events/meta/annotatedText';
var FrameFunctionName = /** @class */ (function (_super) {
    __extends(FrameFunctionName, _super);
    function FrameFunctionName() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            rawFunction: false,
        };
        _this.toggle = function (event) {
            event.stopPropagation();
            _this.setState(function (_a) {
                var rawFunction = _a.rawFunction;
                return ({ rawFunction: !rawFunction });
            });
        };
        return _this;
    }
    FrameFunctionName.prototype.getToggleValue = function (withRawFunctionCondition) {
        if (withRawFunctionCondition === void 0) { withRawFunctionCondition = false; }
        var frame = this.props.frame;
        var valueOutput = t('<unknown>');
        if (withRawFunctionCondition) {
            var rawFunction = this.state.rawFunction;
            if (!rawFunction) {
                if (frame.function) {
                    valueOutput = {
                        value: frame.function,
                        meta: getMeta(frame, 'function'),
                    };
                }
            }
        }
        else {
            if (frame.function) {
                valueOutput = {
                    value: frame.function,
                    meta: getMeta(frame, 'function'),
                };
            }
        }
        if (typeof valueOutput === 'string' && frame.rawFunction) {
            valueOutput = {
                value: frame.rawFunction,
                meta: getMeta(frame, 'rawFunction'),
            };
        }
        if (typeof valueOutput === 'string') {
            return valueOutput;
        }
        return <AnnotatedText value={valueOutput.value} meta={valueOutput.meta}/>;
    };
    FrameFunctionName.prototype.render = function () {
        var _a = this.props, frame = _a.frame, props = __rest(_a, ["frame"]);
        var func = frame.function;
        var rawFunc = frame.rawFunction;
        var canToggle = rawFunc && func && func !== rawFunc;
        if (!canToggle) {
            return <code {...props}>{this.getToggleValue()}</code>;
        }
        var title = this.state.rawFunction ? undefined : rawFunc;
        return (<code {...props} title={title} onClick={this.toggle}>
        {this.getToggleValue(true)}
      </code>);
    };
    FrameFunctionName.propTypes = {
        frame: PropTypes.object,
    };
    return FrameFunctionName;
}(React.Component));
export default FrameFunctionName;
//# sourceMappingURL=frameFunctionName.jsx.map