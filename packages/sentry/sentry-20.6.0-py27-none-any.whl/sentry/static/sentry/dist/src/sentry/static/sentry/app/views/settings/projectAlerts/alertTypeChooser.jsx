import { __extends, __makeTemplateObject, __rest } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Card from 'app/components/card';
import { t, tct } from 'app/locale';
import space from 'app/styles/space';
import Radio from 'app/components/radio';
import textStyles from 'app/styles/text';
import BulletList from 'app/styles/bulletList';
import FeatureBadge from 'app/components/featureBadge';
import Tooltip from 'app/components/tooltip';
import { Panel, PanelHeader } from 'app/components/panels';
import RadioField from 'app/views/settings/components/forms/radioField';
import Feature from 'app/components/acl/feature';
import ExternalLink from 'app/components/links/externalLink';
import withExperiment from 'app/utils/withExperiment';
import { trackAnalyticsEvent } from 'app/utils/analytics';
var MetricsTooltip = function (_a) {
    var children = _a.children;
    return (<Tooltip title={t("A metric is the value of an aggregate function like count() or avg()\n       applied to your events over time")}>
    <abbr>{children}</abbr>
  </Tooltip>);
};
var IssuesTooltip = function (_a) {
    var children = _a.children;
    return (<Tooltip title={t("Sentry groups similar events into an Issue based on their stack trace\n       and other factors.")}>
    <abbr>{children}</abbr>
  </Tooltip>);
};
var TypeChooserCards = function (_a) {
    var onChange = _a.onChange, organization = _a.organization, selected = _a.selected;
    var trackedOnChange = function (type) {
        trackAnalyticsEvent({
            eventKey: 'alert_chooser_cards.select',
            eventName: 'Alert Chooser Cards: Select',
            organization_id: organization.id,
            type: type,
        });
        onChange(type);
    };
    return (<Container>
      <TypeCard interactive onClick={function () { return trackedOnChange('metric'); }}>
        <RadioLabel>
          <Radio aria-label="metric" checked={selected === 'metric'} onChange={function () { return trackedOnChange('metric'); }}/>
          {t('Metric Alert')}
          <FeatureBadge type="beta"/>
        </RadioLabel>
        <Feature requireAll features={[
        'organizations:transaction-events',
        'organizations:incidents-performance',
    ]}>
          {function (_a) {
        var hasFeature = _a.hasFeature;
        return hasFeature ? (<React.Fragment>
                <p>
                  {tct("Notifies you when a [tooltip:metric] exceeds a threshold.", {
            tooltip: <MetricsTooltip />,
        })}
                </p>
                {!selected && (<React.Fragment>
                    <ExampleHeading>{t('For Example:')}</ExampleHeading>
                    <BulletList>
                      <li>{t('Performance metrics like latency and apdex')}</li>
                      <li>
                        {t("Frequency of error events or users affected in the\n                       project")}
                      </li>
                    </BulletList>
                  </React.Fragment>)}
              </React.Fragment>) : (<React.Fragment>
                <p>
                  {tct("Notifies you when a [tooltip:metric] like frequency of events or users affected in\n                   the project exceeds a threshold.", { tooltip: <MetricsTooltip /> })}
                </p>
                {!selected && (<React.Fragment>
                    <ExampleHeading>{t('For Example:')}</ExampleHeading>
                    <BulletList>
                      <li>{t('Total events in the project exceed 1000/minute')}</li>
                      <li>
                        {tct('Events with tag [code:database] and "API" in the title exceed 100/minute', { code: <code /> })}
                      </li>
                    </BulletList>
                  </React.Fragment>)}
              </React.Fragment>);
    }}
        </Feature>
      </TypeCard>
      <TypeCard interactive onClick={function () { return trackedOnChange('issue'); }}>
        <RadioLabel>
          <Radio aria-label="issue" checked={selected === 'issue'} onChange={function () { return trackedOnChange('issue'); }}/>
          {t('Issue Alert')}
        </RadioLabel>
        <p>
          {tct("Notifies you when individual [tooltip:Sentry Issues] trigger your\n           alerting criteria.", { tooltip: <IssuesTooltip /> })}
        </p>
        {!selected && (<React.Fragment>
            <ExampleHeading>{t('For Example:')}</ExampleHeading>
            <BulletList>
              <li>{t('New Issues or regressions')}</li>
              <li>{t('Frequency of individual Issues exceeds 100/minute')}</li>
            </BulletList>
          </React.Fragment>)}
      </TypeCard>
    </Container>);
};
var TypeChooserFlow = /** @class */ (function (_super) {
    __extends(TypeChooserFlow, _super);
    function TypeChooserFlow() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {};
        _this.update = function (state) {
            return _this.setState(state, function () {
                var _a = _this.state, type = _a.type, granularity = _a.granularity;
                var _b = _this.props, organization = _b.organization, onChange = _b.onChange;
                var selectMetricAlerts = type === 'frequency' && granularity === 'project';
                var selectIssueAlerts = type === 'issues' || (type === 'frequency' && granularity === 'issue');
                trackAnalyticsEvent({
                    eventKey: 'alert_chooser_flow.select',
                    eventName: 'Alert Chooser Flow: Select',
                    organization_id: organization.id,
                    type: type,
                    granularity: granularity,
                });
                onChange(selectMetricAlerts ? 'metric' : selectIssueAlerts ? 'issue' : null);
            });
        };
        return _this;
    }
    TypeChooserFlow.prototype.render = function () {
        var _this = this;
        var _a = this.state, type = _a.type, granularity = _a.granularity;
        return (<Panel>
        <PanelHeader>{t('Alert details')}</PanelHeader>
        <RadioField label={t('Alert type')} help={tct('Remember that Sentry groups similar events into an Issue based on their stack trace and other factors. [learnMore:Learn more]', {
            learnMore: (<ExternalLink href="https://docs.sentry.io/data-management/event-grouping/"/>),
        })} onChange={function (value) { return _this.update({ type: value }); }} value={type} choices={[
            ['frequency', t('Frequency of events or users affected increasing')],
            ['issues', t('New issues and regressions')],
        ]}/>
        {type === 'frequency' && (<RadioField label={t('Granularity')} help={t('Frequency thresholds can be set per Issue or for the entire project.')} onChange={function (value) { return _this.update({ granularity: value }); }} value={granularity} choices={[
            [
                'project',
                t('Frequency of events in entire project'),
                <React.Fragment key="list">
                  <Example>{t('Total events in the project exceed 1000/minute')}</Example>
                  <Example>
                    {t('Events with tag `database` and API in the title exceed 100/minute')}
                  </Example>
                </React.Fragment>,
            ],
            [
                'issue',
                t('Frequency of individual Issues'),
                <React.Fragment key="list">
                  <Example>
                    {t("Any single Issue on the checkout page happens more than\n                       100 times in a minute.")}
                  </Example>
                </React.Fragment>,
            ],
        ]}/>)}
      </Panel>);
    };
    return TypeChooserFlow;
}(React.Component));
var RadioLabel = styled('label')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  cursor: pointer;\n  margin-bottom: ", ";\n  display: grid;\n  grid-auto-flow: column;\n  grid-auto-columns: max-content;\n  align-items: center;\n  grid-gap: ", ";\n"], ["\n  cursor: pointer;\n  margin-bottom: ", ";\n  display: grid;\n  grid-auto-flow: column;\n  grid-auto-columns: max-content;\n  align-items: center;\n  grid-gap: ", ";\n"])), space(3), space(2));
var ExampleHeading = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  text-transform: uppercase;\n  font-size: ", ";\n  font-weight: bold;\n  color: ", ";\n  margin-bottom: ", ";\n"], ["\n  text-transform: uppercase;\n  font-size: ", ";\n  font-weight: bold;\n  color: ", ";\n  margin-bottom: ", ";\n"])), function (p) { return p.theme.fontSizeSmall; }, function (p) { return p.theme.gray600; }, space(2));
var Example = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  font-size: ", ";\n  color: ", ";\n"], ["\n  font-size: ", ";\n  color: ", ";\n"])), function (p) { return p.theme.fontSizeSmall; }, function (p) { return p.theme.gray500; });
var Container = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 1fr 1fr;\n  grid-gap: ", ";\n"], ["\n  display: grid;\n  grid-template-columns: 1fr 1fr;\n  grid-gap: ", ";\n"])), space(3));
var TypeCard = styled(Card)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  cursor: pointer;\n  padding: ", ";\n  margin-bottom: ", ";\n  ", ";\n"], ["\n  cursor: pointer;\n  padding: ", ";\n  margin-bottom: ", ";\n  ", ";\n"])), space(4), space(3), textStyles);
export default withExperiment(function (_a) {
    var experimentAssignment = _a.experimentAssignment, props = __rest(_a, ["experimentAssignment"]);
    return experimentAssignment === 'flowChoice' ? (<TypeChooserFlow {...props}/>) : (<TypeChooserCards {...props}/>);
}, { experiment: 'MetricAlertsTypeChooser' });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=alertTypeChooser.jsx.map