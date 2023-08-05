import { __rest } from "tslib";
import React from 'react';
import Feature from 'app/components/acl/feature';
import FeatureDisabled from 'app/components/acl/featureDisabled';
import { PanelAlert } from 'app/components/panels';
import { t } from 'app/locale';
import withOrganization from 'app/utils/withOrganization';
import OrganizationSecurityAndPrivacyContent from './organizationSecurityAndPrivacyContent';
var OrganizationSecurityAndPrivacy = function (_a) {
    var organization = _a.organization, props = __rest(_a, ["organization"]);
    return (<Feature features={['datascrubbers-v2']} organization={organization} renderDisabled={function () { return (<FeatureDisabled alert={PanelAlert} features={organization.features} featureName={t('Security & Privacy - new')}/>); }}>
    <OrganizationSecurityAndPrivacyContent {...props} organization={organization}/>
  </Feature>);
};
export default withOrganization(OrganizationSecurityAndPrivacy);
//# sourceMappingURL=organizationSecurityAndPrivacy.jsx.map