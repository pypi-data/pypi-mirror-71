import { __assign, __extends, __makeTemplateObject, __read, __spread } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import CommitRow from 'app/components/commitRow';
import { t } from 'app/locale';
import space from 'app/styles/space';
import EmptyStateWarning from 'app/components/emptyStateWarning';
import { PanelHeader, Panel, PanelBody } from 'app/components/panels';
import DropdownControl, { DropdownItem } from 'app/components/dropdownControl';
import overflowEllipsisLeft from 'app/styles/overflowEllipsisLeft';
import AsyncView from 'app/views/asyncView';
import routeTitleGen from 'app/utils/routeTitle';
import { formatVersion } from 'app/utils/formatters';
import withOrganization from 'app/utils/withOrganization';
import { getCommitsByRepository } from '../utils';
import ReleaseNoCommitData from '../releaseNoCommitData';
import { ReleaseContext } from '../';
var ALL_REPOSITORIES_LABEL = t('All Repositories');
var ReleaseCommits = /** @class */ (function (_super) {
    __extends(ReleaseCommits, _super);
    function ReleaseCommits() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleRepoFilterChange = function (repo) {
            _this.setState({ activeRepo: repo });
        };
        return _this;
    }
    ReleaseCommits.prototype.getTitle = function () {
        var _a = this.props, params = _a.params, organization = _a.organization;
        return routeTitleGen(t('Commits - Release %s', formatVersion(params.release)), organization.slug, false);
    };
    ReleaseCommits.prototype.getDefaultState = function () {
        return __assign(__assign({}, _super.prototype.getDefaultState.call(this)), { activeRepo: ALL_REPOSITORIES_LABEL });
    };
    ReleaseCommits.prototype.getEndpoints = function () {
        var params = this.props.params;
        var orgId = params.orgId, release = params.release;
        var project = this.context.project;
        return [
            [
                'commits',
                "/projects/" + orgId + "/" + project.slug + "/releases/" + encodeURIComponent(release) + "/commits/",
            ],
            ['repos', "/organizations/" + orgId + "/repos/"],
        ];
    };
    ReleaseCommits.prototype.renderRepoSwitcher = function (commitsByRepository) {
        var _this = this;
        var repos = Object.keys(commitsByRepository);
        var activeRepo = this.state.activeRepo;
        return (<RepoSwitcher>
        <DropdownControl label={<React.Fragment>
              <FilterText>{t('Filter')}: &nbsp; </FilterText>
              {activeRepo}
            </React.Fragment>}>
          {__spread([ALL_REPOSITORIES_LABEL], repos).map(function (repoName) { return (<DropdownItem key={repoName} onSelect={_this.handleRepoFilterChange} eventKey={repoName} isActive={repoName === activeRepo}>
              <RepoLabel>{repoName}</RepoLabel>
            </DropdownItem>); })}
        </DropdownControl>
      </RepoSwitcher>);
    };
    ReleaseCommits.prototype.renderCommitsForRepo = function (repo, commitsByRepository) {
        return (<Panel key={repo}>
        <PanelHeader>{repo}</PanelHeader>
        <PanelBody>
          {commitsByRepository[repo].map(function (commit) { return (<CommitRow key={commit.id} commit={commit}/>); })}
        </PanelBody>
      </Panel>);
    };
    ReleaseCommits.prototype.renderBody = function () {
        var _this = this;
        var orgId = this.props.params.orgId;
        var _a = this.state, commits = _a.commits, repos = _a.repos, activeRepo = _a.activeRepo;
        var commitsByRepository = getCommitsByRepository(commits);
        var reposToRender = activeRepo === ALL_REPOSITORIES_LABEL
            ? Object.keys(commitsByRepository)
            : [activeRepo];
        if (repos.length === 0) {
            return <ReleaseNoCommitData orgId={orgId}/>;
        }
        if (commits.length === 0) {
            return (<Panel>
          <PanelBody>
            <EmptyStateWarning small>
              {t('There are no commits associated with this release.')}
            </EmptyStateWarning>
          </PanelBody>
        </Panel>);
        }
        return (<React.Fragment>
        {Object.keys(commitsByRepository).length > 1 &&
            this.renderRepoSwitcher(commitsByRepository)}
        {reposToRender.map(function (repoName) {
            return _this.renderCommitsForRepo(repoName, commitsByRepository);
        })}
      </React.Fragment>);
    };
    ReleaseCommits.contextType = ReleaseContext;
    return ReleaseCommits;
}(AsyncView));
var RepoSwitcher = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space(1));
var FilterText = styled('em')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  font-style: normal;\n  color: ", ";\n"], ["\n  font-style: normal;\n  color: ", ";\n"])), function (p) { return p.theme.gray500; });
var RepoLabel = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  ", "\n"], ["\n  ", "\n"])), overflowEllipsisLeft);
export default withOrganization(ReleaseCommits);
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=index.jsx.map