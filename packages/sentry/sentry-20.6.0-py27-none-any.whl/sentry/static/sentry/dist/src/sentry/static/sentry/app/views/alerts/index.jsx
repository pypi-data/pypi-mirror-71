import { __extends } from "tslib";
import React from 'react';
import { t } from 'app/locale';
import { PageContent } from 'app/styles/organization';
import SentryTypes from 'app/sentryTypes';
import Feature from 'app/components/acl/feature';
import Alert from 'app/components/alert';
import withOrganization from 'app/utils/withOrganization';
var IncidentsContainer = /** @class */ (function (_super) {
    __extends(IncidentsContainer, _super);
    function IncidentsContainer() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    IncidentsContainer.prototype.renderNoAccess = function () {
        return (<PageContent>
        <Alert type="warning">{t("You don't have access to this feature")}</Alert>
      </PageContent>);
    };
    IncidentsContainer.prototype.render = function () {
        var _a = this.props, organization = _a.organization, children = _a.children;
        return (<Feature features={['organizations:incidents']} organization={organization} renderDisabled={this.renderNoAccess}>
        {children}
      </Feature>);
    };
    IncidentsContainer.propTypes = {
        organization: SentryTypes.Organization.isRequired,
    };
    return IncidentsContainer;
}(React.Component));
export default withOrganization(IncidentsContainer);
//# sourceMappingURL=index.jsx.map