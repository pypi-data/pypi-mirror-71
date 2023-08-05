import React from 'react';
import CrumbTable from 'app/components/events/interfaces/breadcrumbs/crumbTable';
import SummaryLine from 'app/components/events/interfaces/breadcrumbs/summaryLine';
import { getMeta } from 'app/components/events/meta/metaProxy';
import getBreadcrumbCustomRendererValue from './getBreadcrumbCustomRendererValue';
var DefaultRenderer = function (_a) {
    var breadcrumb = _a.breadcrumb;
    return (<CrumbTable breadcrumb={breadcrumb} summary={<SummaryLine>
        {(breadcrumb === null || breadcrumb === void 0 ? void 0 : breadcrumb.message) && (<pre>
            <code>
              {getBreadcrumbCustomRendererValue({
        value: breadcrumb.message,
        meta: getMeta(breadcrumb, 'message'),
    })}
            </code>
          </pre>)}
      </SummaryLine>} kvData={breadcrumb.data}/>);
};
export default DefaultRenderer;
//# sourceMappingURL=defaultRenderer.jsx.map