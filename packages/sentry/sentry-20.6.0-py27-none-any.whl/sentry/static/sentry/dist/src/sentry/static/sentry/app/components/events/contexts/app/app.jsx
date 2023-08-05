import React from 'react';
import ContextBlock from 'app/components/events/contexts/contextBlock';
import getAppKnownData from './getAppKnownData';
import { AppKnownDataType } from './types';
var appKnownDataValues = [
    AppKnownDataType.ID,
    AppKnownDataType.START_TIME,
    AppKnownDataType.DEVICE_HASH,
    AppKnownDataType.IDENTIFIER,
    AppKnownDataType.NAME,
    AppKnownDataType.VERSION,
    AppKnownDataType.BUILD,
];
var App = function (_a) {
    var data = _a.data;
    return (<ContextBlock knownData={getAppKnownData(data, appKnownDataValues)}/>);
};
export default App;
//# sourceMappingURL=app.jsx.map