import { __assign, __extends, __makeTemplateObject, __read, __spread } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import isEqual from 'lodash/isEqual';
import TextField from 'app/components/forms/textField';
import { t } from 'app/locale';
import space from 'app/styles/space';
import FormField from './formField';
import EventIdFieldStatusIcon from './eventIdFieldStatusIcon';
import { EventIdStatus } from '../types';
var EventIdField = /** @class */ (function (_super) {
    __extends(EventIdField, _super);
    function EventIdField() {
        var _a, _b;
        var _this = _super.apply(this, __spread(arguments)) || this;
        _this.state = {
            value: ((_a = _this.props.eventId) === null || _a === void 0 ? void 0 : _a.value) || '',
            status: (_b = _this.props.eventId) === null || _b === void 0 ? void 0 : _b.status,
        };
        _this.loadState = function () {
            _this.setState(__assign({}, _this.props.eventId));
        };
        _this.handleChange = function (value) {
            var eventId = value.replace(/-/g, '').trim();
            if (eventId !== _this.state.value) {
                _this.setState({
                    value: eventId,
                    status: undefined,
                });
            }
        };
        _this.isEventIdValid = function () {
            var value = _this.state.value;
            if (value && value.length !== 32) {
                _this.setState({ status: EventIdStatus.INVALID });
                return false;
            }
            return true;
        };
        _this.handleBlur = function (event) {
            event.preventDefault();
            if (_this.isEventIdValid()) {
                _this.props.onUpdateEventId(_this.state.value);
            }
        };
        _this.handleKeyDown = function (event) {
            var keyCode = event.keyCode;
            if (keyCode === 13 && _this.isEventIdValid()) {
                _this.props.onUpdateEventId(_this.state.value);
            }
        };
        _this.handleClickIconClose = function () {
            _this.setState({
                value: '',
                status: undefined,
            });
        };
        _this.getErrorMessage = function () {
            var status = _this.state.status;
            switch (status) {
                case EventIdStatus.INVALID:
                    return t('This event ID is invalid.');
                case EventIdStatus.ERROR:
                    return t('An error occurred while fetching the suggestions based on this Event ID.');
                case EventIdStatus.NOT_FOUND:
                    return t('The chosen event ID was not found in projects you have access to.');
                default:
                    return undefined;
            }
        };
        return _this;
    }
    EventIdField.prototype.componentDidUpdate = function (prevProps) {
        if (!isEqual(prevProps.eventId, this.props.eventId)) {
            this.loadState();
        }
    };
    EventIdField.prototype.render = function () {
        var disabled = this.props.disabled;
        var _a = this.state, value = _a.value, status = _a.status;
        return (<FormField label={t('Event ID (Optional)')} tooltipInfo={t('Providing an event ID will automatically provide you a list of suggested sources')}>
        <FieldWrapper>
          <StyledTextField name="eventId" disabled={disabled} value={value} placeholder={t('XXXXXXXXXXXXXX')} onChange={this.handleChange} onKeyDown={this.handleKeyDown} onBlur={this.handleBlur} showStatus={status !== EventIdStatus.LOADED} error={this.getErrorMessage()}/>
          <Status>
            <EventIdFieldStatusIcon onClickIconClose={this.handleClickIconClose} status={status}/>
          </Status>
        </FieldWrapper>
      </FormField>);
    };
    return EventIdField;
}(React.Component));
export default EventIdField;
var StyledTextField = styled(TextField)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  flex: 1;\n  font-weight: 400;\n  input {\n    height: 40px;\n    padding-right: ", ";\n  }\n  margin-bottom: 0;\n"], ["\n  flex: 1;\n  font-weight: 400;\n  input {\n    height: 40px;\n    padding-right: ", ";\n  }\n  margin-bottom: 0;\n"])), function (p) { return (p.showStatus ? space(4) : space(1.5)); });
var Status = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  height: 40px;\n  position: absolute;\n  right: ", ";\n  top: 0;\n  display: flex;\n  align-items: center;\n"], ["\n  height: 40px;\n  position: absolute;\n  right: ", ";\n  top: 0;\n  display: flex;\n  align-items: center;\n"])), space(1.5));
var FieldWrapper = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  position: relative;\n  display: flex;\n  align-items: center;\n"], ["\n  position: relative;\n  display: flex;\n  align-items: center;\n"])));
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=eventIdField.jsx.map