import { __assign } from "tslib";
export function getPerformanceLandingUrl(organization) {
    return "/organizations/" + organization.slug + "/performance/";
}
export function getTransactionDetailsUrl(organization, eventSlug, transaction, query) {
    return {
        pathname: "/organizations/" + organization.slug + "/performance/" + eventSlug + "/",
        query: __assign(__assign({}, query), { transaction: transaction }),
    };
}
//# sourceMappingURL=utils.jsx.map