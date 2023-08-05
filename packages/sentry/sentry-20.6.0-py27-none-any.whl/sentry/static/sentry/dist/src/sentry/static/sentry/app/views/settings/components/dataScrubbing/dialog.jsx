import { __assign, __extends, __makeTemplateObject, __read, __spread } from "tslib";
import React from 'react';
import Modal from 'react-bootstrap/lib/Modal';
import styled from '@emotion/styled';
import omit from 'lodash/omit';
import isEqual from 'lodash/isEqual';
import Button from 'app/components/button';
import ButtonBar from 'app/components/buttonBar';
import { t } from 'app/locale';
import { defined } from 'app/utils';
import Form from './form/form';
import { RuleType, MethodType, } from './types';
var DEFAULT_RULE_SOURCE_VALUE = '';
var Dialog = /** @class */ (function (_super) {
    __extends(Dialog, _super);
    function Dialog() {
        var _a;
        var _this = _super.apply(this, __spread(arguments)) || this;
        _this.state = {
            rule: {
                id: -1,
                type: RuleType.CREDITCARD,
                method: MethodType.MASK,
                source: DEFAULT_RULE_SOURCE_VALUE,
            },
            isNewRule: defined((_a = _this.props.rule) === null || _a === void 0 ? void 0 : _a.id),
            isFormValid: false,
            errors: {},
        };
        _this.loadRule = function () {
            var rule = _this.props.rule;
            if (!rule) {
                return;
            }
            _this.setState({ rule: rule });
        };
        _this.updateErrors = function () {
            _this.setState(function (prevState) { return ({ errors: __assign(__assign({}, prevState.errors), _this.props.errors) }); });
        };
        _this.clearError = function (error) {
            _this.setState(function (prevState) { return ({ errors: omit(prevState.errors, error) }); });
        };
        _this.handleChange = function (stateProperty, value) {
            var _a;
            var rule = __assign(__assign({}, _this.state.rule), (_a = {}, _a[stateProperty] = value, _a));
            if (rule.type === RuleType.PATTERN) {
                rule.pattern = (rule === null || rule === void 0 ? void 0 : rule.pattern) || '';
            }
            if (rule.type !== RuleType.PATTERN) {
                // TODO(Priscila): Improve this logic
                // @ts-ignore
                rule === null || rule === void 0 ? true : delete rule.pattern;
                _this.clearError('pattern');
            }
            if (stateProperty === 'pattern' || stateProperty === 'source') {
                _this.clearError(stateProperty);
            }
            _this.setState({ rule: rule });
        };
        _this.handleValidation = function (field) { return function () {
            // @ts-ignore
            var isFieldValueEmpty = !_this.state.rule[field];
            var fieldErrorAlreadyExist = _this.state.errors[field];
            if (isFieldValueEmpty && fieldErrorAlreadyExist) {
                return;
            }
            if (isFieldValueEmpty && !fieldErrorAlreadyExist) {
                _this.setState(function (prevState) {
                    var _a;
                    return ({
                        errors: __assign(__assign({}, prevState.errors), (_a = {}, _a[field] = t('Field Required'), _a)),
                    });
                });
                return;
            }
            if (!isFieldValueEmpty && fieldErrorAlreadyExist) {
                _this.clearError(field);
            }
        }; };
        _this.handleValidateForm = function () {
            var rule = _this.state.rule;
            var ruleKeys = Object.keys(omit(rule, 'id'));
            var isFormValid = !ruleKeys.find(function (ruleKey) { return !rule[ruleKey]; });
            _this.setState({ isFormValid: isFormValid });
        };
        _this.handleSave = function () {
            var rule = _this.state.rule;
            var onSaveRule = _this.props.onSaveRule;
            onSaveRule(rule);
        };
        return _this;
    }
    Dialog.prototype.componentDidMount = function () {
        this.loadRule();
    };
    Dialog.prototype.componentDidUpdate = function (prevProps, prevState) {
        if (!isEqual(prevProps.errors, this.props.errors)) {
            this.updateErrors();
        }
        if (this.props.rule && this.props.rule.id !== prevState.rule.id) {
            return;
        }
        if (!isEqual(prevState.rule, this.state.rule)) {
            this.handleValidateForm();
        }
    };
    Dialog.prototype.render = function () {
        var _a = this.props, onClose = _a.onClose, sourceSuggestions = _a.sourceSuggestions, onUpdateEventId = _a.onUpdateEventId, eventId = _a.eventId;
        var _b = this.state, rule = _b.rule, isFormValid = _b.isFormValid, errors = _b.errors, isNewRule = _b.isNewRule;
        return (<StyledModal show animation={false} onHide={onClose}>
        <Modal.Header closeButton>
          {isNewRule
            ? t('Add an advanced data scrubbing rule')
            : t('Edit an advanced data scrubbing rule')}
        </Modal.Header>
        <Modal.Body>
          <Form onChange={this.handleChange} onValidate={this.handleValidation} sourceSuggestions={sourceSuggestions} rule={rule} onUpdateEventId={onUpdateEventId} eventId={eventId} errors={errors}/>
        </Modal.Body>
        <Modal.Footer>
          <ButtonBar gap={1.5}>
            <Button onClick={onClose}>{t('Cancel')}</Button>
            <Button disabled={!isFormValid} onClick={this.handleSave} priority="primary">
              {t('Save Rule')}
            </Button>
          </ButtonBar>
        </Modal.Footer>
      </StyledModal>);
    };
    return Dialog;
}(React.Component));
export default Dialog;
var StyledModal = styled(Modal)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  .modal-dialog {\n    position: absolute;\n    top: 50%;\n    left: 50%;\n    transform: translate(-50%, -50%) !important;\n    margin: 0;\n    @media (max-width: ", ") {\n      width: 100%;\n    }\n  }\n  .close {\n    outline: none;\n  }\n"], ["\n  .modal-dialog {\n    position: absolute;\n    top: 50%;\n    left: 50%;\n    transform: translate(-50%, -50%) !important;\n    margin: 0;\n    @media (max-width: ", ") {\n      width: 100%;\n    }\n  }\n  .close {\n    outline: none;\n  }\n"])), function (p) { return p.theme.breakpoints[0]; });
var templateObject_1;
//# sourceMappingURL=dialog.jsx.map