import { __assign, __extends, __rest } from "tslib";
import PropTypes from 'prop-types';
import React from 'react';
import SentryTypes from 'app/sentryTypes';
import OrganizationAvatar from 'app/components/avatar/organizationAvatar';
import ProjectAvatar from 'app/components/avatar/projectAvatar';
import TeamAvatar from 'app/components/avatar/teamAvatar';
import UserAvatar from 'app/components/avatar/userAvatar';
var BasicModelShape = PropTypes.shape({ slug: PropTypes.string });
var Avatar = /** @class */ (function (_super) {
    __extends(Avatar, _super);
    function Avatar() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    Avatar.prototype.render = function () {
        var _a = this.props, user = _a.user, team = _a.team, project = _a.project, organization = _a.organization, props = __rest(_a, ["user", "team", "project", "organization"]);
        if (user) {
            return <UserAvatar user={user} {...props}/>;
        }
        if (team) {
            return <TeamAvatar team={team} {...props}/>;
        }
        if (project) {
            return <ProjectAvatar project={project} {...props}/>;
        }
        return <OrganizationAvatar organization={organization} {...props}/>;
    };
    Avatar.propTypes = __assign({ team: PropTypes.oneOfType([BasicModelShape, SentryTypes.Team]), organization: PropTypes.oneOfType([BasicModelShape, SentryTypes.Organization]), project: PropTypes.oneOfType([BasicModelShape, SentryTypes.Project]) }, UserAvatar.propTypes);
    Avatar.defaultProps = {
        hasTooltip: false,
    };
    return Avatar;
}(React.Component));
export default React.forwardRef(function (props, ref) { return (<Avatar forwardedRef={ref} {...props}/>); });
//# sourceMappingURL=index.jsx.map