import { __assign, __awaiter, __extends, __generator, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { t } from 'app/locale';
import AsyncView from 'app/views/asyncView';
import routeTitleGen from 'app/utils/routeTitle';
import SearchBar from 'app/components/searchBar';
import Pagination from 'app/components/pagination';
import { PanelTable } from 'app/components/panels';
import space from 'app/styles/space';
import { formatVersion } from 'app/utils/formatters';
import TextBlock from 'app/views/settings/components/text/textBlock';
import SettingsPageHeader from 'app/views/settings/components/settingsPageHeader';
import Button from 'app/components/button';
import ButtonBar from 'app/components/buttonBar';
import { IconReleases, IconChevron } from 'app/icons';
import { addErrorMessage, addLoadingMessage, addSuccessMessage, } from 'app/actionCreators/indicator';
import { decodeScalar } from 'app/utils/queryString';
import SourceMapsArtifactRow from './sourceMapsArtifactRow';
var ProjectSourceMaps = /** @class */ (function (_super) {
    __extends(ProjectSourceMaps, _super);
    function ProjectSourceMaps() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleSearch = function (query) {
            var _a = _this.props, location = _a.location, router = _a.router;
            router.push(__assign(__assign({}, location), { query: __assign(__assign({}, location.query), { cursor: undefined, query: query }) }));
        };
        _this.handleDelete = function (id) { return __awaiter(_this, void 0, void 0, function () {
            var _a;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        addLoadingMessage(t('Removing artifact\u2026'));
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, this.api.requestPromise("" + this.getArtifactsUrl() + id + "/", {
                                method: 'DELETE',
                            })];
                    case 2:
                        _b.sent();
                        this.fetchData();
                        addSuccessMessage(t('Artifact removed.'));
                        return [3 /*break*/, 4];
                    case 3:
                        _a = _b.sent();
                        addErrorMessage(t('Unable to remove artifact. Please try again.'));
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        return _this;
    }
    ProjectSourceMaps.prototype.getTitle = function () {
        var _a = this.props.params, projectId = _a.projectId, version = _a.version;
        return routeTitleGen(t('Source Maps %s', formatVersion(version)), projectId, false);
    };
    ProjectSourceMaps.prototype.getDefaultState = function () {
        return __assign(__assign({}, _super.prototype.getDefaultState.call(this)), { artifacts: [] });
    };
    ProjectSourceMaps.prototype.getEndpoints = function () {
        return [['artifacts', this.getArtifactsUrl(), { query: { query: this.getQuery() } }]];
    };
    ProjectSourceMaps.prototype.getArtifactsUrl = function () {
        var _a = this.props.params, orgId = _a.orgId, projectId = _a.projectId, version = _a.version;
        return "/projects/" + orgId + "/" + projectId + "/releases/" + encodeURIComponent(version) + "/files/";
    };
    ProjectSourceMaps.prototype.getQuery = function () {
        var query = this.props.location.query.query;
        return decodeScalar(query);
    };
    ProjectSourceMaps.prototype.getEmptyMessage = function () {
        if (this.getQuery()) {
            return t('There are no artifacts that match your search.');
        }
        return t('There are no artifacts for this release.');
    };
    ProjectSourceMaps.prototype.renderLoading = function () {
        return this.renderBody();
    };
    ProjectSourceMaps.prototype.renderArtifacts = function () {
        var _this = this;
        var artifacts = this.state.artifacts;
        var artifactApiUrl = this.api.baseUrl + this.getArtifactsUrl();
        if (!artifacts.length) {
            return null;
        }
        return artifacts.map(function (artifact) {
            return (<SourceMapsArtifactRow key={artifact.id} artifact={artifact} onDelete={_this.handleDelete} downloadUrl={"" + artifactApiUrl + artifact.id + "/?download=1"}/>);
        });
    };
    ProjectSourceMaps.prototype.renderBody = function () {
        var _a = this.state, loading = _a.loading, artifacts = _a.artifacts, artifactsPageLinks = _a.artifactsPageLinks;
        var _b = this.props.params, version = _b.version, orgId = _b.orgId, projectId = _b.projectId;
        var project = this.props.project;
        return (<React.Fragment>
        <SettingsPageHeader title={t('Source Maps Archive %s', formatVersion(version))} action={<ButtonBar gap={1}>
              <Button size="small" to={"/settings/" + orgId + "/projects/" + projectId + "/source-maps/"} icon={<IconChevron size="xs" direction="left"/>}>
                {t('All Archives')}
              </Button>
              <Button size="small" to={"/organizations/" + orgId + "/releases/" + encodeURIComponent(version) + "/?project=" + project.id} icon={<IconReleases size="xs"/>}>
                {t('View Release')}
              </Button>
            </ButtonBar>}/>

        <Wrapper>
          <TextBlock noMargin>{t('Uploaded artifacts')}:</TextBlock>
          <SearchBar placeholder={t('Filter artifacts')} onSearch={this.handleSearch} query={this.getQuery()}/>
        </Wrapper>

        <StyledPanelTable headers={[
            t('Artifact'),
            t('Size'),
            <Actions key="actions">{t('Actions')}</Actions>,
        ]} emptyMessage={this.getEmptyMessage()} isEmpty={artifacts.length === 0} isLoading={loading}>
          {this.renderArtifacts()}
        </StyledPanelTable>
        <Pagination pageLinks={artifactsPageLinks}/>
      </React.Fragment>);
    };
    return ProjectSourceMaps;
}(AsyncView));
var StyledPanelTable = styled(PanelTable)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  grid-template-columns: 1fr 100px 150px;\n"], ["\n  grid-template-columns: 1fr 100px 150px;\n"])));
var Actions = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  text-align: right;\n"], ["\n  text-align: right;\n"])));
var Wrapper = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: auto minmax(200px, 400px);\n  grid-gap: ", ";\n  align-items: center;\n  margin-bottom: ", ";\n  margin-top: ", ";\n  @media (max-width: ", ") {\n    display: block;\n  }\n"], ["\n  display: grid;\n  grid-template-columns: auto minmax(200px, 400px);\n  grid-gap: ", ";\n  align-items: center;\n  margin-bottom: ", ";\n  margin-top: ", ";\n  @media (max-width: ", ") {\n    display: block;\n  }\n"])), space(4), space(1), space(1), function (p) { return p.theme.breakpoints[0]; });
export default ProjectSourceMaps;
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=index.jsx.map