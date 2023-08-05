import { __assign, __awaiter, __extends, __generator, __makeTemplateObject } from "tslib";
import React from 'react';
import { browserHistory } from 'react-router';
import styled from '@emotion/styled';
import * as Sentry from '@sentry/browser';
import isEqual from 'lodash/isEqual';
import { t } from 'app/locale';
import { fetchTotalCount } from 'app/actionCreators/events';
import { loadOrganizationTags } from 'app/actionCreators/tags';
import SentryDocumentTitle from 'app/components/sentryDocumentTitle';
import GlobalSelectionHeader from 'app/components/organizations/globalSelectionHeader';
import { PageContent } from 'app/styles/organization';
import EventView, { isAPIPayloadSimilar } from 'app/utils/discover/eventView';
import { isAggregateField } from 'app/utils/discover/fields';
import { decodeScalar } from 'app/utils/queryString';
import { tokenizeSearch, stringifyQueryObject } from 'app/utils/tokenizeSearch';
import LightWeightNoProjectMessage from 'app/components/lightWeightNoProjectMessage';
import withApi from 'app/utils/withApi';
import withGlobalSelection from 'app/utils/withGlobalSelection';
import withOrganization from 'app/utils/withOrganization';
import withProjects from 'app/utils/withProjects';
import SummaryContent from './content';
var TransactionSummary = /** @class */ (function (_super) {
    __extends(TransactionSummary, _super);
    function TransactionSummary() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            eventView: generateSummaryEventView(_this.props.location, getTransactionName(_this.props)),
            totalValues: null,
        };
        return _this;
    }
    TransactionSummary.getDerivedStateFromProps = function (nextProps, prevState) {
        return __assign(__assign({}, prevState), { eventView: generateSummaryEventView(nextProps.location, getTransactionName(nextProps)) });
    };
    TransactionSummary.prototype.componentDidMount = function () {
        var _a = this.props, api = _a.api, organization = _a.organization, selection = _a.selection;
        this.fetchTotalCount();
        loadOrganizationTags(api, organization.slug, selection);
    };
    TransactionSummary.prototype.componentDidUpdate = function (prevProps, prevState) {
        var _a = this.props, api = _a.api, organization = _a.organization, location = _a.location, selection = _a.selection;
        var eventView = this.state.eventView;
        if (eventView && prevState.eventView) {
            var currentQuery = eventView.getEventsAPIPayload(location);
            var prevQuery = prevState.eventView.getEventsAPIPayload(prevProps.location);
            if (!isAPIPayloadSimilar(currentQuery, prevQuery)) {
                this.fetchTotalCount();
            }
        }
        if (!isEqual(prevProps.selection.projects, selection.projects) ||
            !isEqual(prevProps.selection.datetime, selection.datetime)) {
            loadOrganizationTags(api, organization.slug, selection);
        }
    };
    TransactionSummary.prototype.fetchTotalCount = function () {
        return __awaiter(this, void 0, void 0, function () {
            var _a, api, organization, location, eventView, totals, err_1;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.props, api = _a.api, organization = _a.organization, location = _a.location;
                        eventView = this.state.eventView;
                        if (!eventView || !eventView.isValid()) {
                            return [2 /*return*/];
                        }
                        this.setState({ totalValues: null });
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
    TransactionSummary.prototype.getDocumentTitle = function () {
        var name = getTransactionName(this.props);
        var hasTransactionName = typeof name === 'string' && String(name).trim().length > 0;
        if (hasTransactionName) {
            return [String(name).trim(), t('Performance')].join(' - ');
        }
        return [t('Summary'), t('Performance')].join(' - ');
    };
    TransactionSummary.prototype.render = function () {
        var _a = this.props, organization = _a.organization, location = _a.location;
        var _b = this.state, eventView = _b.eventView, totalValues = _b.totalValues;
        var transactionName = getTransactionName(this.props);
        if (!eventView || transactionName === undefined) {
            // If there is no transaction name, redirect to the Performance landing page
            browserHistory.replace({
                pathname: "/organizations/" + organization.slug + "/performance/",
                query: __assign({}, location.query),
            });
            return null;
        }
        return (<SentryDocumentTitle title={this.getDocumentTitle()} objSlug={organization.slug}>
        <GlobalSelectionHeader>
          <StyledPageContent>
            <LightWeightNoProjectMessage organization={organization}>
              <SummaryContent location={location} organization={organization} eventView={eventView} transactionName={transactionName} totalValues={totalValues}/>
            </LightWeightNoProjectMessage>
          </StyledPageContent>
        </GlobalSelectionHeader>
      </SentryDocumentTitle>);
    };
    return TransactionSummary;
}(React.Component));
var StyledPageContent = styled(PageContent)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  padding: 0;\n"], ["\n  padding: 0;\n"])));
function getTransactionName(props) {
    var location = props.location;
    var transaction = location.query.transaction;
    return decodeScalar(transaction);
}
function generateSummaryEventView(location, transactionName) {
    if (transactionName === undefined) {
        return undefined;
    }
    // Use the user supplied query but overwrite any transaction or event type
    // conditions they applied.
    var query = decodeScalar(location.query.query) || '';
    var conditions = Object.assign(tokenizeSearch(query), {
        'event.type': ['transaction'],
        transaction: [transactionName],
    });
    Object.keys(conditions).forEach(function (field) {
        if (isAggregateField(field))
            delete conditions[field];
    });
    // Handle duration filters from the latency chart
    if (location.query.startDuration || location.query.endDuration) {
        conditions['transaction.duration'] = [
            decodeScalar(location.query.startDuration),
            decodeScalar(location.query.endDuration),
        ]
            .filter(function (item) { return item; })
            .map(function (item, index) { return (index === 0 ? ">" + item : "<" + item); });
    }
    return EventView.fromNewQueryWithLocation({
        id: undefined,
        version: 2,
        name: transactionName,
        fields: ['id', 'user', 'transaction.duration', 'timestamp'],
        query: stringifyQueryObject(conditions),
        projects: [],
    }, location);
}
export default withApi(withGlobalSelection(withProjects(withOrganization(TransactionSummary))));
var templateObject_1;
//# sourceMappingURL=index.jsx.map