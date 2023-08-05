import { __assign, __read, __spread } from "tslib";
import Papa from 'papaparse';
import { browserHistory } from 'react-router';
import { tokenizeSearch, stringifyQueryObject } from 'app/utils/tokenizeSearch';
import { t } from 'app/locale';
import { getTitle } from 'app/utils/events';
import { getUtcDateString } from 'app/utils/dates';
import { URL_PARAM } from 'app/constants/globalSelectionHeader';
import { disableMacros } from 'app/views/discover/result/utils';
import { COL_WIDTH_UNDEFINED } from 'app/components/gridEditable';
import { AGGREGATIONS, FIELDS, explodeFieldString, getAggregateAlias, TRACING_FIELDS, } from 'app/utils/discover/fields';
import { ALL_VIEWS, TRANSACTION_VIEWS } from './data';
import { FieldValueKind } from './table/types';
var TEMPLATE_TABLE_COLUMN = {
    key: '',
    name: '',
    type: 'never',
    isSortable: false,
    column: Object.freeze({ kind: 'field', field: '' }),
    width: COL_WIDTH_UNDEFINED,
};
function normalizeUserTag(key, value) {
    var parts = value.split(':', 2);
    if (parts.length !== 2) {
        return [key, parts[0]];
    }
    var normalizedKey = [key, parts[0]].join('.');
    return [normalizedKey, parts[1]];
}
// TODO(mark) these types are coupled to the gridEditable component types and
// I'd prefer the types to be more general purpose but that will require a second pass.
export function decodeColumnOrder(fields) {
    return fields.map(function (f) {
        var column = __assign({}, TEMPLATE_TABLE_COLUMN);
        var col = explodeFieldString(f.field);
        column.key = f.field;
        column.name = f.field;
        column.width = f.width || COL_WIDTH_UNDEFINED;
        if (col.kind === 'function') {
            // Aggregations can have a strict outputType or they can inherit from their field.
            // Otherwise use the FIELDS data to infer types.
            var aggregate = AGGREGATIONS[col.function[0]];
            if (aggregate && aggregate.outputType) {
                column.type = aggregate.outputType;
            }
            else if (FIELDS.hasOwnProperty(col.function[1])) {
                column.type = FIELDS[col.function[1]];
            }
            column.isSortable = aggregate && aggregate.isSortable;
        }
        else if (col.kind === 'field') {
            column.type = FIELDS[col.field];
        }
        column.column = col;
        return column;
    });
}
export function pushEventViewToLocation(props) {
    var location = props.location, nextEventView = props.nextEventView;
    var extraQuery = props.extraQuery || {};
    var queryStringObject = nextEventView.generateQueryStringObject();
    browserHistory.push(__assign(__assign({}, location), { query: __assign(__assign({}, extraQuery), queryStringObject) }));
}
export function generateTitle(_a) {
    var eventView = _a.eventView, event = _a.event;
    var titles = [t('Discover')];
    var eventViewName = eventView.name;
    if (typeof eventViewName === 'string' && String(eventViewName).trim().length > 0) {
        titles.push(String(eventViewName).trim());
    }
    var eventTitle = event ? getTitle(event).title : undefined;
    if (eventTitle) {
        titles.push(eventTitle);
    }
    titles.reverse();
    return titles.join(' - ');
}
export function getPrebuiltQueries(organization) {
    var views = ALL_VIEWS;
    if (organization.features.includes('performance-view')) {
        // insert transactions queries at index 2
        var cloned = __spread(ALL_VIEWS);
        cloned.splice.apply(cloned, __spread([2, 0], TRANSACTION_VIEWS));
        views = cloned;
    }
    return views;
}
export function downloadAsCsv(tableData, columnOrder, filename) {
    var data = tableData.data;
    var headings = columnOrder.map(function (column) { return column.name; });
    var csvContent = Papa.unparse({
        fields: headings,
        data: data.map(function (row) {
            return headings.map(function (col) {
                col = getAggregateAlias(col);
                // This needs to match the order done in the userBadge component
                if (col === 'user') {
                    return disableMacros(row.user ||
                        row['user.name'] ||
                        row['user.email'] ||
                        row['user.username'] ||
                        row['user.ip']);
                }
                return disableMacros(row[col]);
            });
        }),
    });
    // Need to also manually replace # since encodeURI skips them
    var encodedDataUrl = "data:text/csv;charset=utf8," + encodeURIComponent(csvContent);
    // Create a download link then click it, this is so we can get a filename
    var link = document.createElement('a');
    var now = new Date();
    link.setAttribute('href', encodedDataUrl);
    link.setAttribute('download', filename + " " + getUtcDateString(now) + ".csv");
    link.click();
    link.remove();
    // Make testing easier
    return encodedDataUrl;
}
// A map between aggregate function names and its un-aggregated form
var TRANSFORM_AGGREGATES = {
    last_seen: 'timestamp',
    latest_event: 'id',
    apdex: '',
    impact: '',
    user_misery: '',
    failure_rate: '',
};
function transformAggregate(fieldName) {
    // test if a field name is a percentile field name. for example: p50
    if (/^p\d+$/.test(fieldName)) {
        return 'transaction.duration';
    }
    return TRANSFORM_AGGREGATES[fieldName] || '';
}
function isTransformAggregate(fieldName) {
    return transformAggregate(fieldName) !== '';
}
/**
 * Convert an aggregated query into one that does not have aggregates.
 * Will also apply additions conditions defined in `additionalConditions`
 * and generate conditions based on the `dataRow` parameter and the current fields
 * in the `eventView`.
 */
export function getExpandedResults(eventView, additionalConditions, dataRow) {
    // Find aggregate fields and flag them for updates.
    var fieldsToUpdate = [];
    eventView.fields.forEach(function (field, index) {
        var column = explodeFieldString(field.field);
        if (column.kind === 'function') {
            fieldsToUpdate.push(index);
        }
    });
    var nextView = eventView.clone();
    var transformedFields = new Set();
    var fieldsToDelete = [];
    // make a best effort to replace aggregated columns with their non-aggregated form
    fieldsToUpdate.forEach(function (indexToUpdate) {
        var currentField = nextView.fields[indexToUpdate];
        var exploded = explodeFieldString(currentField.field);
        var fieldNameAlias = '';
        if (exploded.kind === 'function' && isTransformAggregate(exploded.function[0])) {
            fieldNameAlias = exploded.function[0];
        }
        else if (exploded.kind === 'field') {
            fieldNameAlias = exploded.field;
        }
        if (fieldNameAlias !== undefined && isTransformAggregate(fieldNameAlias)) {
            var nextFieldName = transformAggregate(fieldNameAlias);
            if (!nextFieldName || transformedFields.has(nextFieldName)) {
                // this field is either duplicated in another column, or nextFieldName is undefined.
                // in either case, we remove this column
                fieldsToDelete.push(indexToUpdate);
                return;
            }
            transformedFields.add(nextFieldName);
            var updatedColumn = {
                kind: 'field',
                field: nextFieldName,
            };
            nextView = nextView.withUpdatedColumn(indexToUpdate, updatedColumn, undefined);
            return;
        }
        if ((exploded.kind === 'field' && transformedFields.has(exploded.field)) ||
            (exploded.kind === 'function' && transformedFields.has(exploded.function[1]))) {
            // If we already have this field we can delete the new instance.
            fieldsToDelete.push(indexToUpdate);
            return;
        }
        if (exploded.kind === 'function') {
            var field = exploded.function[1];
            // edge case: transform count() into id
            if (exploded.function[0] === 'count') {
                field = 'id';
            }
            if (!field) {
                // This is a function with no field alias. We delete this column as it'll add a blank column in the drilldown.
                fieldsToDelete.push(indexToUpdate);
                return;
            }
            transformedFields.add(field);
            var updatedColumn = {
                kind: 'field',
                field: field,
            };
            nextView = nextView.withUpdatedColumn(indexToUpdate, updatedColumn, undefined);
        }
    });
    // delete any columns marked for deletion
    fieldsToDelete.reverse().forEach(function (index) {
        nextView = nextView.withDeletedColumn(index, undefined);
    });
    nextView.query = generateExpandedConditions(nextView, additionalConditions, dataRow);
    return nextView;
}
/**
 * Create additional conditions based on the fields in an EventView
 * and a datarow/event
 */
function generateAdditionalConditions(eventView, dataRow) {
    var specialKeys = Object.values(URL_PARAM);
    var conditions = {};
    if (!dataRow) {
        return conditions;
    }
    eventView.fields.forEach(function (field) {
        var column = explodeFieldString(field.field);
        // Skip aggregate fields
        if (column.kind === 'function') {
            return;
        }
        var dataKey = getAggregateAlias(field.field);
        // Append the current field as a condition if it exists in the dataRow
        // Or is a simple key in the event. More complex deeply nested fields are
        // more challenging to get at as their location in the structure does not
        // match their name.
        if (dataRow.hasOwnProperty(dataKey)) {
            var value = dataRow[dataKey];
            var nextValue = value === null || value === undefined ? '' : String(value).trim();
            switch (column.field) {
                case 'timestamp':
                    // normalize the "timestamp" field to ensure the payload works
                    conditions[column.field] = getUtcDateString(nextValue);
                    break;
                case 'user':
                    var normalized = normalizeUserTag(dataKey, nextValue);
                    conditions[normalized[0]] = normalized[1];
                    break;
                default:
                    conditions[column.field] = nextValue;
            }
        }
        // If we have an event, check tags as well.
        if (dataRow.tags && Array.isArray(dataRow.tags)) {
            var tagIndex = dataRow.tags.findIndex(function (item) { return item.key === dataKey; });
            if (tagIndex > -1) {
                var key = specialKeys.includes(column.field)
                    ? "tags[" + column.field + "]"
                    : column.field;
                var tagValue = dataRow.tags[tagIndex].value;
                if (key === 'user') {
                    // Remove the user condition that might have been added
                    // from the user context.
                    delete conditions[key];
                    var normalized = normalizeUserTag(key, tagValue);
                    conditions[normalized[0]] = normalized[1];
                    return;
                }
                conditions[key] = tagValue;
            }
        }
    });
    return conditions;
}
function generateExpandedConditions(eventView, additionalConditions, dataRow) {
    var parsedQuery = tokenizeSearch(eventView.query);
    // Remove any aggregates from the search conditions.
    // otherwise, it'll lead to an invalid query result.
    for (var key in parsedQuery) {
        var column = explodeFieldString(key);
        if (column.kind === 'function') {
            delete parsedQuery[key];
        }
    }
    var conditions = Object.assign({}, additionalConditions, generateAdditionalConditions(eventView, dataRow));
    // Add additional conditions provided and generated.
    for (var key in conditions) {
        var value = additionalConditions[key];
        if (key === 'project.id') {
            eventView.project = __spread(eventView.project, [parseInt(value, 10)]);
            continue;
        }
        if (key === 'environment') {
            eventView.environment = __spread(eventView.environment, [value]);
            continue;
        }
        if (key === 'user' && typeof value === 'string') {
            var normalized = normalizeUserTag(key, value);
            parsedQuery[normalized[0]] = [normalized[1]];
            continue;
        }
        var column = explodeFieldString(key);
        // Skip aggregates as they will be invalid.
        if (column.kind === 'function') {
            continue;
        }
        parsedQuery[key] = [conditions[key]];
    }
    return stringifyQueryObject(parsedQuery);
}
export function getDiscoverLandingUrl(organization) {
    if (organization.features.includes('discover-query')) {
        return "/organizations/" + organization.slug + "/discover/queries/";
    }
    return "/organizations/" + organization.slug + "/discover/results/";
}
export function generateFieldOptions(_a) {
    var organization = _a.organization, tagKeys = _a.tagKeys, _b = _a.aggregations, aggregations = _b === void 0 ? AGGREGATIONS : _b, _c = _a.fields, fields = _c === void 0 ? FIELDS : _c;
    var fieldKeys = Object.keys(fields);
    var functions = Object.keys(aggregations);
    // Strip tracing features if the org doesn't have access.
    if (!organization.features.includes('performance-view')) {
        fieldKeys = fieldKeys.filter(function (item) { return !TRACING_FIELDS.includes(item); });
        functions = functions.filter(function (item) { return !TRACING_FIELDS.includes(item); });
    }
    var fieldOptions = {};
    // Index items by prefixed keys as custom tags can overlap both fields and
    // function names. Having a mapping makes finding the value objects easier
    // later as well.
    functions.forEach(function (func) {
        var ellipsis = aggregations[func].parameters.length ? '\u2026' : '';
        fieldOptions["function:" + func] = {
            label: func + "(" + ellipsis + ")",
            value: {
                kind: FieldValueKind.FUNCTION,
                meta: {
                    name: func,
                    parameters: __spread(aggregations[func].parameters),
                },
            },
        };
    });
    fieldKeys.forEach(function (field) {
        fieldOptions["field:" + field] = {
            label: field,
            value: {
                kind: FieldValueKind.FIELD,
                meta: {
                    name: field,
                    dataType: fields[field],
                },
            },
        };
    });
    if (tagKeys !== undefined && tagKeys !== null) {
        tagKeys.forEach(function (tag) {
            var tagValue = fields.hasOwnProperty(tag) || AGGREGATIONS.hasOwnProperty(tag)
                ? "tags[" + tag + "]"
                : tag;
            fieldOptions["tag:" + tag] = {
                label: tag,
                value: {
                    kind: FieldValueKind.TAG,
                    meta: { name: tagValue, dataType: 'string' },
                },
            };
        });
    }
    return fieldOptions;
}
//# sourceMappingURL=utils.jsx.map