import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import RepositoryFileSummary from 'app/components/repositoryFileSummary';
import { t } from 'app/locale';
import space from 'app/styles/space';
import EmptyStateWarning from 'app/components/emptyStateWarning';
import AsyncView from 'app/views/asyncView';
import withOrganization from 'app/utils/withOrganization';
import routeTitleGen from 'app/utils/routeTitle';
import { formatVersion } from 'app/utils/formatters';
import { Panel, PanelBody } from 'app/components/panels';
import { getFilesByRepository } from '../utils';
import ReleaseNoCommitData from '../releaseNoCommitData';
var FilesChanged = /** @class */ (function (_super) {
    __extends(FilesChanged, _super);
    function FilesChanged() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    FilesChanged.prototype.getTitle = function () {
        var _a = this.props, params = _a.params, organization = _a.organization;
        return routeTitleGen(t('Files Changed - Release %s', formatVersion(params.release)), organization.slug, false);
    };
    FilesChanged.prototype.getEndpoints = function () {
        var _a = this.props.params, orgId = _a.orgId, release = _a.release;
        return [
            [
                'fileList',
                "/organizations/" + orgId + "/releases/" + encodeURIComponent(release) + "/commitfiles/",
            ],
            ['repos', "/organizations/" + orgId + "/repos/"],
        ];
    };
    FilesChanged.prototype.renderBody = function () {
        var orgId = this.props.params.orgId;
        var _a = this.state, fileList = _a.fileList, repos = _a.repos;
        var filesByRepository = getFilesByRepository(fileList);
        if (repos.length === 0) {
            return <ReleaseNoCommitData orgId={orgId}/>;
        }
        return (<ContentBox>
        {fileList.length ? (Object.keys(filesByRepository).map(function (repository) { return (<RepositoryFileSummary key={repository} repository={repository} fileChangeSummary={filesByRepository[repository]} collapsable={false}/>); })) : (<Panel>
            <PanelBody>
              <EmptyStateWarning small>
                {t('There are no changed files.')}
              </EmptyStateWarning>
            </PanelBody>
          </Panel>)}
      </ContentBox>);
    };
    return FilesChanged;
}(AsyncView));
var ContentBox = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  h5 {\n    color: ", ";\n    font-size: ", ";\n    margin-bottom: ", ";\n  }\n"], ["\n  h5 {\n    color: ", ";\n    font-size: ", ";\n    margin-bottom: ", ";\n  }\n"])), function (p) { return p.theme.gray600; }, function (p) { return p.theme.fontSizeMedium; }, space(1.5));
export default withOrganization(FilesChanged);
var templateObject_1;
//# sourceMappingURL=index.jsx.map