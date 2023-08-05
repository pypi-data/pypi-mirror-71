import { __assign, __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { browserHistory } from 'react-router';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import GridEditable, { COL_WIDTH_UNDEFINED, COL_WIDTH_MINIMUM, } from 'app/components/gridEditable';
import SortLink from 'app/components/gridEditable/sortLink';
import { IconStack } from 'app/icons';
import { t } from 'app/locale';
import { openModal } from 'app/actionCreators/modal';
import Link from 'app/components/links/link';
import Tooltip from 'app/components/tooltip';
import { isFieldSortable, pickRelevantLocationQueryStrings, } from 'app/utils/discover/eventView';
import { getFieldRenderer } from 'app/utils/discover/fieldRenderers';
import { generateEventSlug, eventDetailsRouteWithEventView } from 'app/utils/discover/urls';
import withProjects from 'app/utils/withProjects';
import { tokenizeSearch, stringifyQueryObject } from 'app/utils/tokenizeSearch';
import { transactionSummaryRouteWithQuery } from 'app/views/performance/transactionSummary/utils';
import { getExpandedResults, pushEventViewToLocation } from '../utils';
import ColumnEditModal, { modalCss } from './columnEditModal';
import HeaderCell from './headerCell';
import CellAction, { Actions } from './cellAction';
import TableActions from './tableActions';
/**
 * The `TableView` is marked with leading _ in its method names. It consumes
 * the EventView object given in its props to generate new EventView objects
 * for actions like resizing column.

 * The entire state of the table view (or event view) is co-located within
 * the EventView object. This object is fed from the props.
 *
 * Attempting to modify the state, and therefore, modifying the given EventView
 * object given from its props, will generate new instances of EventView objects.
 *
 * In most cases, the new EventView object differs from the previous EventView
 * object. The new EventView object is pushed to the location object.
 */
var TableView = /** @class */ (function (_super) {
    __extends(TableView, _super);
    function TableView() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        /**
         * Updates a column on resizing
         */
        _this._resizeColumn = function (columnIndex, nextColumn) {
            var _a = _this.props, location = _a.location, eventView = _a.eventView;
            var newWidth = nextColumn.width ? Number(nextColumn.width) : COL_WIDTH_UNDEFINED;
            var nextEventView = eventView.withResizedColumn(columnIndex, newWidth);
            pushEventViewToLocation({
                location: location,
                nextEventView: nextEventView,
                extraQuery: pickRelevantLocationQueryStrings(location),
            });
        };
        _this._renderPrependColumns = function (isHeader, dataRow, rowIndex) {
            var _a = _this.props, organization = _a.organization, eventView = _a.eventView, tableData = _a.tableData, location = _a.location;
            var hasAggregates = eventView.getAggregateFields().length > 0;
            if (isHeader) {
                if (!hasAggregates) {
                    return [
                        <PrependHeader key="header-event-id">
            <SortLink align="left" title={t('Id')} direction={undefined} canSort={false} generateSortLink={function () { return undefined; }}/>
          </PrependHeader>,
                    ];
                }
                return [
                    <PrependHeader key="header-icon">
          <IconStack size="sm"/>
        </PrependHeader>,
                ];
            }
            if (!hasAggregates) {
                var value = dataRow.id;
                if (tableData && tableData.meta) {
                    var fieldRenderer = getFieldRenderer('id', tableData.meta);
                    value = fieldRenderer(dataRow, { organization: organization, location: location });
                }
                var eventSlug = generateEventSlug(dataRow);
                var target_1 = eventDetailsRouteWithEventView({
                    orgSlug: organization.slug,
                    eventSlug: eventSlug,
                    eventView: eventView,
                });
                return [
                    <Tooltip key={"eventlink" + rowIndex} title={t('View Event')}>
          <StyledLink data-test-id="view-event" to={target_1}>
            {value}
          </StyledLink>
        </Tooltip>,
                ];
            }
            var nextView = getExpandedResults(eventView, {}, dataRow);
            var target = {
                pathname: location.pathname,
                query: nextView.generateQueryStringObject(),
            };
            return [
                <Tooltip key={"eventlink" + rowIndex} title={t('Open Stack')}>
        <Link to={target} data-test-id="open-stack">
          <StyledIcon size="sm"/>
        </Link>
      </Tooltip>,
            ];
        };
        _this._renderGridHeaderCell = function (column) {
            var _a = _this.props, eventView = _a.eventView, location = _a.location, tableData = _a.tableData;
            var tableMeta = tableData === null || tableData === void 0 ? void 0 : tableData.meta;
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
                    return __assign(__assign({}, location), { query: queryStringObject });
                }
                var currentSort = eventView.sortForField(field, tableMeta);
                var canSort = isFieldSortable(field, tableMeta);
                return (<SortLink align={align} title={column.name} direction={currentSort ? currentSort.kind : undefined} canSort={canSort} generateSortLink={generateSortLink}/>);
            }}
      </HeaderCell>);
        };
        _this._renderGridBodyCell = function (column, dataRow) {
            var _a = _this.props, location = _a.location, organization = _a.organization, tableData = _a.tableData;
            if (!tableData || !tableData.meta) {
                return dataRow[column.key];
            }
            var fieldRenderer = getFieldRenderer(String(column.key), tableData.meta);
            return (<CellAction column={column} dataRow={dataRow} handleCellAction={_this.handleCellAction(dataRow, column, tableData.meta)}>
        {fieldRenderer(dataRow, { organization: organization, location: location })}
      </CellAction>);
        };
        _this.handleEditColumns = function () {
            var _a = _this.props, organization = _a.organization, eventView = _a.eventView, tagKeys = _a.tagKeys;
            openModal(function (modalProps) { return (<ColumnEditModal {...modalProps} organization={organization} tagKeys={tagKeys} columns={eventView.getColumns().map(function (col) { return col.column; })} onApply={_this.handleUpdateColumns}/>); }, { modalCss: modalCss });
        };
        _this.handleCellAction = function (dataRow, column, tableMeta) {
            return function (action, value) {
                var _a = _this.props, eventView = _a.eventView, organization = _a.organization, projects = _a.projects;
                var query = tokenizeSearch(eventView.query);
                var nextView = eventView.clone();
                trackAnalyticsEvent({
                    eventKey: 'discover_v2.results.cellaction',
                    eventName: 'Discoverv2: Cell Action Clicked',
                    organization_id: parseInt(organization.id, 10),
                    action: action,
                });
                switch (action) {
                    case Actions.ADD:
                        // Remove exclusion if it exists.
                        delete query["!" + column.name];
                        query[column.name] = ["" + value];
                        break;
                    case Actions.EXCLUDE:
                        // Remove positive if it exists.
                        delete query[column.name];
                        // Negations should stack up.
                        var negation = "!" + column.name;
                        if (!query.hasOwnProperty(negation)) {
                            query[negation] = [];
                        }
                        query[negation].push("" + value);
                        break;
                    case Actions.SHOW_GREATER_THAN: {
                        // Remove query token if it already exists
                        delete query[column.name];
                        query[column.name] = [">" + value];
                        var field = { field: column.name, width: column.width };
                        // sort descending order
                        nextView = nextView.sortOnField(field, tableMeta, 'desc');
                        break;
                    }
                    case Actions.SHOW_LESS_THAN: {
                        // Remove query token if it already exists
                        delete query[column.name];
                        query[column.name] = ["<" + value];
                        var field = { field: column.name, width: column.width };
                        // sort ascending order
                        nextView = nextView.sortOnField(field, tableMeta, 'asc');
                        break;
                    }
                    case Actions.TRANSACTION: {
                        var maybeProject = projects.find(function (project) { return project.slug === dataRow.project; });
                        var projectID = maybeProject ? [maybeProject.id] : undefined;
                        var next = transactionSummaryRouteWithQuery({
                            orgSlug: organization.slug,
                            transaction: String(value),
                            projectID: projectID,
                            query: {},
                        });
                        browserHistory.push(next);
                        return;
                    }
                    case Actions.RELEASE: {
                        var maybeProject = projects.find(function (project) {
                            return project.slug === dataRow.project;
                        });
                        browserHistory.push({
                            pathname: "/organizations/" + organization.slug + "/releases/" + encodeURIComponent(value) + "/",
                            query: __assign(__assign({}, nextView.getGlobalSelection()), { project: maybeProject ? maybeProject.id : undefined }),
                        });
                        return;
                    }
                    case Actions.DRILLDOWN: {
                        // count_unique(column) drilldown
                        trackAnalyticsEvent({
                            eventKey: 'discover_v2.results.drilldown',
                            eventName: 'Discoverv2: Click aggregate drilldown',
                            organization_id: parseInt(organization.id, 10),
                        });
                        // Drilldown into each distinct value and get a count() for each value.
                        nextView = getExpandedResults(nextView, {}, dataRow).withNewColumn({
                            kind: 'function',
                            function: ['count', '', undefined],
                        });
                        browserHistory.push(nextView.getResultsViewUrlTarget(organization.slug));
                        return;
                    }
                    default:
                        throw new Error("Unknown action type. " + action);
                }
                nextView.query = stringifyQueryObject(query);
                browserHistory.push(nextView.getResultsViewUrlTarget(organization.slug));
            };
        };
        _this.handleUpdateColumns = function (columns) {
            var _a = _this.props, organization = _a.organization, eventView = _a.eventView;
            // metrics
            trackAnalyticsEvent({
                eventKey: 'discover_v2.update_columns',
                eventName: 'Discoverv2: Update columns',
                organization_id: parseInt(organization.id, 10),
            });
            var nextView = eventView.withColumns(columns);
            browserHistory.push(nextView.getResultsViewUrlTarget(organization.slug));
        };
        _this.renderHeaderButtons = function () {
            var _a = _this.props, organization = _a.organization, title = _a.title, eventView = _a.eventView, isLoading = _a.isLoading, tableData = _a.tableData, location = _a.location, onChangeShowTags = _a.onChangeShowTags, showTags = _a.showTags;
            return (<TableActions title={title} isLoading={isLoading} organization={organization} eventView={eventView} onEdit={_this.handleEditColumns} tableData={tableData} location={location} onChangeShowTags={onChangeShowTags} showTags={showTags}/>);
        };
        return _this;
    }
    TableView.prototype.render = function () {
        var _a = this.props, isLoading = _a.isLoading, error = _a.error, location = _a.location, tableData = _a.tableData, eventView = _a.eventView;
        var columnOrder = eventView.getColumns();
        var columnSortBy = eventView.getSorts();
        var hasAggregates = eventView.getAggregateFields().length > 0;
        var prependColumnWidths = hasAggregates
            ? ['40px']
            : ["minmax(" + COL_WIDTH_MINIMUM + "px, max-content)"];
        return (<GridEditable isLoading={isLoading} error={error} data={tableData ? tableData.data : []} columnOrder={columnOrder} columnSortBy={columnSortBy} title={t('Results')} grid={{
            renderHeadCell: this._renderGridHeaderCell,
            renderBodyCell: this._renderGridBodyCell,
            onResizeColumn: this._resizeColumn,
            renderPrependColumns: this._renderPrependColumns,
            prependColumnWidths: prependColumnWidths,
        }} headerButtons={this.renderHeaderButtons} location={location}/>);
    };
    return TableView;
}(React.Component));
var PrependHeader = styled('span')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (p) { return p.theme.gray600; });
var StyledLink = styled(Link)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  > div {\n    display: inline;\n  }\n"], ["\n  > div {\n    display: inline;\n  }\n"])));
var StyledIcon = styled(IconStack)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  vertical-align: middle;\n"], ["\n  vertical-align: middle;\n"])));
export default withProjects(TableView);
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=tableView.jsx.map