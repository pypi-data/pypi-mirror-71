import { __assign, __extends, __makeTemplateObject, __read, __spread } from "tslib";
import React from 'react';
import pick from 'lodash/pick';
import styled from '@emotion/styled';
import { t } from 'app/locale';
import AsyncView from 'app/views/asyncView';
import GlobalSelectionHeader from 'app/components/organizations/globalSelectionHeader';
import LightWeightNoProjectMessage from 'app/components/lightWeightNoProjectMessage';
import { PageContent } from 'app/styles/organization';
import withOrganization from 'app/utils/withOrganization';
import routeTitleGen from 'app/utils/routeTitle';
import { URL_PARAM } from 'app/constants/globalSelectionHeader';
import { formatVersion } from 'app/utils/formatters';
import AsyncComponent from 'app/components/asyncComponent';
import withGlobalSelection from 'app/utils/withGlobalSelection';
import LoadingIndicator from 'app/components/loadingIndicator';
import { IconInfo, IconWarning } from 'app/icons';
import space from 'app/styles/space';
import Alert from 'app/components/alert';
import ReleaseHeader from './releaseHeader';
import PickProjectToContinue from './pickProjectToContinue';
var ReleaseContext = React.createContext({});
var ReleasesV2Detail = /** @class */ (function (_super) {
    __extends(ReleasesV2Detail, _super);
    function ReleasesV2Detail() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.shouldReload = true;
        return _this;
    }
    ReleasesV2Detail.prototype.getTitle = function () {
        var _a = this.props, params = _a.params, organization = _a.organization;
        return routeTitleGen(t('Release %s', formatVersion(params.release)), organization.slug, false);
    };
    ReleasesV2Detail.prototype.getDefaultState = function () {
        return __assign(__assign({}, _super.prototype.getDefaultState.call(this)), { deploys: [] });
    };
    ReleasesV2Detail.prototype.getEndpoints = function () {
        var _a = this.props, organization = _a.organization, location = _a.location, params = _a.params, releaseMeta = _a.releaseMeta;
        var query = __assign(__assign({}, pick(location.query, __spread(Object.values(URL_PARAM)))), { health: 1 });
        var basePath = "/organizations/" + organization.slug + "/releases/" + encodeURIComponent(params.release) + "/";
        var endpoints = [
            ['release', basePath, { query: query }],
        ];
        if (releaseMeta.deployCount > 0) {
            endpoints.push(['deploys', basePath + "deploys/"]);
        }
        return endpoints;
    };
    ReleasesV2Detail.prototype.renderError = function () {
        var args = [];
        for (var _i = 0; _i < arguments.length; _i++) {
            args[_i] = arguments[_i];
        }
        var possiblyWrongProject = Object.values(this.state.errors).find(function (e) { return (e === null || e === void 0 ? void 0 : e.status) === 404 || (e === null || e === void 0 ? void 0 : e.status) === 403; });
        if (possiblyWrongProject) {
            return (<PageContent>
          <Alert type="error" icon={<IconWarning />}>
            {t('This release may not be in your selected project.')}
          </Alert>
        </PageContent>);
        }
        return _super.prototype.renderError.apply(this, __spread(args));
    };
    ReleasesV2Detail.prototype.renderLoading = function () {
        return (<PageContent>
        <LoadingIndicator />
      </PageContent>);
    };
    ReleasesV2Detail.prototype.renderBody = function () {
        var _a = this.props, organization = _a.organization, location = _a.location, selection = _a.selection, releaseMeta = _a.releaseMeta;
        var _b = this.state, release = _b.release, deploys = _b.deploys, reloading = _b.reloading;
        var project = release === null || release === void 0 ? void 0 : release.projects.find(function (p) { return p.id === selection.projects[0]; });
        if (!project || !release) {
            if (reloading) {
                return <LoadingIndicator />;
            }
            return null;
        }
        return (<LightWeightNoProjectMessage organization={organization}>
        <StyledPageContent>
          <ReleaseHeader location={location} orgId={organization.slug} release={release} project={project} releaseMeta={releaseMeta}/>

          <ContentBox>
            <ReleaseContext.Provider value={{ release: release, project: project, deploys: deploys, releaseMeta: releaseMeta }}>
              {this.props.children}
            </ReleaseContext.Provider>
          </ContentBox>
        </StyledPageContent>
      </LightWeightNoProjectMessage>);
    };
    return ReleasesV2Detail;
}(AsyncView));
var ReleasesV2DetailContainer = /** @class */ (function (_super) {
    __extends(ReleasesV2DetailContainer, _super);
    function ReleasesV2DetailContainer() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.shouldReload = true;
        return _this;
    }
    ReleasesV2DetailContainer.prototype.getEndpoints = function () {
        var _a = this.props, organization = _a.organization, params = _a.params;
        // fetch projects this release belongs to
        return [
            [
                'releaseMeta',
                "/organizations/" + organization.slug + "/releases/" + encodeURIComponent(params.release) + "/meta/",
            ],
        ];
    };
    ReleasesV2DetailContainer.prototype.renderError = function () {
        var args = [];
        for (var _i = 0; _i < arguments.length; _i++) {
            args[_i] = arguments[_i];
        }
        var has404Errors = Object.values(this.state.errors).find(function (e) { return (e === null || e === void 0 ? void 0 : e.status) === 404; });
        if (has404Errors) {
            // This catches a 404 coming from the release endpoint and displays a custom error message.
            return (<PageContent>
          <Alert type="error" icon={<IconWarning />}>
            {t('This release could not be found.')}
          </Alert>
        </PageContent>);
        }
        return _super.prototype.renderError.apply(this, __spread(args));
    };
    ReleasesV2DetailContainer.prototype.isProjectMissingInUrl = function () {
        var projectId = this.props.location.query.project;
        return !projectId || typeof projectId !== 'string';
    };
    ReleasesV2DetailContainer.prototype.renderLoading = function () {
        return (<PageContent>
        <LoadingIndicator />
      </PageContent>);
    };
    ReleasesV2DetailContainer.prototype.renderProjectsFooterMessage = function () {
        return (<ProjectsFooterMessage>
        <IconInfo size="xs"/> {t('Only projects with this release are visible.')}
      </ProjectsFooterMessage>);
    };
    ReleasesV2DetailContainer.prototype.renderBody = function () {
        var _a = this.props, organization = _a.organization, params = _a.params, router = _a.router;
        var releaseMeta = this.state.releaseMeta;
        var projects = releaseMeta.projects;
        if (this.isProjectMissingInUrl()) {
            return (<PickProjectToContinue orgSlug={organization.slug} version={params.release} router={router} projects={projects}/>);
        }
        return (<GlobalSelectionHeader lockedMessageSubject={t('release')} shouldForceProject={projects.length === 1} forceProject={projects.length === 1 ? projects[0] : undefined} specificProjectSlugs={projects.map(function (p) { return p.slug; })} disableMultipleProjectSelection showProjectSettingsLink projectsFooterMessage={this.renderProjectsFooterMessage()}>
        <ReleasesV2Detail {...this.props} releaseMeta={releaseMeta}/>
      </GlobalSelectionHeader>);
    };
    return ReleasesV2DetailContainer;
}(AsyncComponent));
var StyledPageContent = styled(PageContent)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  padding: 0;\n"], ["\n  padding: 0;\n"])));
var ProjectsFooterMessage = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: grid;\n  align-items: center;\n  grid-template-columns: min-content 1fr;\n  grid-gap: ", ";\n"], ["\n  display: grid;\n  align-items: center;\n  grid-template-columns: min-content 1fr;\n  grid-gap: ", ";\n"])), space(1));
var ContentBox = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  padding: ", ";\n  flex: 1;\n  background-color: white;\n"], ["\n  padding: ", ";\n  flex: 1;\n  background-color: white;\n"])), space(4));
export { ReleasesV2DetailContainer, ReleaseContext };
export default withGlobalSelection(withOrganization(ReleasesV2DetailContainer));
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=index.jsx.map