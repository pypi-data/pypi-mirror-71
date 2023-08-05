import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import minified from 'sentry-dreamy-components/dist/minified.svg';
import emails from 'sentry-dreamy-components/dist/emails.svg';
import issues from 'sentry-dreamy-components/dist/issues.svg';
import suggestedAssignees from 'sentry-dreamy-components/dist/suggested-assignees.svg';
import contributors from 'sentry-dreamy-components/dist/contributors.svg';
import { t } from 'app/locale';
import { analytics } from 'app/utils/analytics';
import withOrganization from 'app/utils/withOrganization';
import withProject from 'app/utils/withProject';
import ReleaseLandingCard from './releaseLandingCard';
// Currently, we need a fallback because <object> doesn't work in msedge,
// and <img> doesn't work in safari. Hopefully we can choose one soon.
var Illustration = styled(function (_a) {
    var data = _a.data, className = _a.className;
    return (<object data={data} className={className}>
    <img src={data} className={className}/>
  </object>);
})(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  width: 100%;\n  height: 100%;\n"], ["\n  width: 100%;\n  height: 100%;\n"])));
var cards = [
    {
        title: t("You Haven't Set Up Releases!"),
        disclaimer: t('(you made no releases in 30 days)'),
        message: t('Releases provide additional context, with rich commits, so you know which errors were addressed and which were introduced in a release'),
        svg: <Illustration data={contributors}/>,
    },
    {
        title: t('Suspect Commits'),
        message: t('Sentry suggests which commit caused an issue and who is likely responsible so you can triage'),
        svg: <Illustration data={suggestedAssignees}/>,
    },
    {
        title: t('Release Stats'),
        message: t('See the commits in each release, and which issues were introduced or fixed in the release'),
        svg: <Illustration data={issues}/>,
    },
    {
        title: t('Easy Resolution'),
        message: t('Automatically resolve issues by including the issue number in your commit message'),
        svg: <Illustration data={minified}/>,
    },
    {
        title: t('Deploy Emails'),
        message: t('Receive email notifications when your code gets deployed'),
        svg: <Illustration data={emails}/>,
    },
];
var ReleaseLanding = withOrganization(withProject(/** @class */ (function (_super) {
    __extends(ReleaseLanding, _super);
    function ReleaseLanding(props) {
        var _this = _super.call(this, props) || this;
        _this.handleClick = function () {
            var stepId = _this.state.stepId;
            var _a = _this.props, organization = _a.organization, project = _a.project;
            var title = cards[stepId].title;
            if (stepId >= cards.length - 1) {
                return;
            }
            _this.setState(function (state) { return ({
                stepId: state.stepId + 1,
            }); });
            analytics('releases.landing_card_clicked', {
                org_id: parseInt(organization.id, 10),
                project_id: project && parseInt(project.id, 10),
                step_id: stepId,
                step_title: title,
            });
        };
        _this.getCard = function (stepId) { return cards[stepId]; };
        _this.state = {
            stepId: 0,
        };
        return _this;
    }
    ReleaseLanding.prototype.componentDidMount = function () {
        var _a = this.props, organization = _a.organization, project = _a.project;
        analytics('releases.landing_card_viewed', {
            org_id: parseInt(organization.id, 10),
            project_id: project && parseInt(project.id, 10),
        });
    };
    ReleaseLanding.prototype.render = function () {
        var stepId = this.state.stepId;
        var card = this.getCard(stepId);
        return (<ReleaseLandingCard onClick={this.handleClick} card={card} step={stepId} cardsLength={cards.length}/>);
    };
    return ReleaseLanding;
}(React.Component))));
export default ReleaseLanding;
var templateObject_1;
//# sourceMappingURL=releaseLanding.jsx.map