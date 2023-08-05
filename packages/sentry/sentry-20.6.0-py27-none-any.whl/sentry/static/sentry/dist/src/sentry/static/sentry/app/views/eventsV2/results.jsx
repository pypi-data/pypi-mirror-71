import { __assign, __awaiter, __extends, __generator, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import * as Sentry from '@sentry/browser';
import * as ReactRouter from 'react-router';
import omit from 'lodash/omit';
import isEqual from 'lodash/isEqual';
import { PageContent } from 'app/styles/organization';
import { getParams } from 'app/components/organizations/globalSelectionHeader/getParams';
import { fetchTotalCount } from 'app/actionCreators/events';
import { loadOrganizationTags } from 'app/actionCreators/tags';
import Alert from 'app/components/alert';
import GlobalSelectionHeader from 'app/components/organizations/globalSelectionHeader';
import LightWeightNoProjectMessage from 'app/components/lightWeightNoProjectMessage';
import SentryDocumentTitle from 'app/components/sentryDocumentTitle';
import space from 'app/styles/space';
import SearchBar from 'app/views/events/searchBar';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import withApi from 'app/utils/withApi';
import withOrganization from 'app/utils/withOrganization';
import withGlobalSelection from 'app/utils/withGlobalSelection';
import EventView, { isAPIPayloadSimilar } from 'app/utils/discover/eventView';
import { ContentBox, Main, Side } from 'app/utils/discover/styles';
import { generateQueryWithTag } from 'app/utils';
import localStorage from 'app/utils/localStorage';
import { decodeScalar } from 'app/utils/queryString';
import { DEFAULT_EVENT_VIEW } from './data';
import Table from './table';
import Tags from './tags';
import ResultsHeader from './resultsHeader';
import ResultsChart from './resultsChart';
import { generateTitle } from './utils';
var SHOW_TAGS_STORAGE_KEY = 'discover2:show-tags';
function readShowTagsState() {
    var value = localStorage.getItem(SHOW_TAGS_STORAGE_KEY);
    return value === '1';
}
var Results = /** @class */ (function (_super) {
    __extends(Results, _super);
    function Results() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            eventView: EventView.fromLocation(_this.props.location),
            error: '',
            errorCode: 200,
            totalValues: null,
            showTags: readShowTagsState(),
        };
        _this.handleChangeShowTags = function () {
            var organization = _this.props.organization;
            trackAnalyticsEvent({
                eventKey: 'discover_v2.results.toggle_tag_facets',
                eventName: 'Discoverv2: Toggle Tag Facets',
                organization_id: parseInt(organization.id, 10),
            });
            _this.setState(function (state) {
                var newValue = !state.showTags;
                localStorage.setItem(SHOW_TAGS_STORAGE_KEY, newValue ? '1' : '0');
                return __assign(__assign({}, state), { showTags: newValue });
            });
        };
        _this.handleSearch = function (query) {
            var _a = _this.props, router = _a.router, location = _a.location;
            var queryParams = getParams(__assign(__assign({}, (location.query || {})), { query: query }));
            // do not propagate pagination when making a new search
            var searchQueryParams = omit(queryParams, 'cursor');
            router.push({
                pathname: location.pathname,
                query: searchQueryParams,
            });
        };
        _this.handleYAxisChange = function (value) {
            var _a = _this.props, router = _a.router, location = _a.location;
            var newQuery = __assign(__assign({}, location.query), { yAxis: value });
            router.push({
                pathname: location.pathname,
                query: newQuery,
            });
            trackAnalyticsEvent({
                eventKey: 'discover_v2.y_axis_change',
                eventName: "Discoverv2: Change chart's y axis",
                organization_id: parseInt(_this.props.organization.id, 10),
                y_axis_value: value,
            });
        };
        _this.handleDisplayChange = function (value) {
            var _a = _this.props, router = _a.router, location = _a.location;
            var newQuery = __assign(__assign({}, location.query), { display: value });
            router.push({
                pathname: location.pathname,
                query: newQuery,
            });
        };
        _this.generateTagUrl = function (key, value) {
            var organization = _this.props.organization;
            var eventView = _this.state.eventView;
            var url = eventView.getResultsViewUrlTarget(organization.slug);
            url.query = generateQueryWithTag(url.query, {
                key: key,
                value: value,
            });
            return url;
        };
        _this.setError = function (error, errorCode) {
            _this.setState({ error: error, errorCode: errorCode });
        };
        return _this;
    }
    Results.getDerivedStateFromProps = function (nextProps, prevState) {
        var eventView = EventView.fromLocation(nextProps.location);
        return __assign(__assign({}, prevState), { eventView: eventView });
    };
    Results.prototype.componentDidMount = function () {
        var _a = this.props, api = _a.api, organization = _a.organization, selection = _a.selection;
        loadOrganizationTags(api, organization.slug, selection);
        this.checkEventView();
        this.fetchTotalCount();
    };
    Results.prototype.componentDidUpdate = function (prevProps, prevState) {
        var _a = this.props, api = _a.api, location = _a.location, organization = _a.organization, selection = _a.selection;
        var eventView = this.state.eventView;
        if (!isEqual(prevProps.selection.projects, selection.projects) ||
            !isEqual(prevProps.selection.datetime, selection.datetime)) {
            loadOrganizationTags(api, organization.slug, selection);
        }
        this.checkEventView();
        var currentQuery = eventView.getEventsAPIPayload(location);
        var prevQuery = prevState.eventView.getEventsAPIPayload(prevProps.location);
        if (!isAPIPayloadSimilar(currentQuery, prevQuery)) {
            this.fetchTotalCount();
        }
    };
    Results.prototype.fetchTotalCount = function () {
        return __awaiter(this, void 0, void 0, function () {
            var _a, api, organization, location, eventView, totals, err_1;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.props, api = _a.api, organization = _a.organization, location = _a.location;
                        eventView = this.state.eventView;
                        if (!eventView.isValid()) {
                            return [2 /*return*/];
                        }
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, fetchTotalCount(api, organization.slug, eventView.getEventsAPIPayload(location))];
                    case 2:
                        totals = _b.sent();
                        this.setState({ totalValues: totals });
                        return [3 /*break*/, 4];
                    case 3:
                        err_1 = _b.sent();
                        Sentry.captureException(err_1);
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        });
    };
    Results.prototype.checkEventView = function () {
        var eventView = this.state.eventView;
        if (eventView.isValid()) {
            return;
        }
        // If the view is not valid, redirect to a known valid state.
        var _a = this.props, location = _a.location, organization = _a.organization, selection = _a.selection;
        var nextEventView = EventView.fromNewQueryWithLocation(DEFAULT_EVENT_VIEW, location);
        if (nextEventView.project.length === 0 && selection.projects) {
            nextEventView.project = selection.projects;
        }
        ReactRouter.browserHistory.replace(nextEventView.getResultsViewUrlTarget(organization.slug));
    };
    Results.prototype.getDocumentTitle = function () {
        var eventView = this.state.eventView;
        if (!eventView) {
            return '';
        }
        return generateTitle({ eventView: eventView });
    };
    Results.prototype.renderTagsTable = function () {
        var _a = this.props, organization = _a.organization, location = _a.location;
        var _b = this.state, eventView = _b.eventView, totalValues = _b.totalValues;
        return (<Side>
        <Tags generateUrl={this.generateTagUrl} totalValues={totalValues} eventView={eventView} organization={organization} location={location}/>
      </Side>);
    };
    Results.prototype.renderError = function (error) {
        if (!error) {
            return null;
        }
        return (<Alert type="error" icon="icon-circle-exclamation">
        {error}
      </Alert>);
    };
    Results.prototype.render = function () {
        var _a = this.props, organization = _a.organization, location = _a.location, router = _a.router, api = _a.api;
        var _b = this.state, eventView = _b.eventView, error = _b.error, errorCode = _b.errorCode, totalValues = _b.totalValues, showTags = _b.showTags;
        var query = decodeScalar(location.query.query) || '';
        var title = this.getDocumentTitle();
        return (<SentryDocumentTitle title={title} objSlug={organization.slug}>
        <StyledPageContent>
          <LightWeightNoProjectMessage organization={organization}>
            <ResultsHeader errorCode={errorCode} organization={organization} location={location} eventView={eventView}/>
            <ContentBox>
              <Top>
                {this.renderError(error)}
                <StyledSearchBar organization={organization} projectIds={eventView.project} query={query} fields={eventView.fields} onSearch={this.handleSearch}/>
                <ResultsChart api={api} router={router} organization={organization} eventView={eventView} location={location} onAxisChange={this.handleYAxisChange} onDisplayChange={this.handleDisplayChange} total={totalValues}/>
              </Top>
              <StyledMain isCollapsed={!!showTags}>
                <Table organization={organization} eventView={eventView} location={location} title={title} setError={this.setError} onChangeShowTags={this.handleChangeShowTags} showTags={showTags}/>
              </StyledMain>
              {showTags ? this.renderTagsTable() : null}
            </ContentBox>
          </LightWeightNoProjectMessage>
        </StyledPageContent>
      </SentryDocumentTitle>);
    };
    return Results;
}(React.Component));
// These styled components are used in getsentry to create a paywall page.
// Be careful changing their interfaces.
export var StyledPageContent = styled(PageContent)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  padding: 0;\n"], ["\n  padding: 0;\n"])));
export var StyledSearchBar = styled(SearchBar)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space(2));
export var Top = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  grid-column: 1/3;\n  flex-grow: 0;\n"], ["\n  grid-column: 1/3;\n  flex-grow: 0;\n"])));
export var StyledMain = styled(Main)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  grid-column: ", ";\n"], ["\n  grid-column: ", ";\n"])), function (p) { return (p.isCollapsed ? '1/2' : '1/3'); });
function ResultsContainer(props) {
    /**
     * Block `<Results>` from mounting until GSH is ready since there are API
     * requests being performed on mount.
     *
     * Also, we skip loading last used projects if you have multiple projects feature as
     * you no longer need to enforce a project if it is empty. We assume an empty project is
     * the desired behavior because saved queries can contain a project filter.
     */
    return (<GlobalSelectionHeader skipLoadLastUsed={props.organization.features.includes('global-views')}>
      <Results {...props}/>
    </GlobalSelectionHeader>);
}
export default withApi(withOrganization(withGlobalSelection(ResultsContainer)));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=results.jsx.map