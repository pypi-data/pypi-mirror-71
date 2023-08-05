import { __extends } from "tslib";
import React from 'react';
import { t } from 'app/locale';
import AsyncView from 'app/views/asyncView';
import EmptyStateWarning from 'app/components/emptyStateWarning';
import ReleaseLanding from 'app/views/releases/list/releaseLanding';
var ReleasePromo = /** @class */ (function (_super) {
    __extends(ReleasePromo, _super);
    function ReleasePromo() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    // if there are no releases in the last 30 days, we want to show releases promo
    ReleasePromo.prototype.getEndpoints = function () {
        var orgSlug = this.props.orgSlug;
        var query = {
            per_page: 1,
            summaryStatsPeriod: '30d',
        };
        return [['releases', "/organizations/" + orgSlug + "/releases/", { query: query }]];
    };
    ReleasePromo.prototype.renderBody = function () {
        if (this.state.releases.length === 0) {
            return <ReleaseLanding />;
        }
        return <EmptyStateWarning small>{t('There are no releases.')}</EmptyStateWarning>;
    };
    return ReleasePromo;
}(AsyncView));
export default ReleasePromo;
//# sourceMappingURL=releasePromo.jsx.map