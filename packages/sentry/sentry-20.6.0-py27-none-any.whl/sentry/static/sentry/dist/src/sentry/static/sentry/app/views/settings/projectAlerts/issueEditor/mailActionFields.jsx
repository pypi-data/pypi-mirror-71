import { __assign, __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import SelectMembers from 'app/components/selectMembers';
import SelectControl from 'app/components/forms/selectControl';
import { MailActionTargetType } from 'app/types/alerts';
import { PanelItem } from 'app/components/panels';
import space from 'app/styles/space';
var MailActionFields = /** @class */ (function (_super) {
    __extends(MailActionFields, _super);
    function MailActionFields() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleChange = function (attribute, newValue) {
            var _a;
            var _b = _this.props, onChange = _b.onChange, action = _b.action;
            if (newValue === action[attribute]) {
                return;
            }
            var newAction = __assign(__assign({}, action), (_a = {}, _a[attribute] = newValue, _a));
            /**
             * TargetIdentifiers between the targetTypes are not unique, and may wrongly map to something that has not been
             * selected. E.g. A member and project can both have the `targetIdentifier`, `'2'`. Hence we clear the identifier.
             **/
            if (attribute === 'targetType') {
                newAction.targetIdentifier = '';
            }
            onChange(newAction);
        };
        _this.handleChangeActorType = function (optionRecord) {
            _this.handleChange('targetType', optionRecord.value);
        };
        _this.handleChangeActorId = function (optionRecord) {
            _this.handleChange('targetIdentifier', optionRecord.value);
        };
        return _this;
    }
    MailActionFields.prototype.render = function () {
        var _a = this.props, disabled = _a.disabled, loading = _a.loading, project = _a.project, organization = _a.organization, action = _a.action;
        var isIssueOwners = action.targetType === MailActionTargetType.IssueOwners;
        var isTeam = action.targetType === MailActionTargetType.Team;
        var selectControlStyles = {
            control: function (provided) { return (__assign(__assign({}, provided), { minHeight: '28px', height: '28px' })); },
        };
        return (<PanelItemGrid>
        <SelectControl isClearable={false} isDisabled={disabled || loading} value={action.targetType} styles={selectControlStyles} options={[
            { value: MailActionTargetType.IssueOwners, label: 'Issue Owners' },
            { value: MailActionTargetType.Team, label: 'Team' },
            { value: MailActionTargetType.Member, label: 'Member' },
        ]} onChange={this.handleChangeActorType}/>
        {!isIssueOwners ? (<SelectMembers disabled={disabled} key={isTeam ? MailActionTargetType.Team : MailActionTargetType.Member} showTeam={isTeam} project={project} organization={organization} 
        // The value from the endpoint is of type `number`, `SelectMembers` require value to be of type `string`
        value={"" + action.targetIdentifier} styles={selectControlStyles} onChange={this.handleChangeActorId}/>) : (<span />)}
      </PanelItemGrid>);
    };
    return MailActionFields;
}(React.Component));
var PanelItemGrid = styled(PanelItem)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 200px 200px;\n  padding: 0;\n  align-items: center;\n  grid-gap: ", ";\n"], ["\n  display: grid;\n  grid-template-columns: 200px 200px;\n  padding: 0;\n  align-items: center;\n  grid-gap: ", ";\n"])), space(2));
export default MailActionFields;
var templateObject_1;
//# sourceMappingURL=mailActionFields.jsx.map