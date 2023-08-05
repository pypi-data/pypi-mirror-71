import { __makeTemplateObject } from "tslib";
// TODO(matej): needs a little bit of styles tinkering when avatarSize is huge
// pretty similar to src/sentry/static/sentry/app/components/avatar/avatarList.tsx, does it make sense to merge into one reusable list?
import React from 'react';
import styled from '@emotion/styled';
import { tn } from 'app/locale';
import Tooltip from 'app/components/tooltip';
import ProjectAvatar from 'app/components/avatar/projectAvatar';
var ProjectList = function (_a) {
    var projects = _a.projects, _b = _a.maxVisibleProjects, maxVisibleProjects = _b === void 0 ? 5 : _b, _c = _a.avatarSize, avatarSize = _c === void 0 ? 20 : _c;
    var visibleProjects = projects.slice(0, maxVisibleProjects);
    var numberOfCollapsedProjects = projects.length - visibleProjects.length;
    return (<ProjectListWrapper>
      {numberOfCollapsedProjects > 0 && (<Tooltip title={tn('%s other project', '%s other projects', numberOfCollapsedProjects)}>
          <CollapsedProjects size={avatarSize}>
            {numberOfCollapsedProjects < 100 && <Plus size={avatarSize}>+</Plus>}
            {numberOfCollapsedProjects}
          </CollapsedProjects>
        </Tooltip>)}

      {visibleProjects.map(function (project) { return (<StyledProjectAvatar project={project} key={project.slug} tooltip={project.slug} size={avatarSize} hasTooltip/>); })}
    </ProjectListWrapper>);
};
var StyledProjectAvatar = styled(ProjectAvatar)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  position: relative;\n  margin-left: -", "px;\n  img {\n    box-shadow: 0 0 0 3px #fff;\n  }\n  &:hover {\n    z-index: 1;\n  }\n"], ["\n  position: relative;\n  margin-left: -", "px;\n  img {\n    box-shadow: 0 0 0 3px #fff;\n  }\n  &:hover {\n    z-index: 1;\n  }\n"])), function (p) { return Math.floor(p.size / 10); });
var ProjectListWrapper = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  flex-direction: row-reverse;\n  justify-content: flex-end;\n  span:last-child ", " {\n    margin-left: 0;\n  }\n"], ["\n  display: flex;\n  align-items: center;\n  flex-direction: row-reverse;\n  justify-content: flex-end;\n  span:last-child ", " {\n    margin-left: 0;\n  }\n"])), StyledProjectAvatar);
var CollapsedProjects = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: flex;\n  justify-content: center;\n  align-items: center;\n  width: ", "px;\n  height: ", "px;\n  border-radius: 3px;\n  box-shadow: 0 0 0 3px #fff;\n  background-color: ", ";\n  color: ", ";\n  position: relative;\n  margin-left: -", "px;\n  font-size: ", "px;\n  font-weight: 600;\n  cursor: default;\n  &:hover {\n    z-index: 1;\n  }\n"], ["\n  display: flex;\n  justify-content: center;\n  align-items: center;\n  width: ", "px;\n  height: ", "px;\n  border-radius: 3px;\n  box-shadow: 0 0 0 3px #fff;\n  background-color: ", ";\n  color: ", ";\n  position: relative;\n  margin-left: -", "px;\n  font-size: ", "px;\n  font-weight: 600;\n  cursor: default;\n  &:hover {\n    z-index: 1;\n  }\n"])), function (p) { return p.size; }, function (p) { return p.size; }, function (p) { return p.theme.borderLight; }, function (p) { return p.theme.gray500; }, function (p) { return Math.floor(p.size / 10); }, function (p) { return Math.floor(p.size / 2); });
var Plus = styled('span')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  font-size: ", "px;\n  font-weight: 600;\n  margin-left: 1px;\n  margin-right: -1px;\n"], ["\n  font-size: ", "px;\n  font-weight: 600;\n  margin-left: 1px;\n  margin-right: -1px;\n"])), function (p) { return Math.floor(p.size / 2); });
export default ProjectList;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=projectList.jsx.map