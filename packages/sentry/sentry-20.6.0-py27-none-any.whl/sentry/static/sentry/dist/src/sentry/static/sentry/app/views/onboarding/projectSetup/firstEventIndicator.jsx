import { __makeTemplateObject, __rest } from "tslib";
import React from 'react';
import posed, { PoseGroup } from 'react-pose';
import styled from '@emotion/styled';
import { t } from 'app/locale';
import Button from 'app/components/button';
import EventWaiter from 'app/utils/eventWaiter';
import InlineSvg from 'app/components/inlineSvg';
import space from 'app/styles/space';
import testablePose from 'app/utils/testablePose';
import pulsingIndicatorStyles from 'app/styles/pulsingIndicator';
var FirstEventIndicator = function (props) { return (<EventWaiter {...props}>
    {function (_a) {
    var firstIssue = _a.firstIssue;
    return <Indicator firstIssue={firstIssue} {...props}/>;
}}
  </EventWaiter>); };
var Indicator = function (_a) {
    var firstIssue = _a.firstIssue, props = __rest(_a, ["firstIssue"]);
    return (<PoseGroup preEnterPose="init">
    {!firstIssue ? (<Waiting key="waiting"/>) : (<Success key="received" firstIssue={firstIssue} {...props}/>)}
  </PoseGroup>);
};
var StatusWrapper = styled(posed.div(testablePose({ enter: { staggerChildren: 350 } })))(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: max-content 1fr max-content;\n  grid-gap: ", ";\n  align-items: center;\n  font-size: 0.9em;\n  /* This is a minor hack, but the line height is just *slightly* too low,\n  making the text appear off center, so we adjust it just a bit */\n  line-height: calc(0.9em + 1px);\n  /* Ensure the event waiter status is always the height of a button */\n  height: ", ";\n"], ["\n  display: grid;\n  grid-template-columns: max-content 1fr max-content;\n  grid-gap: ", ";\n  align-items: center;\n  font-size: 0.9em;\n  /* This is a minor hack, but the line height is just *slightly* too low,\n  making the text appear off center, so we adjust it just a bit */\n  line-height: calc(0.9em + 1px);\n  /* Ensure the event waiter status is always the height of a button */\n  height: ", ";\n"])), space(1), space(4));
var Waiting = function (props) { return (<StatusWrapper {...props}>
    <WaitingIndicator />
    <PosedText>{t('Waiting for verification event')}</PosedText>
  </StatusWrapper>); };
var Success = function (_a) {
    var organization = _a.organization, firstIssue = _a.firstIssue, props = __rest(_a, ["organization", "firstIssue"]);
    return (<StatusWrapper {...props}>
    <ReceivedIndicator src="icon-checkmark-sm"/>
    <PosedText>{t('Event was received!')}</PosedText>
    {firstIssue && firstIssue !== true && (<PosedButton size="small" priority="primary" to={"/organizations/" + organization.slug + "/issues/" + firstIssue.id + "/"}>
        {t('Take me to my event')}
      </PosedButton>)}
  </StatusWrapper>);
};
var indicatorPoses = testablePose({
    init: { opacity: 0, y: -10 },
    enter: { opacity: 1, y: 0 },
    exit: { opacity: 0, y: 10 },
});
var PosedText = posed.div(indicatorPoses);
var WaitingIndicator = styled(posed.div(indicatorPoses))(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  margin: 0 6px;\n  ", ";\n"], ["\n  margin: 0 6px;\n  ", ";\n"])), pulsingIndicatorStyles);
var PosedReceivedIndicator = posed(InlineSvg)(indicatorPoses);
var ReceivedIndicator = styled(PosedReceivedIndicator)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  color: #fff;\n  background: ", ";\n  border-radius: 50%;\n  height: 20px;\n  width: 20px;\n  padding: 5px;\n  margin: 0 2px;\n"], ["\n  color: #fff;\n  background: ", ";\n  border-radius: 50%;\n  height: 20px;\n  width: 20px;\n  padding: 5px;\n  margin: 0 2px;\n"])), function (p) { return p.theme.green400; });
var PosedButton = posed(React.forwardRef(function (props, ref) { return (<div ref={ref}>
      <Button {...props}/>
    </div>); }))(testablePose({
    init: { x: -20, opacity: 0 },
    enter: { x: 0, opacity: 1 },
}));
export { Indicator };
export default FirstEventIndicator;
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=firstEventIndicator.jsx.map