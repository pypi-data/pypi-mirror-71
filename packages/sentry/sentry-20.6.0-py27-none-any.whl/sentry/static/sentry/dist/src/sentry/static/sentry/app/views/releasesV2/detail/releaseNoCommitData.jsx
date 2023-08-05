import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { t } from 'app/locale';
import space from 'app/styles/space';
import Button from 'app/components/button';
import Well from 'app/components/well';
import { IconCommit } from 'app/icons';
var ReleaseNoCommitData = function (_a) {
    var orgId = _a.orgId;
    return (<StyledWell centered>
    <IconCommit size="xl"/>
    <h5>{t('Releases are better with commit data!')}</h5>
    <p>
      {t('Connect a repository to see commit info, files changed, and authors involved in future releases.')}
    </p>
    <Button priority="primary" to={"/settings/" + orgId + "/repos/"}>
      {t('Connect a repository')}
    </Button>
  </StyledWell>);
};
var StyledWell = styled(Well)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  background-color: ", ";\n  padding-top: ", ";\n  padding-bottom: ", ";\n"], ["\n  background-color: ", ";\n  padding-top: ", ";\n  padding-bottom: ", ";\n"])), function (p) { return p.theme.white; }, space(2), space(4));
export default ReleaseNoCommitData;
var templateObject_1;
//# sourceMappingURL=releaseNoCommitData.jsx.map