import React from 'react';
import { t } from 'app/locale';
// TODO(Priscila): Remove BR tags
// mapUrl not always present; e.g. uploaded source maps
var FrameDefaultTitleOriginalSourceInfo = function (_a) {
    var mapUrl = _a.mapUrl, map = _a.map;
    return (<React.Fragment>
    <strong>{t('Source Map')}</strong>
    <br />
    {mapUrl ? mapUrl : map}
    <br />
  </React.Fragment>);
};
export default FrameDefaultTitleOriginalSourceInfo;
//# sourceMappingURL=frameDefaultTitleOriginalSourceInfo.jsx.map