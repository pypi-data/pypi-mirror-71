import React from 'react';
import Category from 'app/components/events/interfaces/breadcrumbs/category';
import { getMeta } from 'app/components/events/meta/metaProxy';
import getBreadcrumbCustomRendererValue from './getBreadcrumbCustomRendererValue';
var CrumbTable = function (_a) {
    var children = _a.children, kvData = _a.kvData, breadcrumb = _a.breadcrumb, summary = _a.summary;
    var renderData = function () {
        if (!kvData) {
            return null;
        }
        return Object.keys(kvData).map(function (key) { return (<tr key={key}>
        <td className="key">{key}</td>
        <td className="value">
          <pre>
            {getBreadcrumbCustomRendererValue({
            value: typeof kvData[key] === 'object'
                ? JSON.stringify(kvData[key])
                : kvData[key],
            meta: getMeta(kvData, key),
        })}
          </pre>
        </td>
      </tr>); });
    };
    return (<table className="table key-value">
      <thead>
        <tr>
          <td className="key">
            <Category value={breadcrumb.category}/>
          </td>
          <td className="value">{summary}</td>
        </tr>
      </thead>
      <tbody>
        {children}
        {renderData()}
      </tbody>
    </table>);
};
export default CrumbTable;
//# sourceMappingURL=crumbTable.jsx.map