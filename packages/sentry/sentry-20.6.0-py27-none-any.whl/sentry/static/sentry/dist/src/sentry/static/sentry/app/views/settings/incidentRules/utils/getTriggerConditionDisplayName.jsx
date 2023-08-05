import { t } from 'app/locale';
import { AlertRuleThresholdType } from '../types';
export default function getTriggerConditionDisplayName(trigger) {
    if (trigger.thresholdType === AlertRuleThresholdType.ABOVE) {
        return [
            "> " + trigger.alertThreshold,
            typeof trigger.resolveThreshold !== 'undefined' && trigger.resolveThreshold !== null
                ? t('Auto-resolves when metric falls below %s', trigger.resolveThreshold)
                : null,
        ];
    }
    else {
        return [
            "< " + trigger.alertThreshold,
            typeof trigger.resolveThreshold !== 'undefined' && trigger.resolveThreshold !== null
                ? t('Auto-resolves when metric is above %s', trigger.resolveThreshold)
                : null,
        ];
    }
}
//# sourceMappingURL=getTriggerConditionDisplayName.jsx.map