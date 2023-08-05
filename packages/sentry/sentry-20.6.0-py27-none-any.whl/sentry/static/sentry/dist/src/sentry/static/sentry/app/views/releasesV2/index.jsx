import { __extends } from "tslib";
import React from 'react';
import { t } from 'app/locale';
import { PageContent } from 'app/styles/organization';
import SentryTypes from 'app/sentryTypes';
import Feature from 'app/components/acl/feature';
import Alert from 'app/components/alert';
import withOrganization from 'app/utils/withOrganization';
var ReleasesContainer = /** @class */ (function (_super) {
    __extends(ReleasesContainer, _super);
    function ReleasesContainer() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    ReleasesContainer.prototype.renderNoAccess = function () {
        return (<PageContent>
        <Alert type="warning">{t("You don't have access to this feature")}</Alert>
      </PageContent>);
    };
    ReleasesContainer.prototype.render = function () {
        var _a = this.props, organization = _a.organization, children = _a.children;
        return (<Feature features={['releases-v2']} organization={organization} renderDisabled={this.renderNoAccess}>
        {children}
      </Feature>);
    };
    ReleasesContainer.propTypes = {
        organization: SentryTypes.Organization.isRequired,
    };
    return ReleasesContainer;
}(React.Component));
export default withOrganization(ReleasesContainer);
//# sourceMappingURL=index.jsx.map