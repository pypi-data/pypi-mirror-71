import React from 'react';
import ErrorBoundary from 'app/components/errorBoundary';
import KeyValueList from 'app/components/events/interfaces/keyValueList/keyValueListV2';
var ContextBlock = function (_a) {
    var knownData = _a.knownData, _b = _a.raw, raw = _b === void 0 ? false : _b;
    if (knownData.length === 0) {
        return null;
    }
    return (<ErrorBoundary mini>
      <KeyValueList data={knownData} raw={raw} isContextData/>
    </ErrorBoundary>);
};
export default ContextBlock;
//# sourceMappingURL=contextBlock.jsx.map