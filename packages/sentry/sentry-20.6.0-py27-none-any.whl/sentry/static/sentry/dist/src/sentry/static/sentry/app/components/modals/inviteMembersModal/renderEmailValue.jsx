import { __makeTemplateObject, __rest } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { css } from '@emotion/core';
import { Value } from 'react-select-legacy';
import InlineSvg from 'app/components/inlineSvg';
import space from 'app/styles/space';
import Tooltip from 'app/components/tooltip';
import LoadingIndicator from 'app/components/loadingIndicator';
function renderEmailValue(status, valueProps) {
    var children = valueProps.children, props = __rest(valueProps, ["children"]);
    var error = status && status.error;
    var emailLabel = status === undefined ? (children) : (<Tooltip disabled={!error} title={error}>
        <EmailLabel>
          {children}
          {!status.sent && !status.error && <SendingIndicator />}
          {status.error && <InlineSvg src="icon-warning-sm" size="10px"/>}
          {status.sent && <InlineSvg src="icon-checkmark-sm" size="10px"/>}
        </EmailLabel>
      </Tooltip>);
    return (<EmailValue status={status}>
      <Value {...props}>{emailLabel}</Value>
    </EmailValue>);
}
var EmailValue = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: initial;\n\n  .Select--multi.is-disabled & .Select-value {\n    ", ";\n  }\n\n  .Select-value ", " {\n    color: ", ";\n  }\n"], ["\n  display: initial;\n\n  .Select--multi.is-disabled & .Select-value {\n    ",
    ";\n  }\n\n  .Select-value ", " {\n    color: ", ";\n  }\n"])), function (p) {
    return p.status &&
        p.status.error && css(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n        color: ", ";\n        border-color: ", ";\n        background-color: ", ";\n      "], ["\n        color: ", ";\n        border-color: ", ";\n        background-color: ", ";\n      "])), p.theme.red, p.theme.redLight, p.theme.redLightest);
}, InlineSvg, function (p) { return (p.status && p.status.sent ? p.theme.green400 : 'inherit'); });
var EmailLabel = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: inline-grid;\n  grid-auto-flow: column;\n  grid-gap: ", ";\n  align-items: center;\n"], ["\n  display: inline-grid;\n  grid-auto-flow: column;\n  grid-gap: ", ";\n  align-items: center;\n"])), space(0.5));
var SendingIndicator = styled(LoadingIndicator)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  margin: 0;\n  .loading-indicator {\n    border-width: 2px;\n  }\n"], ["\n  margin: 0;\n  .loading-indicator {\n    border-width: 2px;\n  }\n"])));
SendingIndicator.defaultProps = {
    hideMessage: true,
    size: 14,
};
export default renderEmailValue;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=renderEmailValue.jsx.map