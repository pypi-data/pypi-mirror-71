import React from 'react';
import EventDataSection from 'app/components/events/eventDataSection';
import Annotated from 'app/components/events/meta/annotated';
import { t } from 'app/locale';
var Sdk = function (_a) {
    var data = _a.event.data;
    return (<EventDataSection type="sdk" title={t('SDK')} wrapTitle>
    <table className="table key-value">
      <tbody>
        <tr key="name">
          <td className="key">{t('Name')}</td>
          <td className="value">
            <Annotated object={data} objectKey="name">
              {function (value) { return <pre>{value}</pre>; }}
            </Annotated>
          </td>
        </tr>
        <tr key="version">
          <td className="key">{t('Version')}</td>
          <td className="value">
            <Annotated object={data} objectKey="version">
              {function (value) { return <pre>{value}</pre>; }}
            </Annotated>
          </td>
        </tr>
      </tbody>
    </table>
  </EventDataSection>);
};
export default Sdk;
//# sourceMappingURL=sdk.jsx.map