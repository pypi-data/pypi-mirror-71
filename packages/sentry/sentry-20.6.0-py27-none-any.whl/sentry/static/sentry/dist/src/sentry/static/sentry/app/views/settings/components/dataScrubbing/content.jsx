import { __extends } from "tslib";
import React from 'react';
import isEqual from 'lodash/isEqual';
import { t } from 'app/locale';
import { defined } from 'app/utils';
import EmptyMessage from 'app/views/settings/components/emptyMessage';
import { IconWarning } from 'app/icons';
import RulesList from './rulesList';
import Dialog from './dialog';
var Content = /** @class */ (function (_super) {
    __extends(Content, _super);
    function Content() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {};
        _this.handleDeleteRule = function (ruleId) { return function () {
            var onDeleteRule = _this.props.onDeleteRule;
            onDeleteRule([ruleId]);
        }; };
        _this.handleShowEditRuleModal = function (ruleId) { return function () {
            _this.setState({ editRule: ruleId });
        }; };
        _this.handleCloseEditRuleModal = function () {
            _this.setState({ editRule: undefined });
        };
        _this.handleSave = function (updatedRule) {
            var onUpdateRule = _this.props.onUpdateRule;
            onUpdateRule(updatedRule);
        };
        return _this;
    }
    Content.prototype.componentDidUpdate = function (prevProps) {
        if (prevProps.rules.length > 0 &&
            !isEqual(prevProps.rules, this.props.rules) &&
            Object.keys(this.props.errors).length === 0) {
            this.handleCloseEditRuleModal();
        }
    };
    Content.prototype.render = function () {
        var editRule = this.state.editRule;
        var _a = this.props, rules = _a.rules, sourceSuggestions = _a.sourceSuggestions, onUpdateEventId = _a.onUpdateEventId, eventId = _a.eventId, disabled = _a.disabled, errors = _a.errors;
        if (rules.length === 0) {
            return (<EmptyMessage icon={<IconWarning size="xl"/>} description={t('You have no data scrubbing rules')}/>);
        }
        return (<React.Fragment>
        <RulesList rules={rules} onDeleteRule={this.handleDeleteRule} onShowEditRuleModal={this.handleShowEditRuleModal} disabled={disabled}/>
        {defined(editRule) && (<Dialog rule={rules[editRule]} sourceSuggestions={sourceSuggestions} onClose={this.handleCloseEditRuleModal} onUpdateEventId={onUpdateEventId} onSaveRule={this.handleSave} eventId={eventId} errors={errors}/>)}
      </React.Fragment>);
    };
    return Content;
}(React.PureComponent));
export default Content;
//# sourceMappingURL=content.jsx.map