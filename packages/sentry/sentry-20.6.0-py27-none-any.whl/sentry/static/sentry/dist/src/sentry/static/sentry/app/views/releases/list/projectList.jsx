import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { tct, t } from 'app/locale';
import ProjectBadge from 'app/components/idBadge/projectBadge';
import space from 'app/styles/space';
import GlobalSelectionLink from 'app/components/globalSelectionLink';
import Hovercard, { Body as HoverCardBody } from 'app/components/hovercard';
var MAX_PROJECTS_IN_HOVERCARD = 5;
var ProjectList = function (_a) {
    var projects = _a.projects, orgId = _a.orgId, version = _a.version, _b = _a.maxLines, maxLines = _b === void 0 ? 2 : _b;
    var visibleProjects, hiddenProjects;
    if (projects.length <= maxLines) {
        visibleProjects = projects;
        hiddenProjects = [];
    }
    else {
        // because we need one line for `and X more`
        visibleProjects = projects.slice(0, maxLines - 1);
        hiddenProjects = projects.slice(maxLines - 1, projects.length);
    }
    var hoverCardHead = t('Release Projects');
    var hovercardBody = (<HovercardContentWrapper>
      <ProjectList projects={hiddenProjects} orgId={orgId} version={version} maxLines={MAX_PROJECTS_IN_HOVERCARD}/>
    </HovercardContentWrapper>);
    return (<React.Fragment>
      {visibleProjects.map(function (project) { return (<StyledProjectBadge project={project} avatarSize={14} key={project.slug}/>); })}
      {hiddenProjects.length > 0 && (<StyledHovercard header={hoverCardHead} body={hovercardBody} show={hiddenProjects.length <= MAX_PROJECTS_IN_HOVERCARD ? undefined : false}>
          <GlobalSelectionLink to={"/organizations/" + orgId + "/releases/" + encodeURIComponent(version) + "/"}>
            {tct('and [count] more', {
        count: hiddenProjects.length,
    })}
          </GlobalSelectionLink>
        </StyledHovercard>)}
    </React.Fragment>);
};
var StyledProjectBadge = styled(ProjectBadge)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  &:not(:last-child) {\n    margin-bottom: ", ";\n  }\n"], ["\n  &:not(:last-child) {\n    margin-bottom: ", ";\n  }\n"])), space(0.5));
var StyledHovercard = styled(Hovercard)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  width: auto;\n  max-width: 295px;\n  ", " {\n    padding-bottom: 0;\n  }\n"], ["\n  width: auto;\n  max-width: 295px;\n  ", " {\n    padding-bottom: 0;\n  }\n"])), HoverCardBody);
var HovercardContentWrapper = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: flex-start;\n  flex-wrap: wrap;\n  font-size: ", ";\n  ", " {\n    margin-right: ", ";\n    margin-bottom: ", ";\n  }\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: flex-start;\n  flex-wrap: wrap;\n  font-size: ", ";\n  ", " {\n    margin-right: ", ";\n    margin-bottom: ", ";\n  }\n"])), function (p) { return p.theme.fontSizeMedium; }, StyledProjectBadge, space(3), space(2));
export default ProjectList;
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=projectList.jsx.map