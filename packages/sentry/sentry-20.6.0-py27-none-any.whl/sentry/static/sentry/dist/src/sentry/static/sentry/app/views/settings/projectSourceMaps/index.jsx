import { __extends } from "tslib";
import React from 'react';
import { t } from 'app/locale';
import { PageContent } from 'app/styles/organization';
import Feature from 'app/components/acl/feature';
import Alert from 'app/components/alert';
import withOrganization from 'app/utils/withOrganization';
var ProjectSourceMapsContainer = /** @class */ (function (_super) {
    __extends(ProjectSourceMapsContainer, _super);
    function ProjectSourceMapsContainer() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    ProjectSourceMapsContainer.prototype.renderNoAccess = function () {
        return (<PageContent>
        <Alert type="warning">{t("You don't have access to this feature")}</Alert>
      </PageContent>);
    };
    ProjectSourceMapsContainer.prototype.render = function () {
        var _a = this.props, children = _a.children, project = _a.project, organization = _a.organization;
        return (<Feature features={['artifacts-in-settings']} organization={organization} renderDisabled={this.renderNoAccess}>
        {React.isValidElement(children) &&
            React.cloneElement(children, { organization: organization, project: project })}
      </Feature>);
    };
    return ProjectSourceMapsContainer;
}(React.Component));
export default withOrganization(ProjectSourceMapsContainer);
//# sourceMappingURL=index.jsx.map