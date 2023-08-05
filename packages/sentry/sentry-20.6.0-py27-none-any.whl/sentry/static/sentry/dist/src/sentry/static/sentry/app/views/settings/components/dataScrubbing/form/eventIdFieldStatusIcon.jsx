import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import ControlState from 'app/views/settings/components/forms/field/controlState';
import { t } from 'app/locale';
import Tooltip from 'app/components/tooltip';
import { IconClose, IconCheckmark } from 'app/icons';
import { EventIdStatus } from '../types';
var EventIdFieldStatusIcon = function (_a) {
    var status = _a.status, onClickIconClose = _a.onClickIconClose;
    switch (status) {
        case EventIdStatus.ERROR:
        case EventIdStatus.INVALID:
        case EventIdStatus.NOT_FOUND:
            return (<CloseIcon onClick={onClickIconClose}>
          <Tooltip title={t('Clear Event ID')}>
            <IconClose color="red"/>
          </Tooltip>
        </CloseIcon>);
        case EventIdStatus.LOADING:
            return <ControlState isSaving/>;
        case EventIdStatus.LOADED:
            return <IconCheckmark color="green"/>;
        default:
            return null;
    }
};
export default EventIdFieldStatusIcon;
var CloseIcon = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  cursor: pointer;\n  :first-child {\n    line-height: 0;\n  }\n"], ["\n  cursor: pointer;\n  :first-child {\n    line-height: 0;\n  }\n"])));
var templateObject_1;
//# sourceMappingURL=eventIdFieldStatusIcon.jsx.map