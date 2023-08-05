import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
var HighlightComponent = function (_a) {
    var className = _a.className, children = _a.children, disabled = _a.disabled, text = _a.text;
    if (!text || disabled) {
        return <React.Fragment>{children}</React.Fragment>;
    }
    var highlightText = text.toLowerCase();
    var idx = children.toLowerCase().indexOf(highlightText);
    if (idx === -1) {
        return <React.Fragment>{children}</React.Fragment>;
    }
    return (<React.Fragment>
      {children.substr(0, idx)}
      <span className={className}>{children.substr(idx, highlightText.length)}</span>
      {children.substr(idx + highlightText.length)}
    </React.Fragment>);
};
var Highlight = styled(HighlightComponent)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  font-weight: normal;\n  background-color: ", ";\n  color: ", ";\n"], ["\n  font-weight: normal;\n  background-color: ", ";\n  color: ", ";\n"])), function (p) { return p.theme.yellowLight; }, function (p) { return p.theme.gray700; });
export default Highlight;
export { HighlightComponent };
var templateObject_1;
//# sourceMappingURL=highlight.jsx.map