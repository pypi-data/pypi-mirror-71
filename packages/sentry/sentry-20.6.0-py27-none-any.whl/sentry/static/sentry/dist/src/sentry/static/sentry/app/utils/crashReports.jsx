import { t, tct } from 'app/locale';
export function formatStoreCrashReports(value) {
    if (value === -1) {
        return t('Unlimited');
    }
    else if (value === 0) {
        return t('Disabled');
    }
    else {
        return tct('[value] per issue', { value: value });
    }
}
function getStoreCrashReportsValues() {
    // generate a range from 0 (disabled) to 20 inclusive
    var values = Array.from(new Array(21), function (_, i) { return i; });
    values.push(-1); // special "Unlimited" at the end
    return values;
}
export var STORE_CRASH_REPORTS_VALUES = getStoreCrashReportsValues();
//# sourceMappingURL=crashReports.jsx.map