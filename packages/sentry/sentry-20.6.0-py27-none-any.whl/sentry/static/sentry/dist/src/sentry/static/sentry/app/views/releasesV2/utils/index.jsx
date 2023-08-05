import { __awaiter, __generator } from "tslib";
import round from 'lodash/round';
import localStorage from 'app/utils/localStorage';
import ConfigStore from 'app/stores/configStore';
import OrganizationStore from 'app/stores/organizationStore';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import { Client } from 'app/api';
import { stringifyQueryObject } from 'app/utils/tokenizeSearch';
var RELEASES_VERSION_KEY = 'releases:version';
export var switchReleasesVersion = function (version, orgId) {
    localStorage.setItem(RELEASES_VERSION_KEY, version);
    var user = ConfigStore.get('user');
    trackAnalyticsEvent({
        eventKey: version === '1' ? 'releases_v2.opt_out' : 'releases_v2.opt_in',
        eventName: version === '1' ? 'ReleasesV2: Go to releases1' : 'ReleasesV2: Go to releases2',
        organization_id: parseInt(orgId, 10),
        user_id: parseInt(user.id, 10),
    });
    location.reload();
};
export var wantsLegacyReleases = function () {
    var version = localStorage.getItem(RELEASES_VERSION_KEY);
    return version === '1';
};
export var decideReleasesVersion = function (hasNewReleases) { return __awaiter(void 0, void 0, void 0, function () {
    var api, organization, currentOrgSlug, fetchedOrg, _a;
    return __generator(this, function (_b) {
        switch (_b.label) {
            case 0:
                api = new Client();
                organization = OrganizationStore.get().organization;
                if (wantsLegacyReleases()) {
                    return [2 /*return*/, hasNewReleases(false)];
                }
                if (organization) {
                    return [2 /*return*/, hasNewReleases(organization.features.includes('releases-v2'))];
                }
                _b.label = 1;
            case 1:
                _b.trys.push([1, 3, , 4]);
                currentOrgSlug = location.pathname.split('/')[2];
                return [4 /*yield*/, api.requestPromise("/organizations/" + currentOrgSlug + "/", {
                        query: { detailed: 0 },
                    })];
            case 2:
                fetchedOrg = _b.sent();
                return [2 /*return*/, hasNewReleases(fetchedOrg.features.includes('releases-v2'))];
            case 3:
                _a = _b.sent();
                return [2 /*return*/, hasNewReleases(false)];
            case 4: return [2 /*return*/];
        }
    });
}); };
export var getCrashFreePercent = function (percent, decimalThreshold, decimalPlaces) {
    if (decimalThreshold === void 0) { decimalThreshold = 95; }
    if (decimalPlaces === void 0) { decimalPlaces = 3; }
    return round(percent, percent > decimalThreshold ? decimalPlaces : 0);
};
export var displayCrashFreePercent = function (percent, decimalThreshold, decimalPlaces) {
    if (decimalThreshold === void 0) { decimalThreshold = 95; }
    if (decimalPlaces === void 0) { decimalPlaces = 3; }
    if (isNaN(percent)) {
        return '\u2015';
    }
    if (percent < 1 && percent > 0) {
        return "<1%";
    }
    var rounded = getCrashFreePercent(percent, decimalThreshold, decimalPlaces);
    return rounded + "%";
};
export var convertAdoptionToProgress = function (percent, numberOfProgressUnits) {
    if (numberOfProgressUnits === void 0) { numberOfProgressUnits = 10; }
    return Math.ceil((percent * numberOfProgressUnits) / 100);
};
export var getReleaseNewIssuesUrl = function (orgSlug, projectId, version) {
    return {
        pathname: "/organizations/" + orgSlug + "/issues/",
        query: {
            project: projectId,
            query: stringifyQueryObject({
                query: [],
                firstRelease: [version],
            }),
        },
    };
};
//# sourceMappingURL=index.jsx.map