import { __assign, __read } from "tslib";
import { BreadcrumbType } from './types';
function convertBreadcrumbType(breadcrumb) {
    if (breadcrumb.level) {
        if (breadcrumb.level === 'warning') {
            return __assign(__assign({}, breadcrumb), { type: BreadcrumbType.WARNING });
        }
        if (breadcrumb.level === 'error') {
            return __assign(__assign({}, breadcrumb), { type: BreadcrumbType.ERROR });
        }
    }
    // special case for 'ui.' and `sentry.` category breadcrumbs
    // TODO: find a better way to customize UI around non-schema data
    if ((!breadcrumb.type || breadcrumb.type === 'default') && breadcrumb.category) {
        var _a = __read(breadcrumb.category.split('.'), 2), category = _a[0], subcategory = _a[1];
        if (category === 'ui') {
            return __assign(__assign({}, breadcrumb), { type: BreadcrumbType.UI });
        }
        if (category === 'console' || category === 'navigation') {
            return __assign(__assign({}, breadcrumb), { type: BreadcrumbType.DEBUG });
        }
        if (category === 'sentry' &&
            (subcategory === 'transaction' || subcategory === 'event')) {
            return __assign(__assign({}, breadcrumb), { type: BreadcrumbType.ERROR });
        }
    }
    return breadcrumb;
}
export default convertBreadcrumbType;
//# sourceMappingURL=convertBreadcrumbType.jsx.map