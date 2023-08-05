import React from 'react';
import omit from 'lodash/omit';
import CrumbTable from 'app/components/events/interfaces/breadcrumbs/crumbTable';
import SummaryLine from 'app/components/events/interfaces/breadcrumbs/summaryLine';
import ExternalLink from 'app/components/links/externalLink';
import { getMeta } from 'app/components/events/meta/metaProxy';
import { t } from 'app/locale';
import { defined } from 'app/utils';
import getBreadcrumbCustomRendererValue from './getBreadcrumbCustomRendererValue';
var HttpRenderer = function (_a) {
    var breadcrumb = _a.breadcrumb;
    var data = breadcrumb.data;
    var renderUrl = function (url) {
        if (typeof url === 'string') {
            return url.match(/^https?:\/\//) ? (<ExternalLink data-test-id="http-renderer-external-link" href={url}>
          {url}
        </ExternalLink>) : (<span>{url}</span>);
        }
        try {
            return JSON.stringify(url);
        }
        catch (_a) {
            return t('Invalid URL');
        }
    };
    return (<CrumbTable breadcrumb={breadcrumb} summary={<SummaryLine>
          <pre>
            <code>
              {(data === null || data === void 0 ? void 0 : data.method) &&
        getBreadcrumbCustomRendererValue({
            value: <strong>{data.method + " "}</strong>,
            meta: getMeta(data, 'method'),
        })}
              {(data === null || data === void 0 ? void 0 : data.url) &&
        getBreadcrumbCustomRendererValue({
            value: renderUrl(data.url),
            meta: getMeta(data, 'url'),
        })}
              {defined(data) &&
        defined(data.status_code) &&
        getBreadcrumbCustomRendererValue({
            value: (<span data-test-id="http-renderer-status-code">{" [" + data.status_code + "]"}</span>),
            meta: getMeta(data, 'status_code'),
        })}
            </code>
          </pre>
        </SummaryLine>} kvData={omit(data, ['method', 'url', 'status_code'])}/>);
};
export default HttpRenderer;
//# sourceMappingURL=httpRenderer.jsx.map