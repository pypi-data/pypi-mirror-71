import { __assign, __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import PropTypes from 'prop-types';
import { BorderlessEventEntries } from 'app/components/events/eventEntries';
import space from 'app/styles/space';
import overflowEllipsis from 'app/styles/overflowEllipsis';
import { t } from 'app/locale';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import withApi from 'app/utils/withApi';
import { getMessage, getTitle } from 'app/utils/events';
import SentryTypes from 'app/sentryTypes';
import getDynamicText from 'app/utils/getDynamicText';
import Button from 'app/components/button';
import OpsBreakdown from 'app/components/events/opsBreakdown';
import EventMetadata from 'app/components/events/eventMetadata';
import LoadingError from 'app/components/loadingError';
import NotFound from 'app/components/errors/notFound';
import TagsTable from 'app/components/tagsTable';
import AsyncComponent from 'app/components/asyncComponent';
import SentryDocumentTitle from 'app/components/sentryDocumentTitle';
import Projects from 'app/utils/projects';
import { ContentBox, HeaderBox, HeaderBottomControls } from 'app/utils/discover/styles';
import { generateTitle, getExpandedResults } from '../utils';
import Pagination from './pagination';
import LineGraph from './lineGraph';
import LinkedIssue from './linkedIssue';
import DiscoverBreadcrumb from '../breadcrumb';
var slugValidator = function (props, propName, componentName) {
    var value = props[propName];
    // Accept slugs that look like:
    // * project-slug:deadbeef
    if (value && typeof value === 'string' && !/^(?:[^:]+):(?:[a-f0-9-]+)$/.test(value)) {
        return new Error("Invalid value for " + propName + " provided to " + componentName + ".");
    }
    return null;
};
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
            var _a;
            var _b = _this.props, eventView = _b.eventView, organization = _b.organization;
            var event = _this.state.event;
            if (!event) {
                return '';
            }
            var eventReference = __assign({}, event);
            if (eventReference.id) {
                delete eventReference.id;
            }
            var nextView = getExpandedResults(eventView, (_a = {}, _a[tag.key] = tag.value, _a), eventReference);
            return nextView.getResultsViewUrlTarget(organization.slug);
        };
        return _this;
    }
    EventDetailsContent.prototype.getEndpoints = function () {
        var _a = this.props, organization = _a.organization, params = _a.params, location = _a.location, eventView = _a.eventView;
        var eventSlug = params.eventSlug;
        var query = eventView.getEventsAPIPayload(location);
        var url = "/organizations/" + organization.slug + "/events/" + eventSlug + "/";
        // Get a specific event. This could be coming from
        // a paginated group or standalone event.
        return [['event', url, { query: query }]];
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
        var _a = this.props, api = _a.api, organization = _a.organization, location = _a.location, eventView = _a.eventView;
        // metrics
        trackAnalyticsEvent({
            eventKey: 'discover_v2.event_details',
            eventName: 'Discoverv2: Opened Event Details',
            event_type: event.type,
            organization_id: parseInt(organization.id, 10),
        });
        // Having an aggregate field means we want to show pagination/graphs
        var isGroupedView = eventView.hasAggregateField();
        var isSidebarVisible = this.state.isSidebarVisible;
        return (<React.Fragment>
        <HeaderBox>
          <DiscoverBreadcrumb eventView={eventView} event={event} organization={organization} location={location}/>
          <EventHeader event={event}/>
          <HeaderBottomControls>
            <StyledButton size="small" onClick={this.toggleSidebar}>
              {isSidebarVisible ? 'Hide Details' : 'Show Details'}
            </StyledButton>
            {isGroupedView && (<Pagination event={event} organization={organization} eventView={eventView}/>)}
          </HeaderBottomControls>
        </HeaderBox>
        <ContentBox>
          <div style={{ gridColumn: isSidebarVisible ? '1/2' : '1/3' }}>
            {isGroupedView &&
            getDynamicText({
                value: (<LineGraph organization={organization} currentEvent={event} location={location} eventView={eventView}/>),
                fixed: 'events chart',
            })}
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
            {event.groupID && (<LinkedIssue groupId={event.groupID} eventId={event.eventID}/>)}
            <TagsTable generateUrl={this.generateTagUrl} event={event} query={eventView.query}/>
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
        var _a = this.props, organization = _a.organization, location = _a.location, eventView = _a.eventView;
        var event = this.state.event;
        return (<EventDetailsWrapper organization={organization} location={location} eventView={eventView} event={event}>
        {children}
      </EventDetailsWrapper>);
    };
    EventDetailsContent.propTypes = {
        organization: SentryTypes.Organization.isRequired,
        eventSlug: slugValidator,
        location: PropTypes.object.isRequired,
    };
    return EventDetailsContent;
}(AsyncComponent));
var EventDetailsWrapper = /** @class */ (function (_super) {
    __extends(EventDetailsWrapper, _super);
    function EventDetailsWrapper() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.getDocumentTitle = function () {
            var _a = _this.props, event = _a.event, eventView = _a.eventView;
            return generateTitle({
                eventView: eventView,
                event: event,
            });
        };
        return _this;
    }
    EventDetailsWrapper.prototype.render = function () {
        var _a = this.props, organization = _a.organization, children = _a.children;
        return (<SentryDocumentTitle title={this.getDocumentTitle()} objSlug={organization.slug}>
        <React.Fragment>{children}</React.Fragment>
      </SentryDocumentTitle>);
    };
    return EventDetailsWrapper;
}(React.Component));
var EventHeader = function (props) {
    var title = getTitle(props.event).title;
    var message = getMessage(props.event);
    return (<StyledEventHeader data-test-id="event-header">
      <StyledTitle>
        {title}
        {message && message.length > 0 ? ':' : null}
      </StyledTitle>
      <span>{getMessage(props.event)}</span>
    </StyledEventHeader>);
};
var StyledButton = styled(Button)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: none;\n\n  @media (min-width: ", ") {\n    display: block;\n    width: 110px;\n  }\n"], ["\n  display: none;\n\n  @media (min-width: ", ") {\n    display: block;\n    width: 110px;\n  }\n"])), function (p) { return p.theme.breakpoints[1]; });
var StyledEventHeader = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  font-size: ", ";\n  color: ", ";\n  grid-column: 1/2;\n  align-self: center;\n  ", ";\n"], ["\n  font-size: ", ";\n  color: ", ";\n  grid-column: 1/2;\n  align-self: center;\n  ", ";\n"])), function (p) { return p.theme.headerFontSize; }, function (p) { return p.theme.gray500; }, overflowEllipsis);
var StyledTitle = styled('span')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  color: ", ";\n  margin-right: ", ";\n  align-self: center;\n"], ["\n  color: ", ";\n  margin-right: ", ";\n  align-self: center;\n"])), function (p) { return p.theme.gray700; }, space(1));
export default withApi(EventDetailsContent);
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=content.jsx.map