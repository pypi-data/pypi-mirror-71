import { __assign, __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import * as ReactRouter from 'react-router';
import styled from '@emotion/styled';
import isEqual from 'lodash/isEqual';
import { t } from 'app/locale';
import { loadOrganizationTags } from 'app/actionCreators/tags';
import FeatureBadge from 'app/components/featureBadge';
import SearchBar from 'app/views/events/searchBar';
import SentryDocumentTitle from 'app/components/sentryDocumentTitle';
import GlobalSelectionHeader from 'app/components/organizations/globalSelectionHeader';
import { ALL_ACCESS_PROJECTS } from 'app/constants/globalSelectionHeader';
import { PageContent } from 'app/styles/organization';
import LightWeightNoProjectMessage from 'app/components/lightWeightNoProjectMessage';
import Alert from 'app/components/alert';
import space from 'app/styles/space';
import Button from 'app/components/button';
import ButtonBar from 'app/components/buttonBar';
import { decodeScalar } from 'app/utils/queryString';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import withApi from 'app/utils/withApi';
import withGlobalSelection from 'app/utils/withGlobalSelection';
import withOrganization from 'app/utils/withOrganization';
import withProjects from 'app/utils/withProjects';
import { tokenizeSearch, stringifyQueryObject } from 'app/utils/tokenizeSearch';
import { generatePerformanceEventView, DEFAULT_STATS_PERIOD } from './data';
import Table from './table';
import Charts from './charts/index';
import Onboarding from './onboarding';
var FilterViews;
(function (FilterViews) {
    FilterViews["ALL_TRANSACTIONS"] = "ALL_TRANSACTIONS";
    FilterViews["KEY_TRANSACTIONS"] = "KEY_TRANSACTIONS";
})(FilterViews || (FilterViews = {}));
var VIEWS = Object.values(FilterViews);
var PerformanceLanding = /** @class */ (function (_super) {
    __extends(PerformanceLanding, _super);
    function PerformanceLanding() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            eventView: generatePerformanceEventView(_this.props.location),
            error: undefined,
            currentView: FilterViews.ALL_TRANSACTIONS,
        };
        _this.setError = function (error) {
            _this.setState({ error: error });
        };
        _this.handleSearch = function (searchQuery) {
            var _a = _this.props, location = _a.location, organization = _a.organization;
            trackAnalyticsEvent({
                eventKey: 'performance_views.overview.search',
                eventName: 'Performance Views: Transaction overview search',
                organization_id: parseInt(organization.id, 10),
            });
            ReactRouter.browserHistory.push({
                pathname: location.pathname,
                query: __assign(__assign({}, location.query), { cursor: undefined, query: String(searchQuery).trim() || undefined }),
            });
        };
        return _this;
    }
    PerformanceLanding.getDerivedStateFromProps = function (nextProps, prevState) {
        return __assign(__assign({}, prevState), { eventView: generatePerformanceEventView(nextProps.location) });
    };
    PerformanceLanding.prototype.componentDidMount = function () {
        var _a = this.props, api = _a.api, organization = _a.organization, selection = _a.selection;
        loadOrganizationTags(api, organization.slug, selection);
    };
    PerformanceLanding.prototype.componentDidUpdate = function (prevProps) {
        var _a = this.props, api = _a.api, organization = _a.organization, selection = _a.selection;
        if (!isEqual(prevProps.selection.projects, selection.projects) ||
            !isEqual(prevProps.selection.datetime, selection.datetime)) {
            loadOrganizationTags(api, organization.slug, selection);
        }
    };
    PerformanceLanding.prototype.renderError = function () {
        var error = this.state.error;
        if (!error) {
            return null;
        }
        return (<Alert type="error" icon="icon-circle-exclamation">
        {error}
      </Alert>);
    };
    PerformanceLanding.prototype.getViewLabel = function (currentView) {
        switch (currentView) {
            case FilterViews.ALL_TRANSACTIONS:
                return t('By Transaction');
            case FilterViews.KEY_TRANSACTIONS:
                return t('By Key Transaction');
            default:
                throw Error("Unknown view: " + currentView);
        }
    };
    PerformanceLanding.prototype.getTransactionSearchQuery = function () {
        var location = this.props.location;
        return String(decodeScalar(location.query.query) || '').trim();
    };
    /**
     * Generate conditions to foward to the summary views.
     *
     * We drop the bare text string as in this view we apply it to
     * the transaction name, and that condition is redundant in the
     * summary view.
     */
    PerformanceLanding.prototype.getSummaryConditions = function (query) {
        var parsed = tokenizeSearch(query);
        parsed.query = [];
        return stringifyQueryObject(parsed);
    };
    PerformanceLanding.prototype.renderHeaderButtons = function () {
        var _this = this;
        var selectView = function (viewKey) {
            return function () {
                _this.setState({
                    currentView: viewKey,
                });
            };
        };
        return (<ButtonBar merged active={this.state.currentView}>
        {VIEWS.map(function (viewKey) {
            return (<Button key={viewKey} barId={viewKey} size="small" onClick={selectView(viewKey)}>
              {_this.getViewLabel(viewKey)}
            </Button>);
        })}
      </ButtonBar>);
    };
    PerformanceLanding.prototype.shouldShowOnboarding = function () {
        var _a = this.props, projects = _a.projects, demoMode = _a.demoMode;
        var eventView = this.state.eventView;
        // XXX used by getsentry to bypass onboarding for the upsell demo state.
        if (demoMode) {
            return false;
        }
        if (projects.length === 0) {
            return false;
        }
        // Current selection is 'my projects' or 'all projects'
        if (eventView.project.length === 0 || eventView.project === [ALL_ACCESS_PROJECTS]) {
            return (projects.filter(function (p) { return p.firstTransactionEvent === false; }).length === projects.length);
        }
        // Any other subset of projects.
        return (projects.filter(function (p) {
            return eventView.project.includes(parseInt(p.id, 10)) &&
                p.firstTransactionEvent === false;
        }).length === eventView.project.length);
    };
    PerformanceLanding.prototype.render = function () {
        var _a = this.props, organization = _a.organization, location = _a.location, router = _a.router, projects = _a.projects;
        var eventView = this.state.eventView;
        var showOnboarding = this.shouldShowOnboarding();
        var filterString = this.getTransactionSearchQuery();
        var summaryConditions = this.getSummaryConditions(filterString);
        return (<SentryDocumentTitle title={t('Performance')} objSlug={organization.slug}>
        <GlobalSelectionHeader defaultSelection={{
            datetime: {
                start: null,
                end: null,
                utc: false,
                period: DEFAULT_STATS_PERIOD,
            },
        }}>
          <PageContent>
            <LightWeightNoProjectMessage organization={organization}>
              <StyledPageHeader>
                <div>
                  {t('Performance')} <FeatureBadge type="beta"/>
                </div>
                {!showOnboarding && <div>{this.renderHeaderButtons()}</div>}
              </StyledPageHeader>
              {this.renderError()}
              {showOnboarding ? (<Onboarding />) : (<div>
                  <StyledSearchBar organization={organization} projectIds={eventView.project} query={filterString} fields={eventView.fields} onSearch={this.handleSearch}/>
                  <Charts eventView={eventView} organization={organization} location={location} router={router} keyTransactions={this.state.currentView === 'KEY_TRANSACTIONS'}/>
                  <Table eventView={eventView} projects={projects} organization={organization} location={location} setError={this.setError} keyTransactions={this.state.currentView === 'KEY_TRANSACTIONS'} summaryConditions={summaryConditions}/>
                </div>)}
            </LightWeightNoProjectMessage>
          </PageContent>
        </GlobalSelectionHeader>
      </SentryDocumentTitle>);
    };
    return PerformanceLanding;
}(React.Component));
export var StyledPageHeader = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  font-size: ", ";\n  color: ", ";\n  height: 40px;\n  margin-bottom: ", ";\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  font-size: ", ";\n  color: ", ";\n  height: 40px;\n  margin-bottom: ", ";\n"])), function (p) { return p.theme.headerFontSize; }, function (p) { return p.theme.gray700; }, space(1));
var StyledSearchBar = styled(SearchBar)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  flex-grow: 1;\n\n  margin-bottom: ", ";\n"], ["\n  flex-grow: 1;\n\n  margin-bottom: ", ";\n"])), space(2));
export default withApi(withOrganization(withProjects(withGlobalSelection(PerformanceLanding))));
var templateObject_1, templateObject_2;
//# sourceMappingURL=landing.jsx.map