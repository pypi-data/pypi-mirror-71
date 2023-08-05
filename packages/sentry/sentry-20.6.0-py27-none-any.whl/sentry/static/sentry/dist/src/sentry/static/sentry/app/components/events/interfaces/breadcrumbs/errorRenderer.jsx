import React from 'react';
import omit from 'lodash/omit';
import CrumbTable from 'app/components/events/interfaces/breadcrumbs/crumbTable';
import SummaryLine from 'app/components/events/interfaces/breadcrumbs/summaryLine';
import { getMeta } from 'app/components/events/meta/metaProxy';
import { defined } from 'app/utils';
import getBreadcrumbCustomRendererValue from './getBreadcrumbCustomRendererValue';
var ErrorRenderer = function (_a) {
    var breadcrumb = _a.breadcrumb;
    var data = breadcrumb.data;
    return (<CrumbTable breadcrumb={breadcrumb} summary={<SummaryLine>
          <pre>
            <code>
              {(data === null || data === void 0 ? void 0 : data.type) &&
        getBreadcrumbCustomRendererValue({
            value: <strong>{data.type + ": "}</strong>,
            meta: getMeta(data, 'type'),
        })}
              {defined(data) &&
        defined(data === null || data === void 0 ? void 0 : data.value) &&
        getBreadcrumbCustomRendererValue({
            value: (breadcrumb === null || breadcrumb === void 0 ? void 0 : breadcrumb.message) ? data.value + ". " : data.value,
            meta: getMeta(data, 'value'),
        })}
              {(breadcrumb === null || breadcrumb === void 0 ? void 0 : breadcrumb.message) &&
        getBreadcrumbCustomRendererValue({
            value: breadcrumb.message,
            meta: getMeta(breadcrumb, 'message'),
        })}
            </code>
          </pre>
        </SummaryLine>} kvData={omit(data, ['type', 'value'])}/>);
};
export default ErrorRenderer;
//# sourceMappingURL=errorRenderer.jsx.map