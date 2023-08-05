import { __makeTemplateObject } from "tslib";
import PropTypes from 'prop-types';
import React from 'react';
import styled from '@emotion/styled';
import { addErrorMessage } from 'app/actionCreators/indicator';
import { defined } from 'app/utils';
import InlineSvg from 'app/components/inlineSvg';
import SentryTypes from 'app/sentryTypes';
import { t } from 'app/locale';
import { update } from 'app/actionCreators/projects';
import withApi from 'app/utils/withApi';
var BookmarkStar = function (_a) {
    var api = _a.api, isBookmarkedProp = _a.isBookmarked, className = _a.className, organization = _a.organization, project = _a.project, onToggle = _a.onToggle;
    var isBookmarked = defined(isBookmarkedProp)
        ? isBookmarkedProp
        : project.isBookmarked;
    var toggleProjectBookmark = function (event) {
        update(api, {
            orgId: organization.slug,
            projectId: project.slug,
            data: { isBookmarked: !isBookmarked },
        }).catch(function () {
            addErrorMessage(t('Unable to toggle bookmark for %s', project.slug));
        });
        //needed to dismiss tooltip
        document.activeElement.blur();
        //prevent dropdowns from closing
        event.stopPropagation();
        if (onToggle) {
            onToggle(!isBookmarked);
        }
    };
    return (<Star isBookmarked={isBookmarked} src="icon-star-small-filled" onClick={toggleProjectBookmark} className={className}/>);
};
BookmarkStar.propTypes = {
    api: PropTypes.any.isRequired,
    /* used to override when under local state */
    isBookmarked: PropTypes.bool,
    className: PropTypes.string,
    organization: SentryTypes.Organization.isRequired,
    project: SentryTypes.Project.isRequired,
    onToggle: PropTypes.func,
};
var Star = styled(InlineSvg)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  color: ", ";\n\n  &:hover {\n    color: ", ";\n  }\n"], ["\n  color: ", ";\n\n  &:hover {\n    color: ", ";\n  }\n"])), function (p) { return (p.isBookmarked ? p.theme.yellowOrange : p.theme.gray400); }, function (p) { return (p.isBookmarked ? p.theme.yellowOrangeLight : p.theme.gray500); });
export default withApi(BookmarkStar);
var templateObject_1;
//# sourceMappingURL=bookmarkStar.jsx.map