import { __assign, __extends, __makeTemplateObject, __read } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { MailActionTargetType, } from 'app/types/alerts';
import Alert from 'app/components/alert';
import Button from 'app/components/button';
import Input from 'app/views/settings/components/forms/controls/input';
import SelectControl from 'app/components/forms/selectControl';
import space from 'app/styles/space';
import { t, tct } from 'app/locale';
import MailActionFields from 'app/views/settings/projectAlerts/issueEditor/mailActionFields';
import ExternalLink from 'app/components/links/externalLink';
import { IconDelete } from 'app/icons';
var RuleNode = /** @class */ (function (_super) {
    __extends(RuleNode, _super);
    function RuleNode() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleDelete = function () {
            var _a = _this.props, index = _a.index, onDelete = _a.onDelete;
            onDelete(index);
        };
        _this.handleMailActionChange = function (action) {
            var _a = _this.props, index = _a.index, onPropertyChange = _a.onPropertyChange;
            onPropertyChange(index, 'targetType', "" + action.targetType);
            onPropertyChange(index, 'targetIdentifier', "" + action.targetIdentifier);
        };
        _this.getChoiceField = function (name, fieldConfig) {
            // Select the first item on this list
            // If it's not yet defined, call onPropertyChange to make sure the value is set on state
            var _a = _this.props, data = _a.data, index = _a.index, onPropertyChange = _a.onPropertyChange;
            var initialVal;
            if (data) {
                if (data[name] === undefined && !!fieldConfig.choices.length) {
                    if (fieldConfig.initial) {
                        initialVal = fieldConfig.initial;
                    }
                    else {
                        initialVal = fieldConfig.choices[0][0];
                    }
                }
                else {
                    initialVal = data[name];
                }
            }
            // Cast `key` to string, this problem pops up because of react-select v3 where
            // `value` requires the `option` object (e.g. {label, object}) - we have
            // helpers in `SelectControl` to filter `choices` to produce the value object
            //
            // However there are integrations that give the form field choices with the value as number, but
            // when the integration configuration gets saved, it gets saved and returned as a string
            var choices = fieldConfig.choices.map(function (_a) {
                var _b = __read(_a, 2), key = _b[0], value = _b[1];
                return ["" + key, value];
            });
            return (<InlineSelectControl isClearable={false} name={name} value={initialVal} styles={{
                control: function (provided) { return (__assign(__assign({}, provided), { minHeight: '28px', height: '28px' })); },
            }} choices={choices} onChange={function (_a) {
                var value = _a.value;
                return onPropertyChange(index, name, value);
            }}/>);
        };
        _this.getTextField = function (name, fieldConfig) {
            var _a;
            var _b = _this.props, data = _b.data, index = _b.index, onPropertyChange = _b.onPropertyChange;
            return (<InlineInput type="text" name={name} value={(_a = (data && data[name])) !== null && _a !== void 0 ? _a : ''} placeholder={"" + fieldConfig.placeholder} onChange={function (e) {
                return onPropertyChange(index, name, e.target.value);
            }}/>);
        };
        _this.getNumberField = function (name, fieldConfig) {
            var _a;
            var _b = _this.props, data = _b.data, index = _b.index, onPropertyChange = _b.onPropertyChange;
            return (<InlineInput type="number" name={name} value={(_a = (data && data[name])) !== null && _a !== void 0 ? _a : ''} placeholder={"" + fieldConfig.placeholder} onChange={function (e) {
                return onPropertyChange(index, name, e.target.value);
            }}/>);
        };
        _this.getMailActionFields = function (_, __) {
            var _a = _this.props, data = _a.data, organization = _a.organization, project = _a.project;
            var isInitialized = (data === null || data === void 0 ? void 0 : data.targetType) !== undefined && ("" + data.targetType).length > 0;
            return (<MailActionFields disabled={false} project={project} organization={organization} loading={!isInitialized} action={data} onChange={_this.handleMailActionChange}/>);
        };
        _this.getField = function (name, fieldConfig) {
            var getFieldTypes = {
                choice: _this.getChoiceField,
                number: _this.getNumberField,
                string: _this.getTextField,
                mailAction: _this.getMailActionFields,
            };
            return getFieldTypes[fieldConfig.type](name, fieldConfig);
        };
        return _this;
    }
    RuleNode.prototype.renderRow = function () {
        var _this = this;
        var _a = this.props, data = _a.data, node = _a.node;
        if (!node) {
            return null;
        }
        var label = node.label, formFields = node.formFields;
        var parts = label.split(/({\w+})/).map(function (part, i) {
            if (!/^{\w+}$/.test(part)) {
                return <Separator key={i}>{part}</Separator>;
            }
            var key = part.slice(1, -1);
            // If matcher is "is set" or "is not set", then we do not want to show the value input
            // because it is not required
            if (key === 'value' && data && (data.match === 'is' || data.match === 'ns')) {
                return null;
            }
            return (<Separator key={key}>
          {formFields && formFields.hasOwnProperty(key)
                ? _this.getField(key, formFields[key])
                : part}
        </Separator>);
        });
        var _b = __read(parts), title = _b[0], inputs = _b.slice(1);
        // We return this so that it can be a grid
        return (<Rule>
        {title}
        {inputs}
      </Rule>);
    };
    RuleNode.prototype.conditionallyRenderHelpfulBanner = function () {
        var _a = this.props, data = _a.data, project = _a.project, organization = _a.organization;
        /**
         * Would prefer to check if data is of `IssueAlertRuleAction` type, however we can't do typechecking at runtime as
         * user defined types are erased through transpilation.
         * Instead, we apply duck typing semantics here.
         * See: https://stackoverflow.com/questions/51528780/typescript-check-typeof-against-custom-type
         */
        if (!(data === null || data === void 0 ? void 0 : data.targetType)) {
            return null;
        }
        switch (data.targetType) {
            case MailActionTargetType.IssueOwners:
                return (<MarginlessAlert thinner type="warning">
            {tct('If there are no matching [issueOwners], ownership is determined by the [ownershipSettings].', {
                    issueOwners: (<ExternalLink href="https://docs.sentry.io/workflow/issue-owners/">
                    {t('issue owners')}
                  </ExternalLink>),
                    ownershipSettings: (<ExternalLink href={"/settings/" + organization.slug + "/projects/" + project.slug + "/ownership/"}>
                    {t('ownership settings')}
                  </ExternalLink>),
                })}
          </MarginlessAlert>);
            case MailActionTargetType.Team:
                return null;
            case MailActionTargetType.Member:
                return (<MarginlessAlert thinner type="warning">
            {tct('Alerts sent directly to a member override their [alertSettings].', {
                    alertSettings: (<ExternalLink href="/settings/account/notifications/">
                  {t('personal project alert settings')}
                </ExternalLink>),
                })}
          </MarginlessAlert>);
            default:
                return null;
        }
    };
    RuleNode.prototype.render = function () {
        var data = this.props.data;
        return (<RuleRowContainer>
        <RuleRow>
          {data && <input type="hidden" name="id" value={data.id}/>}
          {this.renderRow()}
          <DeleteButton label={t('Delete Node')} onClick={this.handleDelete} type="button" size="small" icon={<IconDelete />}/>
        </RuleRow>
        {this.conditionallyRenderHelpfulBanner()}
      </RuleRowContainer>);
    };
    return RuleNode;
}(React.Component));
export default RuleNode;
var InlineInput = styled(Input)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  width: auto;\n  height: 28px;\n"], ["\n  width: auto;\n  height: 28px;\n"])));
var InlineSelectControl = styled(SelectControl)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  width: 180px;\n"], ["\n  width: 180px;\n"])));
var Separator = styled('span')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  margin-right: ", ";\n  padding-top: ", ";\n  padding-bottom: ", ";\n"], ["\n  margin-right: ", ";\n  padding-top: ", ";\n  padding-bottom: ", ";\n"])), space(1), space(0.5), space(0.5));
var RuleRow = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  padding: ", ";\n"], ["\n  display: flex;\n  align-items: center;\n  padding: ", ";\n"])), space(1));
var RuleRowContainer = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  &:nth-child(odd) {\n    background-color: ", ";\n  }\n"], ["\n  &:nth-child(odd) {\n    background-color: ", ";\n  }\n"])), function (p) { return p.theme.gray100; });
var Rule = styled('div')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  flex: 1;\n  flex-wrap: wrap;\n"], ["\n  display: flex;\n  align-items: center;\n  flex: 1;\n  flex-wrap: wrap;\n"])));
var DeleteButton = styled(Button)(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  flex-shrink: 0;\n"], ["\n  flex-shrink: 0;\n"])));
var MarginlessAlert = styled(Alert)(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  margin: 0;\n"], ["\n  margin: 0;\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8;
//# sourceMappingURL=ruleNode.jsx.map