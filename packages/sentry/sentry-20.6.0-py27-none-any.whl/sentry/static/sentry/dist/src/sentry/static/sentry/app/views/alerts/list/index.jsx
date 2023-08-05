import { __assign, __awaiter, __extends, __generator, __makeTemplateObject } from "tslib";
import DocumentTitle from 'react-document-title';
import React from 'react';
import flatten from 'lodash/flatten';
import omit from 'lodash/omit';
import styled from '@emotion/styled';
import { IconAdd, IconSettings } from 'app/icons';
import { PageContent, PageHeader } from 'app/styles/organization';
import { Panel, PanelBody, PanelHeader } from 'app/components/panels';
import { navigateTo } from 'app/actionCreators/navigation';
import { t, tct } from 'app/locale';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import Alert from 'app/components/alert';
import AsyncComponent from 'app/components/asyncComponent';
import FeatureBadge from 'app/components/featureBadge';
import Button from 'app/components/button';
import ButtonBar from 'app/components/buttonBar';
import EmptyStateWarning from 'app/components/emptyStateWarning';
import ExternalLink from 'app/components/links/externalLink';
import LoadingIndicator from 'app/components/loadingIndicator';
import PageHeading from 'app/components/pageHeading';
import Pagination from 'app/components/pagination';
import Projects from 'app/utils/projects';
import space from 'app/styles/space';
import withOrganization from 'app/utils/withOrganization';
import Access from 'app/components/acl/access';
import ConfigStore from 'app/stores/configStore';
import GlobalSelectionHeader from 'app/components/organizations/globalSelectionHeader';
import { TableLayout, TitleAndSparkLine } from './styles';
import AlertListRow from './row';
var DEFAULT_QUERY_STATUS = 'open';
var trackDocumentationClicked = function (org) {
    return trackAnalyticsEvent({
        eventKey: 'alert_stream.documentation_clicked',
        eventName: 'Alert Stream: Documentation Clicked',
        organization_id: org.id,
        user_id: ConfigStore.get('user').id,
    });
};
function getQueryStatus(status) {
    return ['open', 'closed'].includes(status) ? status : DEFAULT_QUERY_STATUS;
}
var IncidentsList = /** @class */ (function (_super) {
    __extends(IncidentsList, _super);
    function IncidentsList() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        /**
         * Incidents list is currently at the organization level, but the link needs to
         * go down to a specific project scope.
         */
        _this.handleAddAlertRule = function (e) {
            var _a = _this.props, router = _a.router, params = _a.params;
            e.preventDefault();
            navigateTo("/settings/" + params.orgId + "/projects/:projectId/alerts/new/", router);
        };
        return _this;
    }
    IncidentsList.prototype.getEndpoints = function () {
        var _a = this.props, params = _a.params, location = _a.location;
        var query = location.query;
        var status = getQueryStatus(query.status);
        return [
            [
                'incidentList',
                "/organizations/" + (params && params.orgId) + "/incidents/",
                {
                    query: __assign(__assign({}, query), { status: status }),
                },
            ],
        ];
    };
    IncidentsList.prototype.onLoadAllEndpointsSuccess = function () {
        return __awaiter(this, void 0, void 0, function () {
            var incidentList, params, alertRules, err_1;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        incidentList = this.state.incidentList;
                        if (incidentList.length !== 0) {
                            return [2 /*return*/];
                        }
                        params = this.props.params;
                        _a.label = 1;
                    case 1:
                        _a.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, this.api.requestPromise("/organizations/" + (params && params.orgId) + "/alert-rules/", {
                                method: 'GET',
                            })];
                    case 2:
                        alertRules = _a.sent();
                        this.setState({
                            hasAlertRule: alertRules.length > 0 ? true : false,
                        });
                        return [3 /*break*/, 4];
                    case 3:
                        err_1 = _a.sent();
                        this.setState({
                            hasAlertRule: true,
                        });
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        });
    };
    IncidentsList.prototype.renderEmpty = function () {
        var location = this.props.location;
        var query = location.query;
        var status = getQueryStatus(query.status);
        var hasAlertRule = this.state.hasAlertRule ? this.state.hasAlertRule : false;
        return (<EmptyStateWarning>
        <p>
          <React.Fragment>
            {tct('No [status] metric alerts. ', {
            status: status === 'open' ? 'active' : 'resolved',
        })}
          </React.Fragment>
          <React.Fragment>
            {!hasAlertRule
            ? tct('Start by [link:creating your first rule].', {
                link: <ExternalLink onClick={this.handleAddAlertRule}/>,
            })
            : ''}
          </React.Fragment>
        </p>
      </EmptyStateWarning>);
    };
    IncidentsList.prototype.renderLoading = function () {
        return this.renderBody();
    };
    IncidentsList.prototype.renderBody = function () {
        var _a = this.state, loading = _a.loading, incidentList = _a.incidentList, incidentListPageLinks = _a.incidentListPageLinks, hasAlertRule = _a.hasAlertRule;
        var orgId = this.props.params.orgId;
        var allProjectsFromIncidents = new Set(flatten(incidentList === null || incidentList === void 0 ? void 0 : incidentList.map(function (_a) {
            var projects = _a.projects;
            return projects;
        })));
        var checkingForAlertRules = incidentList && incidentList.length === 0 && hasAlertRule === undefined
            ? true
            : false;
        var showLoadingIndicator = loading || checkingForAlertRules;
        var status = getQueryStatus(this.props.location.query.status);
        return (<React.Fragment>
        <Panel>
          <StyledPanelHeader>
            <TableLayout status={status}>
              <PaddedTitleAndSparkLine status={status}>
                <div>{t('Alert')}</div>
                {status === 'open' && <div>{t('Graph')}</div>}
              </PaddedTitleAndSparkLine>
              <div>{t('Project')}</div>
              <div>{t('Triggered')}</div>
              {status === 'closed' && <div>{t('Duration')}</div>}
              {status === 'closed' && <div>{t('Resolved')}</div>}
            </TableLayout>
          </StyledPanelHeader>

          <PanelBody>
            {showLoadingIndicator && <LoadingIndicator />}
            {!showLoadingIndicator && (<React.Fragment>
                {incidentList.length === 0 && this.renderEmpty()}
                <Projects orgId={orgId} slugs={Array.from(allProjectsFromIncidents)}>
                  {function (_a) {
            var initiallyLoaded = _a.initiallyLoaded, projects = _a.projects;
            return incidentList.map(function (incident) { return (<AlertListRow key={incident.id} projectsLoaded={initiallyLoaded} projects={projects} incident={incident} orgId={orgId} filteredStatus={status}/>); });
        }}
                </Projects>
              </React.Fragment>)}
          </PanelBody>
        </Panel>
        <Pagination pageLinks={incidentListPageLinks}/>
      </React.Fragment>);
    };
    return IncidentsList;
}(AsyncComponent));
var IncidentsListContainer = /** @class */ (function (_super) {
    __extends(IncidentsListContainer, _super);
    function IncidentsListContainer() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        /**
         * Incidents list is currently at the organization level, but the link needs to
         * go down to a specific project scope.
         */
        _this.handleAddAlertRule = function (e) {
            var _a = _this.props, router = _a.router, params = _a.params;
            e.preventDefault();
            navigateTo("/settings/" + params.orgId + "/projects/:projectId/alerts/new/", router);
        };
        /**
         * Incidents list is currently at the organization level, but the link needs to
         * go down to a specific project scope.
         */
        _this.handleNavigateToSettings = function (e) {
            var _a = _this.props, router = _a.router, params = _a.params;
            e.preventDefault();
            navigateTo("/settings/" + params.orgId + "/projects/:projectId/alerts/", router);
        };
        return _this;
    }
    IncidentsListContainer.prototype.componentDidMount = function () {
        this.trackView();
    };
    IncidentsListContainer.prototype.componentDidUpdate = function (nextProps) {
        var _a, _b;
        if (((_a = nextProps.location.query) === null || _a === void 0 ? void 0 : _a.status) !== ((_b = this.props.location.query) === null || _b === void 0 ? void 0 : _b.status)) {
            this.trackView();
        }
    };
    IncidentsListContainer.prototype.trackView = function () {
        var _a = this.props, location = _a.location, organization = _a.organization;
        var status = getQueryStatus(location.query.status);
        trackAnalyticsEvent({
            eventKey: 'alert_stream.viewed',
            eventName: 'Alert Stream: Viewed',
            organization_id: organization.id,
            status: status,
        });
    };
    IncidentsListContainer.prototype.render = function () {
        var _this = this;
        var _a = this.props, params = _a.params, location = _a.location, organization = _a.organization;
        var pathname = location.pathname, query = location.query;
        var orgId = params.orgId;
        var openIncidentsQuery = omit(__assign(__assign({}, query), { status: 'open' }), 'cursor');
        var closedIncidentsQuery = omit(__assign(__assign({}, query), { status: 'closed' }), 'cursor');
        var status = getQueryStatus(query.status);
        return (<DocumentTitle title={"Alerts- " + orgId + " - Sentry"}>
        <GlobalSelectionHeader organization={organization} showDateSelector={false}>
          <PageContent>
            <PageHeader>
              <StyledPageHeading>
                {t('Alerts')} <FeatureBadge type="beta"/>
              </StyledPageHeading>

              <Actions>
                <Access organization={organization} access={['project:write']}>
                  {function (_a) {
            var hasAccess = _a.hasAccess;
            return (<Button disabled={!hasAccess} title={!hasAccess
                ? t('Users with admin permission or higher can create alert rules.')
                : undefined} onClick={_this.handleAddAlertRule} priority="primary" href="#" size="small" icon={<IconAdd isCircled size="xs"/>}>
                      {t('Add Alert Rule')}
                    </Button>);
        }}
                </Access>

                <Button onClick={this.handleNavigateToSettings} href="#" size="small" icon={<IconSettings size="xs"/>}>
                  {t('View Rules')}
                </Button>

                <ButtonBar merged active={status}>
                  <Button to={{ pathname: pathname, query: openIncidentsQuery }} barId="open" size="small">
                    {t('Active')}
                  </Button>
                  <Button to={{ pathname: pathname, query: closedIncidentsQuery }} barId="closed" size="small">
                    {t('Resolved')}
                  </Button>
                </ButtonBar>
              </Actions>
            </PageHeader>

            <Alert type="info" icon="icon-circle-info">
              {tct('This page is in beta and currently only shows [link:metric alerts]. ', {
            link: (<ExternalLink onClick={function () { return trackDocumentationClicked(organization); }} href="https://docs.sentry.io/workflow/alerts-notifications/alerts/"/>),
        })}
              <ExternalLink href="mailto:alerting-feedback@sentry.io">
                {t('Please contact us if you have any feedback.')}
              </ExternalLink>
            </Alert>
            <IncidentsList {...this.props}/>
          </PageContent>
        </GlobalSelectionHeader>
      </DocumentTitle>);
    };
    return IncidentsListContainer;
}(React.Component));
var StyledPageHeading = styled(PageHeading)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n"], ["\n  display: flex;\n  align-items: center;\n"])));
var PaddedTitleAndSparkLine = styled(TitleAndSparkLine)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  padding-left: ", ";\n"], ["\n  padding-left: ", ";\n"])), space(2));
var StyledPanelHeader = styled(PanelHeader)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  /* Match table row padding for the grid to align */\n  padding: ", " ", " ", " 0;\n"], ["\n  /* Match table row padding for the grid to align */\n  padding: ", " ", " ", " 0;\n"])), space(1.5), space(2), space(1.5));
var Actions = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  display: grid;\n  align-items: center;\n  grid-gap: ", ";\n  grid-auto-flow: column;\n"], ["\n  display: grid;\n  align-items: center;\n  grid-gap: ", ";\n  grid-auto-flow: column;\n"])), space(1));
export default withOrganization(IncidentsListContainer);
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=index.jsx.map