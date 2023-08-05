import { __extends } from "tslib";
import PropTypes from 'prop-types';
import React from 'react';
import ConfigStore from 'app/stores/configStore';
import withOrganization from 'app/utils/withOrganization';
import SentryTypes from 'app/sentryTypes';
var AttachmentUrl = /** @class */ (function (_super) {
    __extends(AttachmentUrl, _super);
    function AttachmentUrl() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    AttachmentUrl.prototype.hasAttachmentsRole = function () {
        var user = ConfigStore.get('user');
        if (!user) {
            return false;
        }
        if (user.isSuperuser) {
            return true;
        }
        var _a = this.props.organization, availableRoles = _a.availableRoles, attachmentsRole = _a.attachmentsRole, role = _a.role;
        if (!Array.isArray(availableRoles)) {
            return false;
        }
        var roleIds = availableRoles.map(function (r) { return r.id; });
        var requiredIndex = roleIds.indexOf(attachmentsRole);
        var currentIndex = roleIds.indexOf(role || '');
        return currentIndex >= requiredIndex;
    };
    AttachmentUrl.prototype.getDownloadUrl = function () {
        var _a = this.props, attachment = _a.attachment, organization = _a.organization, eventId = _a.eventId, projectId = _a.projectId;
        return "/api/0/projects/" + organization.slug + "/" + projectId + "/events/" + eventId + "/attachments/" + attachment.id + "/";
    };
    AttachmentUrl.prototype.render = function () {
        var children = this.props.children;
        return children(this.hasAttachmentsRole() ? this.getDownloadUrl() : null);
    };
    AttachmentUrl.propTypes = {
        organization: SentryTypes.Organization.isRequired,
        projectId: PropTypes.string.isRequired,
        eventId: PropTypes.string.isRequired,
        attachment: SentryTypes.EventAttachment.isRequired,
        children: PropTypes.func.isRequired,
    };
    return AttachmentUrl;
}(React.PureComponent));
export default withOrganization(AttachmentUrl);
//# sourceMappingURL=attachmentUrl.jsx.map