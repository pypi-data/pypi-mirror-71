import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import space from 'app/styles/space';
import video from 'app/../images/spot/congrats-robots.mp4';
/**
 * Note, video needs `muted` for `autoplay` to work on Chrome
 * See https://developer.mozilla.org/en-US/docs/Web/HTML/Element/video
 */
var CongratsRobots = function () { return (<AnimatedScene>
    <StyledVideo autoPlay loop muted>
      <source src={video} type="video/mp4"/>
    </StyledVideo>
  </AnimatedScene>); };
export default CongratsRobots;
var AnimatedScene = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  max-width: 800px;\n"], ["\n  max-width: 800px;\n"])));
var StyledVideo = styled('video')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  max-height: 320px;\n  max-width: 100%;\n  margin-bottom: ", ";\n"], ["\n  max-height: 320px;\n  max-width: 100%;\n  margin-bottom: ", ";\n"])), space(1));
var templateObject_1, templateObject_2;
//# sourceMappingURL=congratsRobots.jsx.map