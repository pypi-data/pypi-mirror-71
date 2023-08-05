import { __assign, __makeTemplateObject, __rest } from "tslib";
import PropTypes from 'prop-types';
import React from 'react';
import styled from '@emotion/styled';
import Alert from 'app/components/alert';
var DEFAULT_ICONS = {
    info: 'icon-circle-info',
    error: 'icon-circle-close',
    warning: 'icon-circle-exclamation',
    success: 'icon-circle-success',
};
// Margin bottom should probably be a different prop
var PanelAlert = styled(function (_a) {
    var icon = _a.icon, props = __rest(_a, ["icon"]);
    return (<Alert {...props} icon={icon || DEFAULT_ICONS[props.type]} system/>);
})(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin: 0 0 1px 0;\n  border-radius: 0;\n"], ["\n  margin: 0 0 1px 0;\n  border-radius: 0;\n"])));
PanelAlert.propTypes = __assign(__assign({}, Alert.propTypes), { type: PropTypes.oneOf(['info', 'warning', 'success', 'error', 'muted']) });
export default PanelAlert;
var templateObject_1;
//# sourceMappingURL=panelAlert.jsx.map