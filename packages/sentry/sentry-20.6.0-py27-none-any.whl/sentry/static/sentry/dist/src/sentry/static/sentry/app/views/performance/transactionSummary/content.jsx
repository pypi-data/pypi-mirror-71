import { __assign, __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import { browserHistory } from 'react-router';
import styled from '@emotion/styled';
import omit from 'lodash/omit';
import { getParams } from 'app/components/organizations/globalSelectionHeader/getParams';
import overflowEllipsis from 'app/styles/overflowEllipsis';
import space from 'app/styles/space';
import { generateQueryWithTag } from 'app/utils';
import { ContentBox, HeaderBox, Main, Side } from 'app/utils/discover/styles';
import Tags from 'app/views/eventsV2/tags';
import SearchBar from 'app/views/events/searchBar';
import { decodeScalar } from 'app/utils/queryString';
import TransactionList from './transactionList';
import UserStats from './userStats';
import KeyTransactionButton from './keyTransactionButton';
import TransactionSummaryCharts from './charts';
import RelatedIssues from './relatedIssues';
import SidebarCharts from './sidebarCharts';
import Breadcrumb from '../breadcrumb';
var SummaryContent = /** @class */ (function (_super) {
    __extends(SummaryContent, _super);
    function SummaryContent() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleSearch = function (query) {
            var location = _this.props.location;
            var queryParams = getParams(__assign(__assign({}, (location.query || {})), { query: query }));
            // do not propagate pagination when making a new search
            var searchQueryParams = omit(queryParams, 'cursor');
            browserHistory.push({
                pathname: location.pathname,
                query: searchQueryParams,
            });
        };
        _this.generateTagUrl = function (key, value) {
            var location = _this.props.location;
            var query = generateQueryWithTag(location.query, { key: key, value: value });
            return __assign(__assign({}, location), { query: query });
        };
        return _this;
    }
    SummaryContent.prototype.renderKeyTransactionButton = function () {
        var _a = this.props, eventView = _a.eventView, organization = _a.organization, transactionName = _a.transactionName;
        return (<KeyTransactionButton transactionName={transactionName} eventView={eventView} organization={organization}/>);
    };
    SummaryContent.prototype.render = function () {
        var _a = this.props, transactionName = _a.transactionName, location = _a.location, eventView = _a.eventView, organization = _a.organization, totalValues = _a.totalValues;
        var query = decodeScalar(location.query.query) || '';
        return (<React.Fragment>
        <HeaderBox>
          <div>
            <Breadcrumb organization={organization} location={location} transactionName={transactionName}/>
          </div>
          <KeyTransactionContainer>
            {this.renderKeyTransactionButton()}
          </KeyTransactionContainer>
          <StyledTitleHeader>{transactionName}</StyledTitleHeader>
        </HeaderBox>
        <ContentBox>
          <StyledMain>
            <StyledSearchBar organization={organization} projectIds={eventView.project} query={query} fields={eventView.fields} onSearch={this.handleSearch}/>
            <TransactionSummaryCharts organization={organization} location={location} eventView={eventView} totalValues={totalValues}/>
            <TransactionList organization={organization} transactionName={transactionName} location={location} eventView={eventView}/>
            <RelatedIssues organization={organization} location={location} transaction={transactionName} start={eventView.start} end={eventView.end} statsPeriod={eventView.statsPeriod}/>
          </StyledMain>
          <Side>
            <UserStats organization={organization} location={location} eventView={eventView}/>
            <SidebarCharts organization={organization} eventView={eventView}/>
            <Tags generateUrl={this.generateTagUrl} totalValues={totalValues} eventView={eventView} organization={organization} location={location}/>
          </Side>
        </ContentBox>
      </React.Fragment>);
    };
    return SummaryContent;
}(React.Component));
var StyledTitleHeader = styled('span')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  font-size: ", ";\n  color: ", ";\n  grid-column: 1/2;\n  align-self: center;\n  min-height: 30px;\n  ", ";\n"], ["\n  font-size: ", ";\n  color: ", ";\n  grid-column: 1/2;\n  align-self: center;\n  min-height: 30px;\n  ", ";\n"])), function (p) { return p.theme.headerFontSize; }, function (p) { return p.theme.gray700; }, overflowEllipsis);
// Allow overflow so chart tooltip and assignee dropdown display.
var StyledMain = styled(Main)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  overflow: visible;\n"], ["\n  overflow: visible;\n"])));
var KeyTransactionContainer = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: flex;\n  justify-content: flex-end;\n"], ["\n  display: flex;\n  justify-content: flex-end;\n"])));
var StyledSearchBar = styled(SearchBar)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space(1));
export default SummaryContent;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=content.jsx.map