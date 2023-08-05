import React from 'react';
import { t } from 'app/locale';
import Button from 'app/components/button';
import { IconReleases } from 'app/icons';
import { switchReleasesVersion } from './index';
var SwitchReleasesButton = function (_a) {
    var orgId = _a.orgId, version = _a.version;
    var switchReleases = function () {
        switchReleasesVersion(version, orgId);
    };
    if (version === '2') {
        return (<Button priority="primary" size="small" icon={<IconReleases size="sm"/>} onClick={switchReleases}>
        {t('Go to New Releases')}
      </Button>);
    }
    return (<div>
      <Button priority="link" size="small" onClick={switchReleases}>
        {t('Go to Legacy Releases')}
      </Button>
    </div>);
};
export default SwitchReleasesButton;
//# sourceMappingURL=switchReleasesButton.jsx.map