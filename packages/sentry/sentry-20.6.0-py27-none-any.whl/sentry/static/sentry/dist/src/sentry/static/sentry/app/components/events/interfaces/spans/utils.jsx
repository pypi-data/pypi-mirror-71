import { __assign } from "tslib";
import isString from 'lodash/isString';
import moment from 'moment';
import set from 'lodash/set';
import isNumber from 'lodash/isNumber';
import { assert } from 'app/types/utils';
import CHART_PALETTE from 'app/constants/chartPalette';
// get position of element relative to top/left of document
var getOffsetOfElement = function (element) {
    // left and top are relative to viewport
    var _a = element.getBoundingClientRect(), left = _a.left, top = _a.top;
    // get values that the document is currently scrolled by
    var scrollLeft = window.pageXOffset;
    var scrollTop = window.pageYOffset;
    return { x: left + scrollLeft, y: top + scrollTop };
};
export var rectOfContent = function (element) {
    var _a = getOffsetOfElement(element), x = _a.x, y = _a.y;
    // offsets for the border and any scrollbars (clientLeft and clientTop),
    // and if the element was scrolled (scrollLeft and scrollTop)
    //
    // NOTE: clientLeft and clientTop does not account for any margins nor padding
    var contentOffsetLeft = element.clientLeft - element.scrollLeft;
    var contentOffsetTop = element.clientTop - element.scrollTop;
    return {
        x: x + contentOffsetLeft,
        y: y + contentOffsetTop,
        width: element.scrollWidth,
        height: element.scrollHeight,
    };
};
export var rectOfViewport = function () { return ({
    x: window.pageXOffset,
    y: window.pageYOffset,
    width: window.document.documentElement.clientWidth,
    height: window.document.documentElement.clientHeight,
}); };
export var rectRelativeTo = function (rect, pos) {
    if (pos === void 0) { pos = { x: 0, y: 0 }; }
    return ({
        x: rect.x - pos.x,
        y: rect.y - pos.y,
        width: rect.width,
        height: rect.height,
    });
};
export var rectOfElement = function (element) {
    var _a = getOffsetOfElement(element), x = _a.x, y = _a.y;
    return {
        x: x,
        y: y,
        width: element.offsetWidth,
        height: element.offsetHeight,
    };
};
export var clamp = function (value, min, max) {
    if (value < min) {
        return min;
    }
    if (value > max) {
        return max;
    }
    return value;
};
export var isValidSpanID = function (maybeSpanID) {
    return isString(maybeSpanID) && maybeSpanID.length > 0;
};
export var toPercent = function (value) { return (value * 100).toFixed(3) + "%"; };
var normalizeTimestamps = function (spanBounds) {
    var startTimestamp = spanBounds.startTimestamp, endTimestamp = spanBounds.endTimestamp;
    if (startTimestamp > endTimestamp) {
        return { startTimestamp: endTimestamp, endTimestamp: startTimestamp };
    }
    return spanBounds;
};
export var TimestampStatus;
(function (TimestampStatus) {
    TimestampStatus[TimestampStatus["Stable"] = 0] = "Stable";
    TimestampStatus[TimestampStatus["Reversed"] = 1] = "Reversed";
    TimestampStatus[TimestampStatus["Equal"] = 2] = "Equal";
})(TimestampStatus || (TimestampStatus = {}));
export var parseSpanTimestamps = function (spanBounds) {
    var startTimestamp = spanBounds.startTimestamp;
    var endTimestamp = spanBounds.endTimestamp;
    if (startTimestamp < endTimestamp) {
        return TimestampStatus.Stable;
    }
    if (startTimestamp === endTimestamp) {
        return TimestampStatus.Equal;
    }
    return TimestampStatus.Reversed;
};
// given the start and end trace timestamps, and the view window, we want to generate a function
// that'll output the relative %'s for the width and placements relative to the left-hand side.
//
// The view window (viewStart and viewEnd) are percentage values (between 0% and 100%), they correspond to the window placement
// between the start and end trace timestamps.
export var boundsGenerator = function (bounds) {
    var viewStart = bounds.viewStart, viewEnd = bounds.viewEnd;
    var _a = normalizeTimestamps({
        startTimestamp: bounds.traceStartTimestamp,
        endTimestamp: bounds.traceEndTimestamp,
    }), traceStartTimestamp = _a.startTimestamp, traceEndTimestamp = _a.endTimestamp;
    // viewStart and viewEnd are percentage values (%) of the view window relative to the left
    // side of the trace view minimap
    // invariant: viewStart <= viewEnd
    // duration of the entire trace in seconds
    var traceDuration = traceEndTimestamp - traceStartTimestamp;
    var viewStartTimestamp = traceStartTimestamp + viewStart * traceDuration;
    var viewEndTimestamp = traceEndTimestamp - (1 - viewEnd) * traceDuration;
    var viewDuration = viewEndTimestamp - viewStartTimestamp;
    return function (spanBounds) {
        // TODO: alberto.... refactor so this is impossible 😠
        if (traceDuration <= 0) {
            return {
                type: 'TRACE_TIMESTAMPS_EQUAL',
                isSpanVisibleInView: true,
            };
        }
        if (viewDuration <= 0) {
            return {
                type: 'INVALID_VIEW_WINDOW',
                isSpanVisibleInView: true,
            };
        }
        var _a = normalizeTimestamps(spanBounds), startTimestamp = _a.startTimestamp, endTimestamp = _a.endTimestamp;
        var timestampStatus = parseSpanTimestamps(spanBounds);
        var start = (startTimestamp - viewStartTimestamp) / viewDuration;
        var end = (endTimestamp - viewStartTimestamp) / viewDuration;
        var isSpanVisibleInView = end > 0 && start < 1;
        switch (timestampStatus) {
            case TimestampStatus.Equal: {
                return {
                    type: 'TIMESTAMPS_EQUAL',
                    start: start,
                    width: 1,
                    // a span bar is visible even if they're at the extreme ends of the view selection.
                    // these edge cases are:
                    // start == end == 0, and
                    // start == end == 1
                    isSpanVisibleInView: end >= 0 && start <= 1,
                };
            }
            case TimestampStatus.Reversed: {
                return {
                    type: 'TIMESTAMPS_REVERSED',
                    start: start,
                    end: end,
                    isSpanVisibleInView: isSpanVisibleInView,
                };
            }
            case TimestampStatus.Stable: {
                return {
                    type: 'TIMESTAMPS_STABLE',
                    start: start,
                    end: end,
                    isSpanVisibleInView: isSpanVisibleInView,
                };
            }
            default: {
                var _exhaustiveCheck = timestampStatus;
                return _exhaustiveCheck;
            }
        }
    };
};
export var getHumanDuration = function (duration) {
    // note: duration is assumed to be in seconds
    var durationMS = duration * 1000;
    return durationMS.toFixed(2) + "ms";
};
var getLetterIndex = function (letter) {
    var index = 'abcdefghijklmnopqrstuvwxyz'.indexOf(letter) || 0;
    return index === -1 ? 0 : index;
};
var colorsAsArray = Object.keys(CHART_PALETTE).map(function (key) { return CHART_PALETTE[17][key]; });
export var spanColors = {
    default: CHART_PALETTE[17][4],
    transaction: CHART_PALETTE[17][8],
    http: CHART_PALETTE[17][10],
    db: CHART_PALETTE[17][17],
};
export var pickSpanBarColour = function (input) {
    // We pick the color for span bars using the first three letters of the op name.
    // That way colors stay consistent between transactions.
    if (!input || input.length < 3) {
        return CHART_PALETTE[17][4];
    }
    if (spanColors[input]) {
        return spanColors[input];
    }
    var letterIndex1 = getLetterIndex(input.slice(0, 1));
    var letterIndex2 = getLetterIndex(input.slice(1, 2));
    var letterIndex3 = getLetterIndex(input.slice(2, 3));
    return colorsAsArray[(letterIndex1 + letterIndex2 + letterIndex3) % colorsAsArray.length];
};
export var setBodyUserSelect = function (nextValues) {
    // NOTE: Vendor prefixes other than `ms` should begin with a capital letter.
    // ref: https://reactjs.org/docs/dom-elements.html#style
    var previousValues = {
        userSelect: document.body.style.userSelect,
        // MozUserSelect is not typed in TS
        // @ts-ignore
        MozUserSelect: document.body.style.MozUserSelect,
        msUserSelect: document.body.style.msUserSelect,
    };
    document.body.style.userSelect = nextValues.userSelect || '';
    // MozUserSelect is not typed in TS
    // @ts-ignore
    document.body.style.MozUserSelect = nextValues.MozUserSelect;
    document.body.style.msUserSelect = nextValues.msUserSelect;
    return previousValues;
};
export function generateRootSpan(trace) {
    var rootSpan = {
        trace_id: trace.traceID,
        span_id: trace.rootSpanID,
        parent_span_id: trace.parentSpanID,
        start_timestamp: trace.traceStartTimestamp,
        timestamp: trace.traceEndTimestamp,
        op: trace.op,
        description: trace.description,
        data: {},
    };
    return rootSpan;
}
// start and end are assumed to be unix timestamps with fractional seconds
export function getTraceDateTimeRange(input) {
    var start = moment
        .unix(input.start)
        .subtract(12, 'hours')
        .format('YYYY-MM-DDTHH:mm:ss.SSS');
    var end = moment
        .unix(input.end)
        .add(12, 'hours')
        .format('YYYY-MM-DDTHH:mm:ss.SSS');
    return {
        start: start,
        end: end,
    };
}
export function isGapSpan(span) {
    if ('type' in span) {
        return span.type === 'gap';
    }
    return false;
}
export function isOrphanSpan(span) {
    if ('type' in span) {
        if (span.type === 'orphan') {
            return true;
        }
        if (span.type === 'gap') {
            return span.isOrphan;
        }
    }
    return false;
}
export function getSpanID(span, defaultSpanID) {
    if (defaultSpanID === void 0) { defaultSpanID = ''; }
    if (isGapSpan(span)) {
        return defaultSpanID;
    }
    return span.span_id;
}
export function getSpanOperation(span) {
    if (isGapSpan(span)) {
        return undefined;
    }
    return span.op;
}
export function getSpanTraceID(span) {
    if (isGapSpan(span)) {
        return 'gap-span';
    }
    return span.trace_id;
}
export function getSpanParentSpanID(span) {
    if (isGapSpan(span)) {
        return 'gap-span';
    }
    return span.parent_span_id;
}
export function getTraceContext(event) {
    var _a;
    return (_a = event === null || event === void 0 ? void 0 : event.contexts) === null || _a === void 0 ? void 0 : _a.trace;
}
export function parseTrace(event) {
    var _a;
    var spanEntry = event.entries.find(function (entry) { return entry.type === 'spans'; });
    var spans = (_a = spanEntry === null || spanEntry === void 0 ? void 0 : spanEntry.data) !== null && _a !== void 0 ? _a : [];
    var traceContext = getTraceContext(event);
    var traceID = (traceContext && traceContext.trace_id) || '';
    var rootSpanID = (traceContext && traceContext.span_id) || '';
    var rootSpanOpName = (traceContext && traceContext.op) || 'transaction';
    var description = traceContext && traceContext.description;
    var parentSpanID = traceContext && traceContext.parent_span_id;
    if (!spanEntry || spans.length <= 0) {
        return {
            op: rootSpanOpName,
            childSpans: {},
            traceStartTimestamp: event.startTimestamp,
            traceEndTimestamp: event.endTimestamp,
            traceID: traceID,
            rootSpanID: rootSpanID,
            parentSpanID: parentSpanID,
            numOfSpans: 0,
            spans: [],
            description: description,
        };
    }
    // any span may be a parent of another span
    var potentialParents = new Set(spans.map(function (span) {
        return span.span_id;
    }));
    // the root transaction span is a parent of all other spans
    potentialParents.add(rootSpanID);
    // we reduce spans to become an object mapping span ids to their children
    var init = {
        op: rootSpanOpName,
        childSpans: {},
        traceStartTimestamp: event.startTimestamp,
        traceEndTimestamp: event.endTimestamp,
        traceID: traceID,
        rootSpanID: rootSpanID,
        parentSpanID: parentSpanID,
        numOfSpans: spans.length,
        spans: spans,
        description: description,
    };
    var reduced = spans.reduce(function (acc, inputSpan) {
        var _a, _b;
        var span = inputSpan;
        var parentSpanId = getSpanParentSpanID(span);
        var hasParent = parentSpanId && potentialParents.has(parentSpanId);
        if (!isValidSpanID(parentSpanId) || !hasParent) {
            // this span is considered an orphan with respect to the spans within this transaction.
            // although the span is an orphan, it's still a descendant of this transaction,
            // so we set its parent span id to be the root transaction span's id
            span.parent_span_id = rootSpanID;
            span = __assign({ type: 'orphan' }, span);
        }
        assert(span.parent_span_id);
        // get any span children whose parent_span_id is equal to span.parent_span_id,
        // otherwise start with an empty array
        var spanChildren = (_b = (_a = acc.childSpans) === null || _a === void 0 ? void 0 : _a[span.parent_span_id]) !== null && _b !== void 0 ? _b : [];
        spanChildren.push(span);
        set(acc.childSpans, span.parent_span_id, spanChildren);
        // set trace start & end timestamps based on given span's start and end timestamps
        if (!acc.traceStartTimestamp || span.start_timestamp < acc.traceStartTimestamp) {
            acc.traceStartTimestamp = span.start_timestamp;
        }
        // establish trace end timestamp
        var hasEndTimestamp = isNumber(span.timestamp);
        if (!acc.traceEndTimestamp) {
            if (hasEndTimestamp) {
                acc.traceEndTimestamp = span.timestamp;
                return acc;
            }
            acc.traceEndTimestamp = span.start_timestamp;
            return acc;
        }
        if (hasEndTimestamp && span.timestamp > acc.traceEndTimestamp) {
            acc.traceEndTimestamp = span.timestamp;
            return acc;
        }
        if (span.start_timestamp > acc.traceEndTimestamp) {
            acc.traceEndTimestamp = span.start_timestamp;
        }
        return acc;
    }, init);
    // sort span children
    Object.values(reduced.childSpans).forEach(function (spanChildren) {
        spanChildren.sort(sortSpans);
    });
    return reduced;
}
function sortSpans(firstSpan, secondSpan) {
    // orphan spans come after non-ophan spans.
    if (isOrphanSpan(firstSpan) && !isOrphanSpan(secondSpan)) {
        // sort secondSpan before firstSpan
        return 1;
    }
    if (!isOrphanSpan(firstSpan) && isOrphanSpan(secondSpan)) {
        // sort firstSpan before secondSpan
        return -1;
    }
    // sort spans by their start timestamp in ascending order
    if (firstSpan.start_timestamp < secondSpan.start_timestamp) {
        // sort firstSpan before secondSpan
        return -1;
    }
    if (firstSpan.start_timestamp === secondSpan.start_timestamp) {
        return 0;
    }
    // sort secondSpan before firstSpan
    return 1;
}
export function isOrphanTreeDepth(treeDepth) {
    if (typeof treeDepth === 'number') {
        return false;
    }
    return (treeDepth === null || treeDepth === void 0 ? void 0 : treeDepth.type) === 'orphan';
}
export function unwrapTreeDepth(treeDepth) {
    if (isOrphanTreeDepth(treeDepth)) {
        return treeDepth.depth;
    }
    return treeDepth;
}
//# sourceMappingURL=utils.jsx.map