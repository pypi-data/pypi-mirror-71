import React from 'react';
import Default from './default';
import Exception from './exception';
import Http from './http';
import { BreadcrumbType } from '../types';
var Data = function (_a) {
    var breadcrumb = _a.breadcrumb, event = _a.event, orgId = _a.orgId;
    if (breadcrumb.type === BreadcrumbType.HTTP) {
        return <Http breadcrumb={breadcrumb}/>;
    }
    if (breadcrumb.type === BreadcrumbType.WARNING ||
        breadcrumb.type === BreadcrumbType.ERROR) {
        return <Exception breadcrumb={breadcrumb}/>;
    }
    return <Default event={event} orgId={orgId} breadcrumb={breadcrumb}/>;
};
export default Data;
//# sourceMappingURL=data.jsx.map