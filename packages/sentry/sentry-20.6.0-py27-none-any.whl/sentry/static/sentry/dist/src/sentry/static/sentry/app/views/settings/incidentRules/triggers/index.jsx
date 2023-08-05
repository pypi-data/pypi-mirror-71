import { __assign, __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { Panel, PanelBody, PanelHeader } from 'app/components/panels';
import { removeAtArrayIndex } from 'app/utils/removeAtArrayIndex';
import { replaceAtArrayIndex } from 'app/utils/replaceAtArrayIndex';
import { t } from 'app/locale';
import Button from 'app/components/button';
import { IconDelete } from 'app/icons';
import CircleIndicator from 'app/components/circleIndicator';
import TriggerForm from 'app/views/settings/incidentRules/triggers/form';
import space from 'app/styles/space';
import withProjects from 'app/utils/withProjects';
/**
 * Button to delete a trigger
 */
var DeleteButton = function (_a) {
    var triggerIndex = _a.triggerIndex, onDelete = _a.onDelete, disabled = _a.disabled;
    return (<Button type="button" icon={<IconDelete size="xs"/>} size="xsmall" aria-label={t('Delete Trigger')} onClick={function (e) { return onDelete(triggerIndex, e); }} disabled={disabled}>
    {t('Delete')}
  </Button>);
};
/**
 * A list of forms to add, edit, and delete triggers.
 */
var Triggers = /** @class */ (function (_super) {
    __extends(Triggers, _super);
    function Triggers() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleDeleteTrigger = function (index) {
            var _a = _this.props, triggers = _a.triggers, onChange = _a.onChange;
            var updatedTriggers = removeAtArrayIndex(triggers, index);
            onChange(updatedTriggers);
        };
        _this.handleChangeTrigger = function (triggerIndex, trigger, changeObj) {
            var _a = _this.props, triggers = _a.triggers, onChange = _a.onChange;
            var updatedTriggers = replaceAtArrayIndex(triggers, triggerIndex, trigger);
            // If we have multiple triggers (warning and critical), we need to make sure
            // the triggers have the same threshold direction
            if (triggers.length > 1) {
                var otherIndex = triggerIndex ^ 1;
                var otherTrigger = triggers[otherIndex];
                if (trigger.thresholdType !== otherTrigger.thresholdType) {
                    otherTrigger = __assign(__assign({}, otherTrigger), { thresholdType: trigger.thresholdType });
                }
                updatedTriggers = replaceAtArrayIndex(updatedTriggers, otherIndex, otherTrigger);
            }
            onChange(updatedTriggers, triggerIndex, changeObj);
        };
        return _this;
    }
    Triggers.prototype.render = function () {
        var _this = this;
        var _a = this.props, availableActions = _a.availableActions, currentProject = _a.currentProject, errors = _a.errors, organization = _a.organization, projects = _a.projects, triggers = _a.triggers, disabled = _a.disabled, onAdd = _a.onAdd;
        // Note we only support 2 triggers max
        return (<React.Fragment>
        {triggers.map(function (trigger, index) {
            var isCritical = index === 0;
            var title = isCritical ? t('Critical Trigger') : t('Warning Trigger');
            return (<Panel key={index}>
              <PanelHeader hasButtons={!isCritical}>
                <Title>
                  {isCritical ? <CriticalIndicator /> : <WarningIndicator />}
                  {title}
                </Title>
                {!isCritical && (<DeleteButton disabled={disabled} triggerIndex={index} onDelete={_this.handleDeleteTrigger}/>)}
              </PanelHeader>
              <PanelBody>
                <TriggerForm disabled={disabled} isCritical={isCritical} error={errors && errors.get(index)} availableActions={availableActions} organization={organization} projects={projects} currentProject={currentProject} trigger={trigger} triggerIndex={index} onChange={_this.handleChangeTrigger}/>
              </PanelBody>
            </Panel>);
        })}

        {triggers.length < 2 && (<AddWarningButton disabled={disabled} type="button" size="small" icon={<WarningIndicator size={12}/>} onClick={onAdd}>
            {t('Add Warning Trigger')}
          </AddWarningButton>)}
      </React.Fragment>);
    };
    return Triggers;
}(React.Component));
var AddWarningButton = styled(Button)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space(3));
var Title = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: grid;\n  grid-auto-flow: column;\n  grid-gap: ", ";\n  align-items: center;\n"], ["\n  display: grid;\n  grid-auto-flow: column;\n  grid-gap: ", ";\n  align-items: center;\n"])), space(1));
var CriticalIndicator = styled(CircleIndicator)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  background: ", ";\n"], ["\n  background: ", ";\n"])), function (p) { return p.theme.redLight; });
var WarningIndicator = styled(CircleIndicator)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  background: ", ";\n"], ["\n  background: ", ";\n"])), function (p) { return p.theme.yellowDark; });
export default withProjects(Triggers);
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=index.jsx.map