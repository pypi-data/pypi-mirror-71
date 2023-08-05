import React from 'react';
import ContextBlock from 'app/components/events/contexts/contextBlock';
import getOperatingSystemKnownData from './getGPUKnownData';
import { GPUKnownDataType } from './types';
var gpuKnownDataValues = [
    GPUKnownDataType.NAME,
    GPUKnownDataType.VERSION,
    GPUKnownDataType.VENDOR_NAME,
    GPUKnownDataType.MEMORY,
    GPUKnownDataType.NPOT_SUPPORT,
    GPUKnownDataType.MULTI_THREAD_RENDERING,
    GPUKnownDataType.API_TYPE,
];
var GPU = function (_a) {
    var data = _a.data;
    if (data.vendor_id > 0) {
        gpuKnownDataValues.unshift[GPUKnownDataType.VENDOR_ID];
    }
    if (data.id > 0) {
        gpuKnownDataValues.unshift[GPUKnownDataType.ID];
    }
    return (<ContextBlock knownData={getOperatingSystemKnownData(data, gpuKnownDataValues)}/>);
};
export default GPU;
//# sourceMappingURL=gpu.jsx.map