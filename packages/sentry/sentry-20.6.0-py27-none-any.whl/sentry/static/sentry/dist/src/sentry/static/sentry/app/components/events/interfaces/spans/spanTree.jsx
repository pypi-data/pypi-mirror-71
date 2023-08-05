import { __extends, __makeTemplateObject, __read, __spread } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { t } from 'app/locale';
import { boundsGenerator, pickSpanBarColour, generateRootSpan, getSpanID, getSpanOperation, getSpanTraceID, isGapSpan, isOrphanSpan, } from './utils';
import SpanGroup from './spanGroup';
import { SpanRowMessage } from './styles';
import * as DividerHandlerManager from './dividerHandlerManager';
var SpanTree = /** @class */ (function (_super) {
    __extends(SpanTree, _super);
    function SpanTree() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.traceViewRef = React.createRef();
        _this.renderSpan = function (_a) {
            var spanNumber = _a.spanNumber, isRoot = _a.isRoot, isLast = _a.isLast, treeDepth = _a.treeDepth, continuingTreeDepths = _a.continuingTreeDepths, numOfSpansOutOfViewAbove = _a.numOfSpansOutOfViewAbove, numOfFilteredSpansAbove = _a.numOfFilteredSpansAbove, childSpans = _a.childSpans, span = _a.span, generateBounds = _a.generateBounds, previousSiblingEndTimestamp = _a.previousSiblingEndTimestamp;
            var _b, _c;
            var _d = _this.props, orgId = _d.orgId, eventView = _d.eventView, event = _d.event, spansWithErrors = _d.spansWithErrors, organization = _d.organization;
            var spanBarColour = pickSpanBarColour(getSpanOperation(span));
            var spanChildren = (_b = childSpans === null || childSpans === void 0 ? void 0 : childSpans[getSpanID(span)]) !== null && _b !== void 0 ? _b : [];
            var bounds = generateBounds({
                startTimestamp: span.start_timestamp,
                endTimestamp: span.timestamp,
            });
            var isCurrentSpanHidden = !bounds.isSpanVisibleInView;
            var isCurrentSpanFilteredOut = isGapSpan(span)
                ? false
                : _this.isSpanFilteredOut(span);
            var isSpanDisplayed = !isCurrentSpanHidden && !isCurrentSpanFilteredOut;
            // hide gap spans (i.e. "missing instrumentation" spans) for browser js transactions,
            // since they're not useful to indicate
            var shouldIncludeGap = !isJavaScriptSDK((_c = event.sdk) === null || _c === void 0 ? void 0 : _c.name);
            var isValidGap = typeof previousSiblingEndTimestamp === 'number' &&
                previousSiblingEndTimestamp < span.start_timestamp &&
                // gap is at least 100 ms
                span.start_timestamp - previousSiblingEndTimestamp >= 0.1 &&
                shouldIncludeGap;
            var spanGroupNumber = isValidGap && isSpanDisplayed ? spanNumber + 1 : spanNumber;
            var treeDepthEntry = isOrphanSpan(span)
                ? { type: 'orphan', depth: treeDepth }
                : treeDepth;
            var treeArr = isLast
                ? continuingTreeDepths
                : __spread(continuingTreeDepths, [treeDepthEntry]);
            var reduced = spanChildren.reduce(function (acc, spanChild, index) {
                var key = "" + getSpanTraceID(span) + getSpanID(spanChild);
                var results = _this.renderSpan({
                    spanNumber: acc.nextSpanNumber,
                    isLast: index + 1 === spanChildren.length,
                    continuingTreeDepths: treeArr,
                    treeDepth: treeDepth + 1,
                    numOfSpansOutOfViewAbove: acc.numOfSpansOutOfViewAbove,
                    numOfFilteredSpansAbove: acc.numOfFilteredSpansAbove,
                    span: spanChild,
                    childSpans: childSpans,
                    generateBounds: generateBounds,
                    previousSiblingEndTimestamp: acc.previousSiblingEndTimestamp,
                });
                acc.renderedSpanChildren.push(<React.Fragment key={key}>{results.spanTree}</React.Fragment>);
                acc.numOfSpansOutOfViewAbove = results.numOfSpansOutOfViewAbove;
                acc.numOfFilteredSpansAbove = results.numOfFilteredSpansAbove;
                acc.nextSpanNumber = results.nextSpanNumber;
                acc.previousSiblingEndTimestamp = spanChild.timestamp;
                return acc;
            }, {
                renderedSpanChildren: [],
                nextSpanNumber: spanGroupNumber + 1,
                numOfSpansOutOfViewAbove: isCurrentSpanHidden ? numOfSpansOutOfViewAbove + 1 : 0,
                numOfFilteredSpansAbove: isCurrentSpanFilteredOut
                    ? numOfFilteredSpansAbove + 1
                    : isCurrentSpanHidden
                        ? numOfFilteredSpansAbove
                        : 0,
                previousSiblingEndTimestamp: undefined,
            });
            var infoMessage = _this.generateInfoMessage({
                isCurrentSpanHidden: isCurrentSpanHidden,
                numOfSpansOutOfViewAbove: numOfSpansOutOfViewAbove,
                isCurrentSpanFilteredOut: isCurrentSpanFilteredOut,
                numOfFilteredSpansAbove: numOfFilteredSpansAbove,
            });
            var spanGap = {
                type: 'gap',
                start_timestamp: previousSiblingEndTimestamp || span.start_timestamp,
                timestamp: span.start_timestamp,
                description: t('Missing instrumentation'),
                isOrphan: isOrphanSpan(span),
            };
            var spanGapComponent = isValidGap && isSpanDisplayed ? (<SpanGroup eventView={eventView} orgId={orgId} organization={organization} event={event} spanNumber={spanNumber} isLast={false} continuingTreeDepths={continuingTreeDepths} isRoot={isRoot} span={spanGap} trace={_this.props.trace} generateBounds={generateBounds} treeDepth={treeDepth} numOfSpanChildren={0} renderedSpanChildren={[]} isCurrentSpanFilteredOut={isCurrentSpanFilteredOut} spansWithErrors={spansWithErrors} spanBarHatch/>) : null;
            return {
                numOfSpansOutOfViewAbove: reduced.numOfSpansOutOfViewAbove,
                numOfFilteredSpansAbove: reduced.numOfFilteredSpansAbove,
                nextSpanNumber: reduced.nextSpanNumber,
                spanTree: (<React.Fragment>
          {infoMessage}
          {spanGapComponent}
          <SpanGroup eventView={eventView} orgId={orgId} organization={organization} event={event} spanNumber={spanGroupNumber} isLast={isLast} continuingTreeDepths={continuingTreeDepths} isRoot={isRoot} span={span} trace={_this.props.trace} generateBounds={generateBounds} treeDepth={treeDepth} numOfSpanChildren={spanChildren.length} renderedSpanChildren={reduced.renderedSpanChildren} spanBarColour={spanBarColour} isCurrentSpanFilteredOut={isCurrentSpanFilteredOut} spanBarHatch={false} spansWithErrors={spansWithErrors}/>
        </React.Fragment>),
            };
        };
        _this.renderRootSpan = function () {
            var _a = _this.props, dragProps = _a.dragProps, trace = _a.trace;
            var rootSpan = generateRootSpan(trace);
            var generateBounds = boundsGenerator({
                traceStartTimestamp: trace.traceStartTimestamp,
                traceEndTimestamp: trace.traceEndTimestamp,
                viewStart: dragProps.viewWindowStart,
                viewEnd: dragProps.viewWindowEnd,
            });
            return _this.renderSpan({
                isRoot: true,
                isLast: true,
                spanNumber: 1,
                treeDepth: 0,
                continuingTreeDepths: [],
                numOfSpansOutOfViewAbove: 0,
                numOfFilteredSpansAbove: 0,
                span: rootSpan,
                childSpans: trace.childSpans,
                generateBounds: generateBounds,
                previousSiblingEndTimestamp: undefined,
            });
        };
        return _this;
    }
    SpanTree.prototype.shouldComponentUpdate = function (nextProps) {
        if (nextProps.dragProps.isDragging || nextProps.dragProps.isWindowSelectionDragging) {
            return false;
        }
        return true;
    };
    SpanTree.prototype.generateInfoMessage = function (input) {
        var isCurrentSpanHidden = input.isCurrentSpanHidden, numOfSpansOutOfViewAbove = input.numOfSpansOutOfViewAbove, isCurrentSpanFilteredOut = input.isCurrentSpanFilteredOut, numOfFilteredSpansAbove = input.numOfFilteredSpansAbove;
        var messages = [];
        var showHiddenSpansMessage = !isCurrentSpanHidden && numOfSpansOutOfViewAbove > 0;
        if (showHiddenSpansMessage) {
            messages.push(<span key="spans-out-of-view">
          <strong>{numOfSpansOutOfViewAbove}</strong> {t('spans out of view')}
        </span>);
        }
        var showFilteredSpansMessage = !isCurrentSpanFilteredOut && numOfFilteredSpansAbove > 0;
        if (showFilteredSpansMessage) {
            if (!isCurrentSpanHidden) {
                messages.push(<span key="spans-filtered">
            <strong>{numOfFilteredSpansAbove}</strong> {t('spans filtered out')}
          </span>);
            }
        }
        if (messages.length <= 0) {
            return null;
        }
        return <SpanRowMessage>{messages}</SpanRowMessage>;
    };
    SpanTree.prototype.isSpanFilteredOut = function (span) {
        var filterSpans = this.props.filterSpans;
        if (!filterSpans) {
            return false;
        }
        return !filterSpans.spanIDs.has(getSpanID(span));
    };
    SpanTree.prototype.render = function () {
        var _a = this.renderRootSpan(), spanTree = _a.spanTree, numOfSpansOutOfViewAbove = _a.numOfSpansOutOfViewAbove, numOfFilteredSpansAbove = _a.numOfFilteredSpansAbove;
        var infoMessage = this.generateInfoMessage({
            isCurrentSpanHidden: false,
            numOfSpansOutOfViewAbove: numOfSpansOutOfViewAbove,
            isCurrentSpanFilteredOut: false,
            numOfFilteredSpansAbove: numOfFilteredSpansAbove,
        });
        return (<DividerHandlerManager.Provider interactiveLayerRef={this.traceViewRef}>
        <TraceViewContainer ref={this.traceViewRef}>
          {spanTree}
          {infoMessage}
        </TraceViewContainer>
      </DividerHandlerManager.Provider>);
    };
    return SpanTree;
}(React.Component));
var TraceViewContainer = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  overflow-x: hidden;\n  border-bottom-left-radius: 3px;\n  border-bottom-right-radius: 3px;\n"], ["\n  overflow-x: hidden;\n  border-bottom-left-radius: 3px;\n  border-bottom-right-radius: 3px;\n"])));
function isJavaScriptSDK(sdkName) {
    if (!sdkName) {
        return false;
    }
    // based on https://github.com/getsentry/sentry-javascript/blob/master/packages/browser/src/version.ts
    return sdkName.toLowerCase() === 'sentry.javascript.browser';
}
export default SpanTree;
var templateObject_1;
//# sourceMappingURL=spanTree.jsx.map