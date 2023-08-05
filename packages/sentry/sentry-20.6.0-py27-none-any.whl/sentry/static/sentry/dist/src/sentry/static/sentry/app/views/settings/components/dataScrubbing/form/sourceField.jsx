import { __extends, __makeTemplateObject, __read, __spread } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import space from 'app/styles/space';
import { t } from 'app/locale';
import TextField from 'app/components/forms/textField';
import TextOverflow from 'app/components/textOverflow';
import { defined } from 'app/utils';
import { unarySuggestions, binarySuggestions } from '../utils';
import SourceSuggestionExamples from './sourceSuggestionExamples';
import { SourceSuggestionType } from '../types';
var SourceField = /** @class */ (function (_super) {
    __extends(SourceField, _super);
    function SourceField() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            suggestions: [],
            fieldValues: [],
            activeSuggestion: 0,
            showSuggestions: false,
            hideCaret: false,
        };
        _this.selectorField = React.createRef();
        _this.suggestionList = React.createRef();
        _this.getFilteredSuggestions = function (value, type) {
            var valuesToBeFiltered = [];
            switch (type) {
                case SourceSuggestionType.BINARY: {
                    valuesToBeFiltered = binarySuggestions;
                    break;
                }
                case SourceSuggestionType.VALUE: {
                    valuesToBeFiltered = _this.getValueSuggestions();
                    break;
                }
                case SourceSuggestionType.UNARY: {
                    valuesToBeFiltered = unarySuggestions;
                    break;
                }
                default: {
                    valuesToBeFiltered = __spread(_this.getValueSuggestions(), unarySuggestions);
                }
            }
            var filteredSuggestions = valuesToBeFiltered.filter(function (s) { return s.value.toLowerCase().indexOf(value.toLowerCase()) > -1; });
            return filteredSuggestions;
        };
        _this.getNewSuggestions = function (fieldValues) {
            var lastFieldValue = fieldValues[fieldValues.length - 1];
            var penultimateFieldValue = fieldValues[fieldValues.length - 2];
            if (Array.isArray(lastFieldValue)) {
                // recursion
                return _this.getNewSuggestions(lastFieldValue);
            }
            if (Array.isArray(penultimateFieldValue)) {
                if ((lastFieldValue === null || lastFieldValue === void 0 ? void 0 : lastFieldValue.type) === 'binary') {
                    // returns filtered values
                    return _this.getFilteredSuggestions(lastFieldValue === null || lastFieldValue === void 0 ? void 0 : lastFieldValue.value, SourceSuggestionType.VALUE);
                }
                // returns all binaries without any filter
                return _this.getFilteredSuggestions('', SourceSuggestionType.BINARY);
            }
            if ((lastFieldValue === null || lastFieldValue === void 0 ? void 0 : lastFieldValue.type) === 'value' && (penultimateFieldValue === null || penultimateFieldValue === void 0 ? void 0 : penultimateFieldValue.type) === 'unary') {
                // returns filtered values
                return _this.getFilteredSuggestions(lastFieldValue === null || lastFieldValue === void 0 ? void 0 : lastFieldValue.value, SourceSuggestionType.VALUE);
            }
            if ((lastFieldValue === null || lastFieldValue === void 0 ? void 0 : lastFieldValue.type) === 'unary') {
                // returns all values without any filter
                return _this.getFilteredSuggestions('', SourceSuggestionType.VALUE);
            }
            if ((lastFieldValue === null || lastFieldValue === void 0 ? void 0 : lastFieldValue.type) === 'string' && (penultimateFieldValue === null || penultimateFieldValue === void 0 ? void 0 : penultimateFieldValue.type) === 'value') {
                // returns all binaries without any filter
                return _this.getFilteredSuggestions('', SourceSuggestionType.BINARY);
            }
            if ((lastFieldValue === null || lastFieldValue === void 0 ? void 0 : lastFieldValue.type) === 'string' &&
                (penultimateFieldValue === null || penultimateFieldValue === void 0 ? void 0 : penultimateFieldValue.type) === 'string' &&
                !(penultimateFieldValue === null || penultimateFieldValue === void 0 ? void 0 : penultimateFieldValue.value)) {
                // returns all values without any filter
                return _this.getFilteredSuggestions('', SourceSuggestionType.STRING);
            }
            if (((penultimateFieldValue === null || penultimateFieldValue === void 0 ? void 0 : penultimateFieldValue.type) === 'string' && !(lastFieldValue === null || lastFieldValue === void 0 ? void 0 : lastFieldValue.value)) ||
                ((penultimateFieldValue === null || penultimateFieldValue === void 0 ? void 0 : penultimateFieldValue.type) === 'value' && !(lastFieldValue === null || lastFieldValue === void 0 ? void 0 : lastFieldValue.value)) ||
                (lastFieldValue === null || lastFieldValue === void 0 ? void 0 : lastFieldValue.type) === 'binary') {
                // returns filtered binaries
                return _this.getFilteredSuggestions(lastFieldValue === null || lastFieldValue === void 0 ? void 0 : lastFieldValue.value, SourceSuggestionType.BINARY);
            }
            return _this.getFilteredSuggestions(lastFieldValue === null || lastFieldValue === void 0 ? void 0 : lastFieldValue.value, lastFieldValue === null || lastFieldValue === void 0 ? void 0 : lastFieldValue.type);
        };
        _this.loadFieldValues = function (newValue) {
            var fieldValues = [];
            var splittedValue = newValue.split(' ');
            var _loop_1 = function (splittedValueIndex) {
                var value = splittedValue[splittedValueIndex];
                var lastFieldValue = fieldValues[fieldValues.length - 1];
                if (lastFieldValue &&
                    !Array.isArray(lastFieldValue) &&
                    !lastFieldValue.value &&
                    !value) {
                    return "continue";
                }
                if (value.includes('!') && !!value.split('!')[1]) {
                    var valueAfterUnaryOperator_1 = value.split('!')[1];
                    var selector_1 = _this.getAllSuggestions().find(function (s) { return s.value === valueAfterUnaryOperator_1; });
                    if (!selector_1) {
                        fieldValues.push([
                            unarySuggestions[0],
                            { type: SourceSuggestionType.STRING, value: valueAfterUnaryOperator_1 },
                        ]);
                        return "continue";
                    }
                    fieldValues.push([unarySuggestions[0], selector_1]);
                    return "continue";
                }
                var selector = _this.getAllSuggestions().find(function (s) { return s.value === value; });
                if (selector) {
                    fieldValues.push(selector);
                    return "continue";
                }
                fieldValues.push({ type: SourceSuggestionType.STRING, value: value });
            };
            for (var splittedValueIndex in splittedValue) {
                _loop_1(splittedValueIndex);
            }
            var filteredSuggestions = _this.getNewSuggestions(fieldValues);
            _this.setState({
                fieldValues: fieldValues,
                activeSuggestion: 0,
                suggestions: filteredSuggestions,
            });
        };
        _this.scrollToSuggestion = function () {
            var _a, _b;
            var _c = _this.state, activeSuggestion = _c.activeSuggestion, hideCaret = _c.hideCaret;
            (_b = (_a = _this.suggestionList) === null || _a === void 0 ? void 0 : _a.current) === null || _b === void 0 ? void 0 : _b.children[activeSuggestion].scrollIntoView({
                behavior: 'smooth',
                block: 'nearest',
                inline: 'start',
            });
            if (!hideCaret) {
                _this.setState({
                    hideCaret: true,
                });
            }
        };
        _this.handleChange = function (newValue) {
            _this.loadFieldValues(newValue);
            _this.props.onChange(newValue);
        };
        _this.handleClickOutside = function () {
            _this.setState({
                showSuggestions: false,
                hideCaret: false,
            });
        };
        _this.handleChangeParentValue = function () {
            var onChange = _this.props.onChange;
            var fieldValues = _this.state.fieldValues;
            var newValue = [];
            for (var index in fieldValues) {
                var fieldValue = fieldValues[index];
                if (Array.isArray(fieldValue)) {
                    newValue.push("" + fieldValue[0].value + fieldValue[1].value);
                    continue;
                }
                newValue.push(fieldValue.value);
            }
            onChange(newValue.join(' '));
        };
        _this.getNewFieldValues = function (suggestion) {
            var fieldValues = __spread(_this.state.fieldValues);
            var lastFieldValue = fieldValues[fieldValues.length - 1];
            if (!defined(lastFieldValue)) {
                return [suggestion];
            }
            if (Array.isArray(lastFieldValue)) {
                fieldValues[fieldValues.length - 1] = [lastFieldValue[0], suggestion];
                return fieldValues;
            }
            if ((lastFieldValue === null || lastFieldValue === void 0 ? void 0 : lastFieldValue.type) === 'unary') {
                fieldValues[fieldValues.length - 1] = [lastFieldValue, suggestion];
            }
            if ((lastFieldValue === null || lastFieldValue === void 0 ? void 0 : lastFieldValue.type) === 'string') {
                fieldValues[fieldValues.length - 1] = suggestion;
            }
            return fieldValues;
        };
        _this.handleClickSuggestionItem = function (suggestion) { return function () {
            var fieldValues = _this.getNewFieldValues(suggestion);
            _this.setState({
                fieldValues: fieldValues,
                activeSuggestion: 0,
                showSuggestions: false,
                hideCaret: false,
            }, function () {
                _this.handleChangeParentValue();
            });
        }; };
        _this.handleKeyDown = function (event) {
            event.persist();
            var keyCode = event.keyCode;
            var _a = _this.state, activeSuggestion = _a.activeSuggestion, suggestions = _a.suggestions;
            if (keyCode === 8 || keyCode === 32) {
                _this.toggleSuggestions(true);
                return;
            }
            if (keyCode === 13) {
                _this.handleClickSuggestionItem(suggestions[activeSuggestion])();
                return;
            }
            if (keyCode === 38) {
                if (activeSuggestion === 0) {
                    return;
                }
                _this.setState({ activeSuggestion: activeSuggestion - 1 }, function () {
                    _this.scrollToSuggestion();
                });
                return;
            }
            if (keyCode === 40) {
                if (activeSuggestion === suggestions.length - 1) {
                    return;
                }
                _this.setState({ activeSuggestion: activeSuggestion + 1 }, function () {
                    _this.scrollToSuggestion();
                });
                return;
            }
        };
        _this.toggleSuggestions = function (showSuggestions) {
            _this.setState({ showSuggestions: showSuggestions });
        };
        _this.handleFocus = function () {
            _this.toggleSuggestions(true);
        };
        _this.checkPossiblyRegExMatchExpression = function (value) {
            var isRegExMatchesSelected = _this.props.isRegExMatchesSelected;
            var help = _this.state.help;
            if (isRegExMatchesSelected) {
                if (help) {
                    _this.setState({ help: '' });
                }
                return;
            }
            var isPossiblyARegularExpression = RegExp('^/.*/g?$').test(value);
            if (help) {
                if (!isPossiblyARegularExpression) {
                    _this.setState({
                        help: '',
                    });
                }
                return;
            }
            if (isPossiblyARegularExpression) {
                _this.setState({
                    help: t("You might want to change Data Type's value to 'Regex matches'"),
                });
            }
        };
        return _this;
    }
    SourceField.prototype.componentDidMount = function () {
        this.loadFieldValues(this.props.value);
        this.toggleSuggestions(false);
    };
    SourceField.prototype.componentDidUpdate = function (prevProps) {
        if (prevProps.suggestions !== this.props.suggestions) {
            this.loadFieldValues(this.props.value);
            this.toggleSuggestions(false);
        }
        if (prevProps.isRegExMatchesSelected !== this.props.isRegExMatchesSelected ||
            prevProps.value !== this.props.value) {
            this.checkPossiblyRegExMatchExpression(this.props.value);
        }
    };
    SourceField.prototype.getAllSuggestions = function () {
        return __spread(this.getValueSuggestions(), unarySuggestions, binarySuggestions);
    };
    SourceField.prototype.getValueSuggestions = function () {
        return this.props.suggestions || [];
    };
    SourceField.prototype.render = function () {
        var _this = this;
        var _a = this.props, error = _a.error, value = _a.value, onBlur = _a.onBlur;
        var _b = this.state, showSuggestions = _b.showSuggestions, suggestions = _b.suggestions, activeSuggestion = _b.activeSuggestion, hideCaret = _b.hideCaret, help = _b.help;
        return (<Wrapper ref={this.selectorField} hideCaret={hideCaret}>
        <StyledTextField name="source" placeholder={t('Enter a custom attribute, variable or header name')} onChange={this.handleChange} autoComplete="off" value={value} onKeyDown={this.handleKeyDown} error={error} help={error ? undefined : help} onBlur={onBlur} onFocus={this.handleFocus}/>
        {showSuggestions && suggestions.length > 0 && (<React.Fragment>
            <Suggestions ref={this.suggestionList} data-test-id="source">
              {suggestions.slice(0, 50).map(function (suggestion, index) { return (<Suggestion key={suggestion.value} onClick={_this.handleClickSuggestionItem(suggestion)} active={index === activeSuggestion} tabIndex={-1}>
                  <TextOverflow>{suggestion.value}</TextOverflow>
                  {suggestion.description && (<SuggestionDescription>
                      (<TextOverflow>{suggestion.description}</TextOverflow>)
                    </SuggestionDescription>)}
                  {suggestion.examples && suggestion.examples.length > 0 && (<SourceSuggestionExamples examples={suggestion.examples} sourceName={suggestion.value}/>)}
                </Suggestion>); })}
            </Suggestions>
            <SuggestionsOverlay onClick={this.handleClickOutside}/>
          </React.Fragment>)}
      </Wrapper>);
    };
    return SourceField;
}(React.Component));
export default SourceField;
var Wrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  position: relative;\n  width: 100%;\n  ", "\n"], ["\n  position: relative;\n  width: 100%;\n  ", "\n"])), function (p) { return p.hideCaret && "caret-color: transparent;"; });
var StyledTextField = styled(TextField)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  width: 100%;\n  height: 40px;\n  input {\n    height: 40px;\n  }\n\n  z-index: 1002;\n  :focus {\n    outline: none;\n  }\n"], ["\n  width: 100%;\n  height: 40px;\n  input {\n    height: 40px;\n  }\n\n  z-index: 1002;\n  :focus {\n    outline: none;\n  }\n"])));
var Suggestions = styled('ul')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  position: absolute;\n  width: 100%;\n  padding-left: 0;\n  list-style: none;\n  margin-bottom: 0;\n  box-shadow: 0 2px 0 rgba(37, 11, 54, 0.04);\n  border: 1px solid ", ";\n  border-radius: 0 0 ", " ", ";\n  background: ", ";\n  top: 35px;\n  right: 0;\n  z-index: 1002;\n  overflow: hidden;\n  max-height: 200px;\n  overflow-y: auto;\n"], ["\n  position: absolute;\n  width: 100%;\n  padding-left: 0;\n  list-style: none;\n  margin-bottom: 0;\n  box-shadow: 0 2px 0 rgba(37, 11, 54, 0.04);\n  border: 1px solid ", ";\n  border-radius: 0 0 ", " ", ";\n  background: ", ";\n  top: 35px;\n  right: 0;\n  z-index: 1002;\n  overflow: hidden;\n  max-height: 200px;\n  overflow-y: auto;\n"])), function (p) { return p.theme.borderDark; }, space(0.5), space(0.5), function (p) { return p.theme.white; });
var Suggestion = styled('li')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: auto 1fr max-content;\n  grid-gap: ", ";\n  border-bottom: 1px solid ", ";\n  padding: ", " ", ";\n  font-size: ", ";\n  cursor: pointer;\n  background: ", ";\n  :hover {\n    background: ", ";\n  }\n"], ["\n  display: grid;\n  grid-template-columns: auto 1fr max-content;\n  grid-gap: ", ";\n  border-bottom: 1px solid ", ";\n  padding: ", " ", ";\n  font-size: ", ";\n  cursor: pointer;\n  background: ", ";\n  :hover {\n    background: ", ";\n  }\n"])), space(1), function (p) { return p.theme.borderLight; }, space(1), space(2), function (p) { return p.theme.fontSizeMedium; }, function (p) { return (p.active ? p.theme.gray200 : p.theme.white); }, function (p) { return (p.active ? p.theme.gray200 : p.theme.gray100); });
var SuggestionDescription = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  display: flex;\n  overflow: hidden;\n  color: ", ";\n"], ["\n  display: flex;\n  overflow: hidden;\n  color: ", ";\n"])), function (p) { return p.theme.gray500; });
var SuggestionsOverlay = styled('div')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  position: fixed;\n  top: 0;\n  left: 0;\n  right: 0;\n  bottom: 0;\n  z-index: 1001;\n"], ["\n  position: fixed;\n  top: 0;\n  left: 0;\n  right: 0;\n  bottom: 0;\n  z-index: 1001;\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6;
//# sourceMappingURL=sourceField.jsx.map