import { __assign, __extends, __read, __spread } from "tslib";
import React from 'react';
import * as ReactRouter from 'react-router';
import Pagination from 'app/components/pagination';
import Link from 'app/components/links/link';
import { isFieldSortable, } from 'app/utils/discover/eventView';
import GridEditable, { COL_WIDTH_UNDEFINED } from 'app/components/gridEditable';
import SortLink from 'app/components/gridEditable/sortLink';
import HeaderCell from 'app/views/eventsV2/table/headerCell';
import CellAction, { Actions } from 'app/views/eventsV2/table/cellAction';
import DiscoverQuery from 'app/utils/discover/discoverQuery';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import { getFieldRenderer } from 'app/utils/discover/fieldRenderers';
import { tokenizeSearch, stringifyQueryObject } from 'app/utils/tokenizeSearch';
import { transactionSummaryRouteWithQuery } from './transactionSummary/utils';
import { COLUMN_TITLES } from './data';
export function getProjectID(eventData, projects) {
    var projectSlug = (eventData === null || eventData === void 0 ? void 0 : eventData.project) || undefined;
    if (typeof projectSlug === undefined) {
        return undefined;
    }
    var project = projects.find(function (currentProject) { return currentProject.slug === projectSlug; });
    if (!project) {
        return undefined;
    }
    return project.id;
}
var Table = /** @class */ (function (_super) {
    __extends(Table, _super);
    function Table() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            widths: [],
        };
        _this.handleCellAction = function (column, tableMeta) {
            return function (action, value) {
                var _a = _this.props, eventView = _a.eventView, location = _a.location, organization = _a.organization;
                var nextLocationQuery = {};
                var searchConditions = tokenizeSearch(eventView.query);
                // remove any event.type queries since it is implied to apply to only transactions
                delete searchConditions['event.type'];
                trackAnalyticsEvent({
                    eventKey: 'performance_views.overview.cellaction',
                    eventName: 'Performance Views: Cell Action Clicked',
                    organization_id: parseInt(organization.id, 10),
                    action: action,
                });
                switch (action) {
                    case Actions.ADD: {
                        // Remove exclusion if it exists.
                        delete searchConditions["!" + column.name];
                        searchConditions[column.name] = ["" + value];
                        nextLocationQuery = {
                            query: stringifyQueryObject(searchConditions),
                        };
                        break;
                    }
                    case Actions.EXCLUDE: {
                        // Remove positive if it exists.
                        delete searchConditions[column.name];
                        // Negations should stack up.
                        var negation = "!" + column.name;
                        if (!searchConditions.hasOwnProperty(negation)) {
                            searchConditions[negation] = [];
                        }
                        searchConditions[negation].push("" + value);
                        nextLocationQuery = {
                            query: stringifyQueryObject(searchConditions),
                        };
                        break;
                    }
                    case Actions.SHOW_GREATER_THAN: {
                        // Remove query token if it already exists
                        delete searchConditions[column.name];
                        searchConditions[column.name] = [">" + value];
                        var field = { field: column.name, width: column.width };
                        // sort descending order
                        var nextEventView = eventView.sortOnField(field, tableMeta, 'desc');
                        var queryStringObject = nextEventView.generateQueryStringObject();
                        nextLocationQuery = {
                            query: stringifyQueryObject(searchConditions),
                            sort: queryStringObject.sort,
                        };
                        break;
                    }
                    case Actions.SHOW_LESS_THAN: {
                        // Remove query token if it already exists
                        delete searchConditions[column.name];
                        searchConditions[column.name] = ["<" + value];
                        var field = { field: column.name, width: column.width };
                        // sort ascending order
                        var nextEventView = eventView.sortOnField(field, tableMeta, 'asc');
                        var queryStringObject = nextEventView.generateQueryStringObject();
                        nextLocationQuery = {
                            query: stringifyQueryObject(searchConditions),
                            sort: queryStringObject.sort,
                        };
                        break;
                    }
                    default:
                        throw new Error("Unknown action type. " + action);
                }
                ReactRouter.browserHistory.push({
                    pathname: location.pathname,
                    query: __assign(__assign(__assign({}, location.query), { cursor: undefined }), nextLocationQuery),
                });
            };
        };
        _this.renderBodyCell = function (tableData) {
            var _a = _this.props, eventView = _a.eventView, organization = _a.organization, projects = _a.projects, location = _a.location, summaryConditions = _a.summaryConditions;
            return function (column, dataRow) {
                if (!tableData || !tableData.meta) {
                    return dataRow[column.key];
                }
                var tableMeta = tableData.meta;
                var field = String(column.key);
                var fieldRenderer = getFieldRenderer(field, tableMeta);
                var rendered = fieldRenderer(dataRow, { organization: organization, location: location });
                var allowActions = [
                    Actions.ADD,
                    Actions.EXCLUDE,
                    Actions.SHOW_GREATER_THAN,
                    Actions.SHOW_LESS_THAN,
                ];
                if (field === 'transaction') {
                    var projectID = getProjectID(dataRow, projects);
                    var summaryView = eventView.clone();
                    summaryView.query = summaryConditions;
                    var target = transactionSummaryRouteWithQuery({
                        orgSlug: organization.slug,
                        transaction: String(dataRow.transaction) || '',
                        query: summaryView.generateQueryStringObject(),
                        projectID: projectID,
                    });
                    return (<CellAction column={column} dataRow={dataRow} handleCellAction={_this.handleCellAction(column, tableData.meta)} allowActions={allowActions}>
            <Link to={target} onClick={_this.handleSummaryClick}>
              {rendered}
            </Link>
          </CellAction>);
                }
                if (field.startsWith('user_misery')) {
                    // don't display per cell actions for user_misery
                    return rendered;
                }
                return (<CellAction column={column} dataRow={dataRow} handleCellAction={_this.handleCellAction(column, tableData.meta)} allowActions={allowActions}>
          {rendered}
        </CellAction>);
            };
        };
        _this.renderHeadCell = function (tableMeta) {
            var _a = _this.props, eventView = _a.eventView, location = _a.location;
            return function (column, index) {
                return (<HeaderCell column={column} tableMeta={tableMeta}>
          {function (_a) {
                    var align = _a.align;
                    var field = { field: column.name, width: column.width };
                    function generateSortLink() {
                        if (!tableMeta) {
                            return undefined;
                        }
                        var nextEventView = eventView.sortOnField(field, tableMeta);
                        var queryStringObject = nextEventView.generateQueryStringObject();
                        return __assign(__assign({}, location), { query: __assign(__assign({}, location.query), { sort: queryStringObject.sort }) });
                    }
                    var currentSort = eventView.sortForField(field, tableMeta);
                    var canSort = isFieldSortable(field, tableMeta);
                    return (<SortLink align={align} title={COLUMN_TITLES[index] || field.field} direction={currentSort ? currentSort.kind : undefined} canSort={canSort} generateSortLink={generateSortLink}/>);
                }}
        </HeaderCell>);
            };
        };
        _this.handleSummaryClick = function () {
            var organization = _this.props.organization;
            trackAnalyticsEvent({
                eventKey: 'performance_views.overview.navigate.summary',
                eventName: 'Performance Views: Overview view summary',
                organization_id: parseInt(organization.id, 10),
            });
        };
        _this.handleResizeColumn = function (columnIndex, nextColumn) {
            var widths = __spread(_this.state.widths);
            widths[columnIndex] = nextColumn.width
                ? Number(nextColumn.width)
                : COL_WIDTH_UNDEFINED;
            _this.setState({ widths: widths });
        };
        return _this;
    }
    Table.prototype.render = function () {
        var _this = this;
        var _a = this.props, eventView = _a.eventView, organization = _a.organization, location = _a.location, keyTransactions = _a.keyTransactions;
        var widths = this.state.widths;
        var columnOrder = eventView
            .getColumns()
            .map(function (col, i) {
            if (typeof widths[i] === 'number') {
                return __assign(__assign({}, col), { width: widths[i] });
            }
            return col;
        });
        var columnSortBy = eventView.getSorts();
        return (<div>
        <DiscoverQuery eventView={eventView} orgSlug={organization.slug} location={location} keyTransactions={keyTransactions}>
          {function (_a) {
            var pageLinks = _a.pageLinks, isLoading = _a.isLoading, tableData = _a.tableData;
            return (<React.Fragment>
              <GridEditable isLoading={isLoading} data={tableData ? tableData.data : []} columnOrder={columnOrder} columnSortBy={columnSortBy} grid={{
                onResizeColumn: _this.handleResizeColumn,
                renderHeadCell: _this.renderHeadCell(tableData === null || tableData === void 0 ? void 0 : tableData.meta),
                renderBodyCell: _this.renderBodyCell(tableData),
            }} location={location}/>
              <Pagination pageLinks={pageLinks}/>
            </React.Fragment>);
        }}
        </DiscoverQuery>
      </div>);
    };
    return Table;
}(React.Component));
export default Table;
//# sourceMappingURL=table.jsx.map