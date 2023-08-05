var _a;
import { __assign, __read, __spread } from "tslib";
import { platforms } from 'integration-docs-platforms';
import { t } from 'app/locale';
var otherPlatform = {
    integrations: [
        {
            link: 'https://docs.getsentry.com/hosted/clients/',
            type: 'language',
            id: 'other',
            name: t('Other'),
        },
    ],
    id: 'other',
    name: t('Other'),
};
export default (_a = []).concat.apply(_a, __spread([[]], __spread(platforms, [otherPlatform]).map(function (platform) {
    return platform.integrations.map(function (i) { return (__assign(__assign({}, i), { language: platform.id })); });
})));
//# sourceMappingURL=platforms.jsx.map