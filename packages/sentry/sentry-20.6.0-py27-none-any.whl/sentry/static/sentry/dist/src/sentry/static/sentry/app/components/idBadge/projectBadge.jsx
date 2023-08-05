import { __assign, __rest } from "tslib";
import React from 'react';
import PropTypes from 'prop-types';
import BaseBadge from 'app/components/idBadge/baseBadge';
import BadgeDisplayName from 'app/components/idBadge/badgeDisplayName';
function ProjectBadge(_a) {
    var _b = _a.hideOverflow, hideOverflow = _b === void 0 ? true : _b, _c = _a.hideAvatar, hideAvatar = _c === void 0 ? false : _c, project = _a.project, props = __rest(_a, ["hideOverflow", "hideAvatar", "project"]);
    return (<BaseBadge displayName={<BadgeDisplayName hideOverflow={hideOverflow}>{project.slug}</BadgeDisplayName>} project={project} hideAvatar={hideAvatar} {...props}/>);
}
ProjectBadge.propTypes = __assign(__assign({}, BaseBadge.propTypes), { project: BaseBadge.propTypes.project.isRequired, avatarSize: PropTypes.number, 
    /**
     * If true, will use default max-width, or specify one as a string
     */
    hideOverflow: PropTypes.oneOfType([PropTypes.bool, PropTypes.string]), hideAvatar: PropTypes.bool });
export default ProjectBadge;
//# sourceMappingURL=projectBadge.jsx.map