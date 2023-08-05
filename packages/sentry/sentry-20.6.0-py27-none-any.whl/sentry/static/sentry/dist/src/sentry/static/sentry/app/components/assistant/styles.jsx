import { __makeTemplateObject, __rest } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import InlineSvg from 'app/components/inlineSvg';
import space from 'app/styles/space';
/* styles common to the guide and support cue/drawer. */
var AssistantContainer = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  position: fixed;\n  z-index: ", ";\n  width: 25vw;\n  max-width: 450px;\n  min-width: 300px;\n  min-height: 40px;\n  bottom: 1vw;\n  border-radius: ", ";\n  box-shadow: ", ";\n  padding: ", ";\n"], ["\n  position: fixed;\n  z-index: ", ";\n  width: 25vw;\n  max-width: 450px;\n  min-width: 300px;\n  min-height: 40px;\n  bottom: 1vw;\n  border-radius: ", ";\n  box-shadow: ", ";\n  padding: ", ";\n"])), function (p) { return p.theme.zIndex.modal; }, function (p) { return p.theme.borderRadius; }, function (p) { return p.theme.dropShadowHeavy; }, space(2));
var CueContainer = styled(AssistantContainer)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  cursor: pointer;\n  max-width: none;\n  min-width: 0;\n  width: auto;\n  height: 2.75em;\n"], ["\n  display: flex;\n  align-items: center;\n  cursor: pointer;\n  max-width: none;\n  min-width: 0;\n  width: auto;\n  height: 2.75em;\n"])));
var CueIcon = styled(function (_a) {
    var hasGuide = _a.hasGuide, props = __rest(_a, ["hasGuide"]);
    return (<InlineSvg src={hasGuide ? 'icon-circle-exclamation' : 'icon-circle-question'} {...props}/>);
})(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  width: 1.33em;\n  height: 1.33em;\n"], ["\n  width: 1.33em;\n  height: 1.33em;\n"])));
var CloseIcon = styled(function (props) { return <InlineSvg src="icon-close-lg" {...props}/>; })(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  stroke-width: 3px;\n  width: 0.75em;\n  height: 0.75em;\n  margin: 0 0 0 ", ";\n  cursor: pointer;\n"], ["\n  stroke-width: 3px;\n  width: 0.75em;\n  height: 0.75em;\n  margin: 0 0 0 ", ";\n  cursor: pointer;\n"])), space(1.5));
var CueText = styled('span')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  overflow: hidden;\n  transition: 0.2s all;\n  white-space: nowrap;\n"], ["\n  overflow: hidden;\n  transition: 0.2s all;\n  white-space: nowrap;\n"])));
export { AssistantContainer, CueContainer, CueIcon, CueText, CloseIcon };
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=styles.jsx.map