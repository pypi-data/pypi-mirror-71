var _a;
import { AlertRuleThresholdType, Dataset, } from 'app/views/settings/incidentRules/types';
export var DEFAULT_AGGREGATE = 'count()';
export var DATASET_EVENT_TYPE_FILTERS = (_a = {},
    _a[Dataset.ERRORS] = 'event.type:error',
    _a[Dataset.TRANSACTIONS] = 'event.type:transaction',
    _a);
export function createDefaultTrigger() {
    return {
        label: 'critical',
        alertThreshold: '',
        resolveThreshold: '',
        thresholdType: AlertRuleThresholdType.ABOVE,
        actions: [],
    };
}
export function createDefaultRule() {
    return {
        dataset: Dataset.ERRORS,
        aggregate: DEFAULT_AGGREGATE,
        query: '',
        timeWindow: 1,
        triggers: [createDefaultTrigger()],
        projects: [],
        environment: null,
    };
}
//# sourceMappingURL=constants.jsx.map