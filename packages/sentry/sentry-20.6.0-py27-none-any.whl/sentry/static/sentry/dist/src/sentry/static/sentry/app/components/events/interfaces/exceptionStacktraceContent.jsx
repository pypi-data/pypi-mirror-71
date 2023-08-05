import React from 'react';
import { defined } from 'app/utils';
import StacktraceContent from 'app/components/events/interfaces/stacktraceContent';
import { Panel } from 'app/components/panels';
import EmptyMessage from 'app/views/settings/components/emptyMessage';
var ExceptionStacktraceContent = function (_a) {
    var stackView = _a.stackView, stacktrace = _a.stacktrace, platform = _a.platform, newestFirst = _a.newestFirst, data = _a.data, expandFirstFrame = _a.expandFirstFrame, event = _a.event;
    if (!defined(stacktrace)) {
        return null;
    }
    if (stackView === 'app' &&
        stacktrace.frames.filter(function (frame) { return frame.inApp; }).length === 0) {
        return (<Panel dashedBorder>
        <EmptyMessage icon="icon-warning-sm" title="No app only stacktrace has been found!"/>
      </Panel>);
    }
    return (<StacktraceContent data={data} expandFirstFrame={expandFirstFrame} includeSystemFrames={stackView === 'full'} platform={platform} newestFirst={newestFirst} event={event}/>);
};
export default ExceptionStacktraceContent;
//# sourceMappingURL=exceptionStacktraceContent.jsx.map