import React from 'react';
import omit from 'lodash/omit';
import { getMeta } from 'app/components/events/meta/metaProxy';
import { defined } from 'app/utils';
import getBreadcrumbCustomRendererValue from '../../breadcrumbs/getBreadcrumbCustomRendererValue';
import Summary from './summary';
var Exception = function (_a) {
    var breadcrumb = _a.breadcrumb;
    var data = breadcrumb.data;
    var dataValue = data === null || data === void 0 ? void 0 : data.value;
    return (<Summary kvData={omit(data, ['type', 'value'])}>
      {(data === null || data === void 0 ? void 0 : data.type) &&
        getBreadcrumbCustomRendererValue({
            value: <strong>{data.type + ": "}</strong>,
            meta: getMeta(data, 'type'),
        })}
      {defined(dataValue) &&
        getBreadcrumbCustomRendererValue({
            value: (breadcrumb === null || breadcrumb === void 0 ? void 0 : breadcrumb.message) ? dataValue + ". " : dataValue,
            meta: getMeta(data, 'value'),
        })}
      {(breadcrumb === null || breadcrumb === void 0 ? void 0 : breadcrumb.message) &&
        getBreadcrumbCustomRendererValue({
            value: breadcrumb.message,
            meta: getMeta(breadcrumb, 'message'),
        })}
    </Summary>);
};
export default Exception;
//# sourceMappingURL=exception.jsx.map