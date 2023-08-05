import { __awaiter, __generator, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { browserHistory } from 'react-router';
import { t } from 'app/locale';
import space from 'app/styles/space';
import Button from 'app/components/button';
import { IconDelete } from 'app/icons';
import Confirm from 'app/components/confirm';
import { addErrorMessage, addLoadingMessage, addSuccessMessage, } from 'app/actionCreators/indicator';
import Tooltip from 'app/components/tooltip';
import { deleteRelease } from './utils';
var ReleaseActions = function (_a) {
    var orgId = _a.orgId, version = _a.version, hasHealthData = _a.hasHealthData;
    var handleDelete = function () { return __awaiter(void 0, void 0, void 0, function () {
        var redirectPath, error_1, errorMessage;
        var _a, _b;
        return __generator(this, function (_c) {
            switch (_c.label) {
                case 0:
                    redirectPath = "/organizations/" + orgId + "/releases/";
                    addLoadingMessage(t('Deleting Release...'));
                    _c.label = 1;
                case 1:
                    _c.trys.push([1, 3, , 4]);
                    return [4 /*yield*/, deleteRelease(orgId, version)];
                case 2:
                    _c.sent();
                    addSuccessMessage(t('Release was successfully removed.'));
                    browserHistory.push(redirectPath);
                    return [3 /*break*/, 4];
                case 3:
                    error_1 = _c.sent();
                    errorMessage = (_b = (_a = error_1.responseJSON) === null || _a === void 0 ? void 0 : _a.detail) !== null && _b !== void 0 ? _b : t('Release could not be be removed.');
                    addErrorMessage(errorMessage);
                    return [3 /*break*/, 4];
                case 4: return [2 /*return*/];
            }
        });
    }); };
    return (<Wrapper>
      <Confirm onConfirm={handleDelete} message={t('Deleting this release is permanent and will affect other projects associated with it. Are you sure you wish to continue?')}>
        <div>
          <Tooltip title={t('You can only delete releases if they have no issues or health data.')} disabled={!hasHealthData}>
            <Button icon={<IconDelete />} disabled={hasHealthData}/>
          </Tooltip>
        </div>
      </Confirm>
    </Wrapper>);
};
var Wrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-auto-flow: column;\n  grid-auto-columns: min-content;\n  grid-gap: ", ";\n\n  @media (max-width: ", ") {\n    width: 100%;\n    margin: ", " 0 ", " 0;\n  }\n"], ["\n  display: grid;\n  grid-auto-flow: column;\n  grid-auto-columns: min-content;\n  grid-gap: ", ";\n\n  @media (max-width: ", ") {\n    width: 100%;\n    margin: ", " 0 ", " 0;\n  }\n"])), space(0.5), function (p) { return p.theme.breakpoints[0]; }, space(1), space(2));
export default ReleaseActions;
var templateObject_1;
//# sourceMappingURL=releaseActions.jsx.map