import React from 'react';
import ContextBlock from 'app/components/events/contexts/contextBlock';
import getOperatingSystemKnownData from './getOperatingSystemKnownData';
import { OperatingSystemKnownDataType } from './types';
var operatingSystemKnownDataValues = [
    OperatingSystemKnownDataType.NAME,
    OperatingSystemKnownDataType.VERSION,
    OperatingSystemKnownDataType.KERNEL_VERSION,
    OperatingSystemKnownDataType.ROOTED,
];
var OperatingSystem = function (_a) {
    var data = _a.data;
    return (<ContextBlock knownData={getOperatingSystemKnownData(data, operatingSystemKnownDataValues)}/>);
};
export default OperatingSystem;
//# sourceMappingURL=operatingSystem.jsx.map