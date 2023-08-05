import { __assign, __extends, __makeTemplateObject, __read } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import isEqual from 'lodash/isEqual';
import DropdownControl from 'app/components/dropdownControl';
import DropDownButton from './dropdownButton';
import OptionsGroup from './optionsGroup';
import Header from './header';
var Filter = /** @class */ (function (_super) {
    __extends(Filter, _super);
    function Filter() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            checkAll: true,
            hasTypeOption: false,
            hasLevelOption: false,
            checkedQuantity: _this.props.options.length,
        };
        _this.updateState = function () {
            var options = _this.props.options;
            _this.setState({
                hasTypeOption: options[0].length > 0,
                hasLevelOption: options[1].length > 0,
                checkedQuantity: _this.getCheckedQuantity(),
            });
        };
        _this.handleToggleCheckAll = function () {
            var onCheckAll = _this.props.onCheckAll;
            _this.setState(function (prevState) { return ({
                checkAll: !prevState.checkAll,
            }); }, function () {
                onCheckAll(_this.state.checkAll);
            });
        };
        _this.getCheckedQuantity = function () {
            var options = _this.props.options;
            var checkedQuantity = 0;
            for (var index in options) {
                for (var option in options[index]) {
                    if (options[index][option].isChecked) {
                        checkedQuantity += 1;
                    }
                }
            }
            return checkedQuantity;
        };
        _this.filterOptionsFirstStep = function (options, option) {
            var filteredOptions = options.map(function (type) {
                if (isEqual(type, option)) {
                    return __assign(__assign({}, type), { isChecked: !type.isChecked });
                }
                return type;
            });
            var checkedOptions = filteredOptions.filter(function (t) { return t.isChecked; });
            return [filteredOptions, checkedOptions];
        };
        _this.filterOptionsByLevel = function (options, option) {
            // Filter levels
            var _a = __read(_this.filterOptionsFirstStep(options[1], option), 2), levels = _a[0], checkedLevels = _a[1];
            // Filter types
            var types = options[0].map(function (type) {
                if (!type.levels.some(function (level) {
                    return checkedLevels.some(function (checkedLevel) { return checkedLevel.type === level; });
                })) {
                    var isAllLevelsWithTypeDisabled = levels
                        .filter(function (l) { return type.levels.includes(l.type); })
                        .every(function (l) { return l.isDisabled; });
                    return __assign(__assign({}, type), { isDisabled: !isAllLevelsWithTypeDisabled });
                }
                return __assign(__assign({}, type), { isDisabled: false });
            });
            return [types, levels];
        };
        _this.filterOptionsByType = function (options, option) {
            // Filter types
            var _a = __read(_this.filterOptionsFirstStep(options[0], option), 2), types = _a[0], checkedTypes = _a[1];
            // Filter levels
            var levels = options[1].map(function (level) {
                if (!checkedTypes.some(function (type) { return type.levels.includes(level.type); })) {
                    var isAllTypesWithLevelDisabled = types
                        .filter(function (t) { return t.levels.includes(level.type); })
                        .every(function (t) { return t.isDisabled; });
                    return __assign(__assign({}, level), { isDisabled: !isAllTypesWithLevelDisabled });
                }
                return __assign(__assign({}, level), { isDisabled: false });
            });
            return [types, levels];
        };
        _this.handleClick = function () {
            var args = [];
            for (var _i = 0; _i < arguments.length; _i++) {
                args[_i] = arguments[_i];
            }
            var _a = __read(args, 2), type = _a[0], option = _a[1];
            var _b = _this.props, onFilter = _b.onFilter, options = _b.options;
            var updatedOptions = type === 'type'
                ? _this.filterOptionsByType(options, option)
                : _this.filterOptionsByLevel(options, option);
            onFilter(updatedOptions);
        };
        return _this;
    }
    Filter.prototype.componentDidMount = function () {
        this.updateState();
    };
    Filter.prototype.componentDidUpdate = function (prevProps) {
        if (!isEqual(prevProps.options, this.props.options)) {
            this.updateState();
        }
    };
    Filter.prototype.render = function () {
        var options = this.props.options;
        var _a = this.state, hasTypeOption = _a.hasTypeOption, hasLevelOption = _a.hasLevelOption, checkedQuantity = _a.checkedQuantity;
        if (!hasTypeOption && !hasLevelOption) {
            return null;
        }
        return (<Wrapper>
        <DropdownControl menuWidth="240px" blendWithActor button={function (_a) {
            var isOpen = _a.isOpen, getActorProps = _a.getActorProps;
            return (<DropDownButton isOpen={isOpen} getActorProps={getActorProps} checkedQuantity={checkedQuantity}/>);
        }}>
          <Header onCheckAll={this.handleToggleCheckAll} checkedQuantity={checkedQuantity} isAllChecked={false}/>
          {hasTypeOption && (<OptionsGroup type="type" onClick={this.handleClick} options={options[0]}/>)}

          {hasLevelOption && (<OptionsGroup type="level" onClick={this.handleClick} options={options[1]}/>)}
        </DropdownControl>
      </Wrapper>);
    };
    return Filter;
}(React.Component));
export default Filter;
var Wrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  position: relative;\n  display: flex;\n"], ["\n  position: relative;\n  display: flex;\n"])));
var templateObject_1;
//# sourceMappingURL=filter.jsx.map