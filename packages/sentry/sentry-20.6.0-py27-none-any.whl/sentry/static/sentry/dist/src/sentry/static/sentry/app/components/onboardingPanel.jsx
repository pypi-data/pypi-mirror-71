import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { Panel } from 'app/components/panels';
import space from 'app/styles/space';
function OnboardingPanel(_a) {
    var className = _a.className, image = _a.image, children = _a.children;
    return (<Panel className={className}>
      <Container>
        <IllustrationContainer>{image}</IllustrationContainer>
        <StyledBox>{children}</StyledBox>
      </Container>
    </Panel>);
}
var Container = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  flex-wrap: wrap;\n  min-height: 450px;\n  padding: ", " ", ";\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  flex-wrap: wrap;\n  min-height: 450px;\n  padding: ", " ", ";\n"])), space(1), space(4));
var StyledBox = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  flex: 1;\n  padding: ", ";\n"], ["\n  flex: 1;\n  padding: ", ";\n"])), space(3));
var IllustrationContainer = styled(StyledBox)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: center;\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: center;\n"])));
export default OnboardingPanel;
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=onboardingPanel.jsx.map