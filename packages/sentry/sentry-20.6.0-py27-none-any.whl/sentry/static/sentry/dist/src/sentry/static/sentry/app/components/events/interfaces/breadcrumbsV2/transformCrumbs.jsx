import { __assign } from "tslib";
import convertCrumbType from './convertCrumbType';
import getCrumbDetails from './getCrumbDetails';
var transformCrumbs = function (breadcrumbs) {
    return breadcrumbs.map(function (breadcrumb, index) {
        var convertedCrumbType = convertCrumbType(breadcrumb);
        var crumbDetails = getCrumbDetails(convertedCrumbType.type);
        return __assign(__assign({ id: index }, convertedCrumbType), crumbDetails);
    });
};
export default transformCrumbs;
//# sourceMappingURL=transformCrumbs.jsx.map