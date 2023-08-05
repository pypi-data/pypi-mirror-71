import { __assign, __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { browserHistory } from 'react-router';
import space from 'app/styles/space';
import { t } from 'app/locale';
import DiscoverButton from 'app/components/discoverButton';
import DropdownControl, { DropdownItem } from 'app/components/dropdownControl';
import PanelTable from 'app/components/panels/panelTable';
import Link from 'app/components/links/link';
import HeaderCell from 'app/views/eventsV2/table/headerCell';
import SortLink from 'app/components/gridEditable/sortLink';
import { getFieldRenderer } from 'app/utils/discover/fieldRenderers';
import { getAggregateAlias } from 'app/utils/discover/fields';
import { generateEventSlug } from 'app/utils/discover/urls';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import { decodeScalar } from 'app/utils/queryString';
import DiscoverQuery from 'app/utils/discover/discoverQuery';
import { TOP_TRANSACTION_LIMIT, TOP_TRANSACTION_FILTERS, } from 'app/views/performance/constants';
import { GridBodyCell, GridBodyCellNumber, GridHeadCell } from '../styles';
import { getTransactionDetailsUrl } from '../utils';
var TransactionList = /** @class */ (function (_super) {
    __extends(TransactionList, _super);
    function TransactionList() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleTransactionFilterChange = function (value) {
            var _a = _this.props, location = _a.location, organization = _a.organization;
            trackAnalyticsEvent({
                eventKey: 'performance_views.summary.filter_transactions',
                eventName: 'Performance Views: Filter transactions table',
                organization_id: parseInt(organization.id, 10),
                value: value,
            });
            var target = {
                pathname: location.pathname,
                query: __assign(__assign({}, location.query), { showTransactions: value }),
            };
            browserHistory.push(target);
        };
        _this.handleDiscoverViewClick = function () {
            var organization = _this.props.organization;
            trackAnalyticsEvent({
                eventKey: 'performance_views.summary.view_in_discover',
                eventName: 'Performance Views: View in Discover from Transaction Summary',
                organization_id: parseInt(organization.id, 10),
            });
        };
        return _this;
    }
    TransactionList.prototype.getTransactionSort = function (location) {
        var urlParam = decodeScalar(location.query.showTransactions) || 'slowest';
        var option = TOP_TRANSACTION_FILTERS.find(function (opt) { return opt.value === urlParam; }) ||
            TOP_TRANSACTION_FILTERS[0];
        return option;
    };
    TransactionList.prototype.render = function () {
        var _this = this;
        var _a = this.props, eventView = _a.eventView, location = _a.location, organization = _a.organization, transactionName = _a.transactionName;
        var activeFilter = this.getTransactionSort(location);
        var sortedEventView = eventView.withSorts([activeFilter.sort]);
        return (<React.Fragment>
        <Header>
          <DropdownControl data-test-id="filter-transactions" label={activeFilter.label} buttonProps={{ prefix: t('Filter'), size: 'small' }}>
            {TOP_TRANSACTION_FILTERS.map(function (_a) {
            var value = _a.value, label = _a.label;
            return (<DropdownItem key={value} onSelect={_this.handleTransactionFilterChange} eventKey={value} isActive={value === activeFilter.value}>
                {label}
              </DropdownItem>);
        })}
          </DropdownControl>
          <HeaderButtonContainer>
            <DiscoverButton onClick={this.handleDiscoverViewClick} to={sortedEventView.getResultsViewUrlTarget(organization.slug)} size="small" data-test-id="discover-open">
              {t('Open in Discover')}
            </DiscoverButton>
          </HeaderButtonContainer>
        </Header>
        <DiscoverQuery location={location} eventView={sortedEventView} orgSlug={organization.slug} limit={TOP_TRANSACTION_LIMIT}>
          {function (_a) {
            var isLoading = _a.isLoading, tableData = _a.tableData;
            return (<TransactionTable organization={organization} location={location} transactionName={transactionName} eventView={eventView} tableData={tableData} isLoading={isLoading}/>);
        }}
        </DiscoverQuery>
      </React.Fragment>);
    };
    return TransactionList;
}(React.PureComponent));
var TransactionTable = /** @class */ (function (_super) {
    __extends(TransactionTable, _super);
    function TransactionTable() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleViewDetailsClick = function () {
            var organization = _this.props.organization;
            trackAnalyticsEvent({
                eventKey: 'performance_views.summary.view_details',
                eventName: 'Performance Views: View Details from Transaction Summary',
                organization_id: parseInt(organization.id, 10),
            });
        };
        return _this;
    }
    TransactionTable.prototype.renderHeader = function () {
        var _a = this.props, eventView = _a.eventView, tableData = _a.tableData;
        var tableMeta = tableData === null || tableData === void 0 ? void 0 : tableData.meta;
        var columnOrder = eventView.getColumns();
        var generateSortLink = function () { return undefined; };
        return columnOrder.map(function (column, index) { return (<HeaderCell column={column} tableMeta={tableMeta} key={index}>
        {function (_a) {
            var align = _a.align;
            return (<GridHeadCell>
              <SortLink align={align} title={column.name} direction={undefined} canSort={false} generateSortLink={generateSortLink}/>
            </GridHeadCell>);
        }}
      </HeaderCell>); });
    };
    TransactionTable.prototype.renderResults = function () {
        var _this = this;
        var _a = this.props, isLoading = _a.isLoading, tableData = _a.tableData;
        var cells = [];
        if (isLoading) {
            return cells;
        }
        if (!tableData || !tableData.meta || !tableData.data) {
            return cells;
        }
        var columnOrder = this.props.eventView.getColumns();
        tableData.data.forEach(function (row, i) {
            // Another check to appease tsc
            if (!tableData.meta) {
                return;
            }
            cells = cells.concat(_this.renderRow(row, i, columnOrder, tableData.meta));
        });
        return cells;
    };
    TransactionTable.prototype.renderRow = function (row, rowIndex, columnOrder, tableMeta) {
        var _this = this;
        var _a = this.props, organization = _a.organization, location = _a.location, transactionName = _a.transactionName;
        return columnOrder.map(function (column, index) {
            var field = String(column.key);
            // TODO add a better abstraction for this in fieldRenderers.
            var fieldName = getAggregateAlias(field);
            var fieldType = tableMeta[fieldName];
            var fieldRenderer = getFieldRenderer(field, tableMeta);
            var rendered = fieldRenderer(row, { organization: organization, location: location });
            var isFirstCell = index === 0;
            if (isFirstCell) {
                // The first column of the row should link to the transaction details view
                var eventSlug = generateEventSlug(row);
                var target = getTransactionDetailsUrl(organization, eventSlug, transactionName, location.query);
                rendered = (<Link data-test-id="view-details" to={target} onClick={_this.handleViewDetailsClick}>
            {rendered}
          </Link>);
            }
            var isNumeric = ['integer', 'number', 'duration'].includes(fieldType);
            var key = rowIndex + ":" + column.key + ":" + index;
            if (isNumeric) {
                return <GridBodyCellNumber key={key}>{rendered}</GridBodyCellNumber>;
            }
            return <GridBodyCell key={key}>{rendered}</GridBodyCell>;
        });
    };
    TransactionTable.prototype.render = function () {
        var _a = this.props, isLoading = _a.isLoading, tableData = _a.tableData;
        var hasResults = tableData && tableData.data && tableData.meta && tableData.data.length > 0;
        return (<React.Fragment>
        <PanelTable isEmpty={!hasResults} emptyMessage={t('No transactions found')} headers={this.renderHeader()} isLoading={isLoading} disablePadding>
          {this.renderResults()}
        </PanelTable>
      </React.Fragment>);
    };
    return TransactionTable;
}(React.PureComponent));
var Header = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  justify-content: space-between;\n  align-items: center;\n  margin: 0 0 ", " 0;\n"], ["\n  display: flex;\n  justify-content: space-between;\n  align-items: center;\n  margin: 0 0 ", " 0;\n"])), space(1));
var HeaderButtonContainer = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  flex-direction: row;\n"], ["\n  display: flex;\n  flex-direction: row;\n"])));
export default TransactionList;
var templateObject_1, templateObject_2;
//# sourceMappingURL=transactionList.jsx.map