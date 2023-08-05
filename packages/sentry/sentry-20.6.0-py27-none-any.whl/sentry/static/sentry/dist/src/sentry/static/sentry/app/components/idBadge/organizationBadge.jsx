import { __assign, __extends, __rest } from "tslib";
import PropTypes from 'prop-types';
import React from 'react';
import BaseBadge from 'app/components/idBadge/baseBadge';
import BadgeDisplayName from 'app/components/idBadge/badgeDisplayName';
import SentryTypes from 'app/sentryTypes';
var OrganizationBadge = /** @class */ (function (_super) {
    __extends(OrganizationBadge, _super);
    function OrganizationBadge() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    OrganizationBadge.prototype.render = function () {
        var _a = this.props, hideOverflow = _a.hideOverflow, organization = _a.organization, props = __rest(_a, ["hideOverflow", "organization"]);
        return (<BaseBadge displayName={<BadgeDisplayName hideOverflow={hideOverflow}>
            {organization.slug}
          </BadgeDisplayName>} organization={organization} {...props}/>);
    };
    OrganizationBadge.propTypes = __assign(__assign({}, BaseBadge.propTypes), { organization: SentryTypes.Organization.isRequired, avatarSize: PropTypes.number, hideOverflow: PropTypes.oneOfType([PropTypes.bool, PropTypes.string]), hideAvatar: PropTypes.bool });
    OrganizationBadge.defaultProps = {
        avatarSize: 24,
        hideAvatar: false,
        hideOverflow: true,
    };
    return OrganizationBadge;
}(React.Component));
export default OrganizationBadge;
//# sourceMappingURL=organizationBadge.jsx.map