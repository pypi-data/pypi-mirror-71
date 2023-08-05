import { __assign, __extends, __makeTemplateObject } from "tslib";
import PropTypes from 'prop-types';
import React from 'react';
import * as ReactRouter from 'react-router';
import isEqual from 'lodash/isEqual';
import pick from 'lodash/pick';
import styled from '@emotion/styled';
import { PageContent } from 'app/styles/organization';
import { t } from 'app/locale';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import Alert from 'app/components/alert';
import AsyncComponent from 'app/components/asyncComponent';
import Banner from 'app/components/banner';
import Button from 'app/components/button';
import DropdownControl, { DropdownItem } from 'app/components/dropdownControl';
import ConfigStore from 'app/stores/configStore';
import Feature from 'app/components/acl/feature';
import LightWeightNoProjectMessage from 'app/components/lightWeightNoProjectMessage';
import SearchBar from 'app/components/searchBar';
import SentryDocumentTitle from 'app/components/sentryDocumentTitle';
import SentryTypes from 'app/sentryTypes';
import localStorage from 'app/utils/localStorage';
import space from 'app/styles/space';
import withOrganization from 'app/utils/withOrganization';
import EventView from 'app/utils/discover/eventView';
import { decodeScalar } from 'app/utils/queryString';
import { DEFAULT_EVENT_VIEW } from './data';
import { getPrebuiltQueries } from './utils';
import QueryList from './queryList';
import backgroundSpace from '../../../images/spot/background-space.svg';
var BANNER_DISMISSED_KEY = 'discover-banner-dismissed';
var SORT_OPTIONS = [
    { label: t('Recently Edited'), value: '-dateUpdated' },
    { label: t('My Queries'), value: 'myqueries' },
    { label: t('Query Name (A-Z)'), value: 'name' },
    { label: t('Date Created (Newest)'), value: '-dateCreated' },
    { label: t('Date Created (Oldest)'), value: 'dateCreated' },
    { label: t('Most Outdated'), value: 'dateUpdated' },
];
function checkIsBannerHidden() {
    return localStorage.getItem(BANNER_DISMISSED_KEY) === 'true';
}
var DiscoverLanding = /** @class */ (function (_super) {
    __extends(DiscoverLanding, _super);
    function DiscoverLanding() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            // AsyncComponent state
            loading: true,
            reloading: false,
            error: false,
            errors: [],
            // local component state
            isBannerHidden: checkIsBannerHidden(),
            savedQueries: [],
            savedQueriesPageLinks: '',
        };
        _this.shouldReload = true;
        _this.handleQueryChange = function () {
            _this.fetchData({ reloading: true });
        };
        _this.handleClick = function () {
            localStorage.setItem(BANNER_DISMISSED_KEY, 'true');
            _this.setState({ isBannerHidden: true });
        };
        _this.handleSearchQuery = function (searchQuery) {
            var location = _this.props.location;
            ReactRouter.browserHistory.push({
                pathname: location.pathname,
                query: __assign(__assign({}, location.query), { cursor: undefined, query: String(searchQuery).trim() || undefined }),
            });
        };
        _this.handleSortChange = function (value) {
            var location = _this.props.location;
            ReactRouter.browserHistory.push({
                pathname: location.pathname,
                query: __assign(__assign({}, location.query), { cursor: undefined, sort: value }),
            });
        };
        _this.onGoLegacyDiscover = function () {
            localStorage.setItem('discover:version', '1');
            var user = ConfigStore.get('user');
            trackAnalyticsEvent({
                eventKey: 'discover_v2.opt_out',
                eventName: 'Discoverv2: Go to discover',
                organization_id: parseInt(_this.props.organization.id, 10),
                user_id: parseInt(user.id, 10),
            });
        };
        return _this;
    }
    DiscoverLanding.prototype.getSavedQuerySearchQuery = function () {
        var location = this.props.location;
        return String(decodeScalar(location.query.query) || '').trim();
    };
    DiscoverLanding.prototype.getActiveSort = function () {
        var location = this.props.location;
        var urlSort = location.query.sort
            ? decodeScalar(location.query.sort)
            : '-dateUpdated';
        return SORT_OPTIONS.find(function (item) { return item.value === urlSort; }) || SORT_OPTIONS[0];
    };
    DiscoverLanding.prototype.getEndpoints = function () {
        var _a = this.props, organization = _a.organization, location = _a.location;
        var views = getPrebuiltQueries(organization);
        var searchQuery = this.getSavedQuerySearchQuery();
        var cursor = decodeScalar(location.query.cursor);
        var perPage = 9;
        if (!cursor) {
            // invariant: we're on the first page
            if (searchQuery && searchQuery.length > 0) {
                var needleSearch_1 = searchQuery.toLowerCase();
                var numOfPrebuiltQueries = views.reduce(function (sum, view) {
                    var eventView = EventView.fromNewQueryWithLocation(view, location);
                    // if a search is performed on the list of queries, we filter
                    // on the pre-built queries
                    if (eventView.name && eventView.name.toLowerCase().includes(needleSearch_1)) {
                        return sum + 1;
                    }
                    return sum;
                }, 0);
                perPage = Math.max(1, perPage - numOfPrebuiltQueries);
            }
            else {
                perPage = Math.max(1, perPage - views.length);
            }
        }
        var queryParams = {
            cursor: cursor,
            query: "version:2 name:\"" + searchQuery + "\"",
            per_page: perPage,
            sortBy: this.getActiveSort().value,
        };
        if (!cursor) {
            delete queryParams.cursor;
        }
        return [
            [
                'savedQueries',
                "/organizations/" + organization.slug + "/discover/saved/",
                {
                    query: queryParams,
                },
            ],
        ];
    };
    DiscoverLanding.prototype.componentDidUpdate = function (prevProps) {
        var isBannerHidden = checkIsBannerHidden();
        if (isBannerHidden !== this.state.isBannerHidden) {
            // eslint-disable-next-line react/no-did-update-set-state
            this.setState({
                isBannerHidden: isBannerHidden,
            });
        }
        var PAYLOAD_KEYS = ['sort', 'cursor', 'query'];
        var payloadKeysChanged = !isEqual(pick(prevProps.location.query, PAYLOAD_KEYS), pick(this.props.location.query, PAYLOAD_KEYS));
        // if any of the query strings relevant for the payload has changed,
        // we re-fetch data
        if (payloadKeysChanged) {
            this.fetchData();
        }
    };
    DiscoverLanding.prototype.renderBanner = function () {
        var _this = this;
        var bannerDismissed = this.state.isBannerHidden;
        if (bannerDismissed) {
            return null;
        }
        var _a = this.props, location = _a.location, organization = _a.organization;
        var eventView = EventView.fromNewQueryWithLocation(DEFAULT_EVENT_VIEW, location);
        var to = eventView.getResultsViewUrlTarget(organization.slug);
        return (<Banner title={t('Discover Trends')} subtitle={t('Customize and save queries by search conditions, event fields, and tags')} backgroundImg={backgroundSpace} onCloseClick={this.handleClick}>
        <StarterButton to={to} onClick={function () {
            trackAnalyticsEvent({
                eventKey: 'discover_v2.build_new_query',
                eventName: 'Discoverv2: Build a new Discover Query',
                organization_id: parseInt(_this.props.organization.id, 10),
            });
        }}>
          {t('Build a new query')}
        </StarterButton>
        <StarterButton href="https://docs.sentry.io/performance/discover/">
          {t('Read the docs')}
        </StarterButton>
      </Banner>);
    };
    DiscoverLanding.prototype.renderActions = function () {
        var _this = this;
        var activeSort = this.getActiveSort();
        return (<StyledActions>
        <StyledSearchBar defaultQuery="" query={this.getSavedQuerySearchQuery()} placeholder={t('Search saved queries')} onSearch={this.handleSearchQuery}/>
        <DropdownControl buttonProps={{ prefix: t('Sort By') }} label={activeSort.label}>
          {SORT_OPTIONS.map(function (_a) {
            var label = _a.label, value = _a.value;
            return (<DropdownItem key={value} onSelect={_this.handleSortChange} eventKey={value} isActive={value === activeSort.value}>
              {label}
            </DropdownItem>);
        })}
        </DropdownControl>
      </StyledActions>);
    };
    DiscoverLanding.prototype.renderNoAccess = function () {
        return (<PageContent>
        <Alert type="warning">{t("You don't have access to this feature")}</Alert>
      </PageContent>);
    };
    DiscoverLanding.prototype.renderBody = function () {
        var _a = this.props, location = _a.location, organization = _a.organization;
        var _b = this.state, savedQueries = _b.savedQueries, savedQueriesPageLinks = _b.savedQueriesPageLinks;
        return (<QueryList pageLinks={savedQueriesPageLinks} savedQueries={savedQueries} savedQuerySearchQuery={this.getSavedQuerySearchQuery()} location={location} organization={organization} onQueryChange={this.handleQueryChange}/>);
    };
    DiscoverLanding.prototype.render = function () {
        var _this = this;
        var _a = this.props, location = _a.location, organization = _a.organization;
        var eventView = EventView.fromNewQueryWithLocation(DEFAULT_EVENT_VIEW, location);
        var to = eventView.getResultsViewUrlTarget(organization.slug);
        return (<Feature organization={organization} features={['discover-query']} renderDisabled={this.renderNoAccess}>
        <SentryDocumentTitle title={t('Discover')} objSlug={organization.slug}>
          <StyledPageContent>
            <LightWeightNoProjectMessage organization={organization}>
              <PageContent>
                <StyledPageHeader>
                  {t('Discover')}
                  <StyledButton data-test-id="build-new-query" to={to} priority="primary" onClick={function () {
            trackAnalyticsEvent({
                eventKey: 'discover_v2.build_new_query',
                eventName: 'Discoverv2: Build a new Discover Query',
                organization_id: parseInt(_this.props.organization.id, 10),
            });
        }}>
                    {t('Build a new query')}
                  </StyledButton>
                </StyledPageHeader>
                {this.renderBanner()}
                {this.renderActions()}
                {this.renderComponent()}
                <Feature features={['organizations:discover']} organization={organization}>
                  <div>
                    <SwitchLink href={"/organizations/" + organization.slug + "/discover/"} onClick={this.onGoLegacyDiscover}>
                      {t('Go to Legacy Discover')}
                    </SwitchLink>
                  </div>
                </Feature>
              </PageContent>
            </LightWeightNoProjectMessage>
          </StyledPageContent>
        </SentryDocumentTitle>
      </Feature>);
    };
    DiscoverLanding.propTypes = {
        organization: SentryTypes.Organization.isRequired,
        location: PropTypes.object.isRequired,
        router: PropTypes.object.isRequired,
    };
    return DiscoverLanding;
}(AsyncComponent));
var StyledPageContent = styled(PageContent)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  padding: 0;\n"], ["\n  padding: 0;\n"])));
export var StyledPageHeader = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  align-items: flex-end;\n  font-size: ", ";\n  color: ", ";\n  justify-content: space-between;\n  margin-bottom: ", ";\n"], ["\n  display: flex;\n  align-items: flex-end;\n  font-size: ", ";\n  color: ", ";\n  justify-content: space-between;\n  margin-bottom: ", ";\n"])), function (p) { return p.theme.headerFontSize; }, function (p) { return p.theme.gray800; }, space(2));
var StyledSearchBar = styled(SearchBar)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  flex-grow: 1;\n"], ["\n  flex-grow: 1;\n"])));
var StyledActions = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n  grid-template-columns: auto min-content;\n\n  align-items: center;\n  margin-bottom: ", ";\n"], ["\n  display: grid;\n  grid-gap: ", ";\n  grid-template-columns: auto min-content;\n\n  align-items: center;\n  margin-bottom: ", ";\n"])), space(2), space(3));
var StyledButton = styled(Button)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  white-space: nowrap;\n"], ["\n  white-space: nowrap;\n"])));
var StarterButton = styled(Button)(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  margin: ", ";\n"], ["\n  margin: ", ";\n"])), space(1));
var SwitchLink = styled('a')(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  font-size: ", ";\n  margin-left: ", ";\n"], ["\n  font-size: ", ";\n  margin-left: ", ";\n"])), function (p) { return p.theme.fontSizeSmall; }, space(1));
export default withOrganization(DiscoverLanding);
export { DiscoverLanding };
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7;
//# sourceMappingURL=landing.jsx.map