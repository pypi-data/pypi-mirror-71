import React from 'react';
import ContextBlock from 'app/components/events/contexts/contextBlock';
import getRuntimeKnownData from './getRuntimeKnownData';
import { RuntimeKnownDataType } from './types';
var runTimerKnownDataValues = [RuntimeKnownDataType.NAME, RuntimeKnownDataType.VERSION];
var Runtime = function (_a) {
    var data = _a.data;
    return (<ContextBlock knownData={getRuntimeKnownData(data, runTimerKnownDataValues)}/>);
};
export default Runtime;
//# sourceMappingURL=runtime.jsx.map