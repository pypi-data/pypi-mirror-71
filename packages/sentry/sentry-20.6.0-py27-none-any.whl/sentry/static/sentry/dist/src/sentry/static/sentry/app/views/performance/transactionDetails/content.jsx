import { __assign, __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import PropTypes from 'prop-types';
import { t } from 'app/locale';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import withApi from 'app/utils/withApi';
import SentryTypes from 'app/sentryTypes';
import EventMetadata from 'app/components/events/eventMetadata';
import { BorderlessEventEntries } from 'app/components/events/eventEntries';
import Button from 'app/components/button';
import LoadingError from 'app/components/loadingError';
import NotFound from 'app/components/errors/notFound';
import AsyncComponent from 'app/components/asyncComponent';
import SentryDocumentTitle from 'app/components/sentryDocumentTitle';
import OpsBreakdown from 'app/components/events/opsBreakdown';
import TagsTable from 'app/components/tagsTable';
import Projects from 'app/utils/projects';
import { ContentBox, HeaderBox, HeaderBottomControls } from 'app/utils/discover/styles';
import Breadcrumb from 'app/views/performance/breadcrumb';
import EventView from 'app/utils/discover/eventView';
import { decodeScalar, appendTagCondition } from 'app/utils/queryString';
import { transactionSummaryRouteWithQuery } from '../transactionSummary/utils';
var EventDetailsContent = /** @class */ (function (_super) {
    __extends(EventDetailsContent, _super);
    function EventDetailsContent() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            // AsyncComponent state
            loading: true,
            reloading: false,
            error: false,
            errors: [],
            event: undefined,
            // local state
            isSidebarVisible: true,
        };
        _this.toggleSidebar = function () {
            _this.setState({ isSidebarVisible: !_this.state.isSidebarVisible });
        };
        _this.generateTagUrl = function (tag) {
            var _a = _this.props, location = _a.location, organization = _a.organization;
            var event = _this.state.event;
            if (!event) {
                return '';
            }
            var query = decodeScalar(location.query.query) || '';
            var newQuery = __assign(__assign({}, location.query), { query: appendTagCondition(query, tag.key, tag.value) });
            return transactionSummaryRouteWithQuery({
                orgSlug: organization.slug,
                transaction: event.title,
                projectID: decodeScalar(location.query.project),
                query: newQuery,
            });
        };
        return _this;
    }
    EventDetailsContent.prototype.getEndpoints = function () {
        var _a = this.props, organization = _a.organization, params = _a.params;
        var eventSlug = params.eventSlug;
        var url = "/organizations/" + organization.slug + "/events/" + eventSlug + "/";
        return [['event', url]];
    };
    Object.defineProperty(EventDetailsContent.prototype, "projectId", {
        get: function () {
            return this.props.eventSlug.split(':')[0];
        },
        enumerable: true,
        configurable: true
    });
    EventDetailsContent.prototype.renderBody = function () {
        var event = this.state.event;
        if (!event) {
            return this.renderWrapper(<NotFound />);
        }
        return this.renderWrapper(this.renderContent(event));
    };
    EventDetailsContent.prototype.renderContent = function (event) {
        var _a = this.props, api = _a.api, organization = _a.organization, location = _a.location, eventSlug = _a.eventSlug;
        // metrics
        trackAnalyticsEvent({
            eventKey: 'performance.event_details',
            eventName: 'Performance: Opened Event Details',
            event_type: event.type,
            organization_id: parseInt(organization.id, 10),
        });
        var isSidebarVisible = this.state.isSidebarVisible;
        var transactionName = event.title;
        var query = decodeScalar(location.query.query) || '';
        // Build a new event view so span details links will go to useful results.
        var eventView = EventView.fromNewQueryWithLocation({
            id: undefined,
            name: 'Related events',
            fields: [
                'transaction',
                'project',
                'trace.span',
                'transaction.duration',
                'timestamp',
            ],
            orderby: '-timestamp',
            version: 2,
            projects: [],
            query: appendTagCondition(query, 'transaction', transactionName),
        }, location);
        return (<React.Fragment>
        <HeaderBox>
          <Breadcrumb organization={organization} location={location} transactionName={transactionName} eventSlug={eventSlug}/>
          <StyledTitle data-test-id="event-header">{event.title}</StyledTitle>
          <HeaderBottomControls>
            <StyledButton size="small" onClick={this.toggleSidebar}>
              {isSidebarVisible ? 'Hide Details' : 'Show Details'}
            </StyledButton>
          </HeaderBottomControls>
        </HeaderBox>
        <ContentBox>
          <div style={{ gridColumn: isSidebarVisible ? '1/2' : '1/3' }}>
            <Projects orgId={organization.slug} slugs={[this.projectId]}>
              {function (_a) {
            var projects = _a.projects;
            return (<BorderlessEventEntries api={api} organization={organization} event={event} project={projects[0]} location={location} showExampleCommit={false} showTagSummary={false} eventView={eventView}/>);
        }}
            </Projects>
          </div>
          <div style={{ gridColumn: '2/3', display: isSidebarVisible ? '' : 'none' }}>
            <EventMetadata event={event} organization={organization} projectId={this.projectId}/>
            <OpsBreakdown event={event}/>
            <TagsTable event={event} query={query} generateUrl={this.generateTagUrl}/>
          </div>
        </ContentBox>
      </React.Fragment>);
    };
    EventDetailsContent.prototype.renderError = function (error) {
        var notFound = Object.values(this.state.errors).find(function (resp) { return resp && resp.status === 404; });
        var permissionDenied = Object.values(this.state.errors).find(function (resp) { return resp && resp.status === 403; });
        if (notFound) {
            return this.renderWrapper(<NotFound />);
        }
        if (permissionDenied) {
            return this.renderWrapper(<LoadingError message={t('You do not have permission to view that event.')}/>);
        }
        return this.renderWrapper(_super.prototype.renderError.call(this, error, true, true));
    };
    EventDetailsContent.prototype.renderLoading = function () {
        return this.renderWrapper(_super.prototype.renderLoading.call(this));
    };
    EventDetailsContent.prototype.renderWrapper = function (children) {
        var organization = this.props.organization;
        return (<SentryDocumentTitle title={t('Performance - Event Details')} objSlug={organization.slug}>
        <React.Fragment>{children}</React.Fragment>
      </SentryDocumentTitle>);
    };
    EventDetailsContent.propTypes = {
        organization: SentryTypes.Organization.isRequired,
        eventSlug: PropTypes.string.isRequired,
        location: PropTypes.object.isRequired,
    };
    return EventDetailsContent;
}(AsyncComponent));
var StyledButton = styled(Button)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: none;\n\n  @media (min-width: ", ") {\n    display: block;\n    width: 110px;\n  }\n"], ["\n  display: none;\n\n  @media (min-width: ", ") {\n    display: block;\n    width: 110px;\n  }\n"])), function (p) { return p.theme.breakpoints[1]; });
var StyledTitle = styled('span')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  color: ", ";\n  font-size: ", ";\n  grid-column: 1 / 2;\n"], ["\n  color: ", ";\n  font-size: ", ";\n  grid-column: 1 / 2;\n"])), function (p) { return p.theme.gray700; }, function (p) { return p.theme.headerFontSize; });
export default withApi(EventDetailsContent);
var templateObject_1, templateObject_2;
//# sourceMappingURL=content.jsx.map