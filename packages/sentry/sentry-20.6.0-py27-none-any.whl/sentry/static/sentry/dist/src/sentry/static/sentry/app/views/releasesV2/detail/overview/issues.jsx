import { __assign, __extends, __makeTemplateObject, __read, __spread } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import pick from 'lodash/pick';
import { t, tct } from 'app/locale';
import DropdownControl, { DropdownItem } from 'app/components/dropdownControl';
import Button from 'app/components/button';
import DiscoverButton from 'app/components/discoverButton';
import GroupList from 'app/components/issues/groupList';
import space from 'app/styles/space';
import { Panel, PanelBody } from 'app/components/panels';
import EventView from 'app/utils/discover/eventView';
import { formatVersion } from 'app/utils/formatters';
import EmptyStateWarning from 'app/components/emptyStateWarning';
import { DEFAULT_RELATIVE_PERIODS } from 'app/constants';
import Feature from 'app/components/acl/feature';
import { URL_PARAM } from 'app/constants/globalSelectionHeader';
import { getUtcDateString } from 'app/utils/dates';
import DropdownButton from 'app/components/dropdownButton';
import ButtonBar from 'app/components/buttonBar';
import { stringifyQueryObject } from 'app/utils/tokenizeSearch';
var IssuesType;
(function (IssuesType) {
    IssuesType["NEW"] = "new";
    IssuesType["RESOLVED"] = "resolved";
    IssuesType["ALL"] = "all";
})(IssuesType || (IssuesType = {}));
var Issues = /** @class */ (function (_super) {
    __extends(Issues, _super);
    function Issues() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            issuesType: IssuesType.NEW,
        };
        _this.handleIssuesTypeSelection = function (issuesType) {
            _this.setState({ issuesType: issuesType });
        };
        _this.renderEmptyMessage = function () {
            var selection = _this.props.selection;
            var issuesType = _this.state.issuesType;
            var selectedTimePeriod = DEFAULT_RELATIVE_PERIODS[selection.datetime.period];
            var displayedPeriod = selectedTimePeriod
                ? selectedTimePeriod.toLowerCase()
                : t('given timeframe');
            return (<Panel>
        <PanelBody>
          <EmptyStateWarning small withIcon={false}>
            {issuesType === IssuesType.NEW &&
                tct('No new issues in this release for the [timePeriod].', {
                    timePeriod: displayedPeriod,
                })}
            {issuesType === IssuesType.RESOLVED &&
                t('No resolved issues in this release.')}
            {issuesType === IssuesType.ALL &&
                tct('No issues in this release for the [timePeriod].', {
                    timePeriod: displayedPeriod,
                })}
          </EmptyStateWarning>
        </PanelBody>
      </Panel>);
        };
        return _this;
    }
    Issues.prototype.getDiscoverUrl = function () {
        var _a = this.props, version = _a.version, orgId = _a.orgId, selection = _a.selection;
        var projects = selection.projects, environments = selection.environments, datetime = selection.datetime;
        var start = datetime.start, end = datetime.end, period = datetime.period;
        var discoverQuery = {
            id: undefined,
            version: 2,
            name: t('Release') + " " + formatVersion(version),
            fields: ['title', 'count()', 'event.type', 'issue', 'last_seen()'],
            query: "release:" + version + " !event.type:transaction",
            orderby: '-last_seen',
            range: period,
            environment: environments,
            projects: projects,
            start: start ? getUtcDateString(start) : undefined,
            end: end ? getUtcDateString(end) : undefined,
        };
        var discoverView = EventView.fromSavedQuery(discoverQuery);
        return discoverView.getResultsViewUrlTarget(orgId);
    };
    Issues.prototype.getIssuesUrl = function () {
        var _a = this.props, version = _a.version, orgId = _a.orgId;
        var issuesType = this.state.issuesType;
        var queryParams = this.getIssuesEndpoint().queryParams;
        var query = { query: [] };
        if (issuesType === IssuesType.NEW) {
            query.firstRelease = [version];
        }
        else {
            query.release = [version];
        }
        return {
            pathname: "/organizations/" + orgId + "/issues/",
            query: __assign(__assign({}, queryParams), { query: stringifyQueryObject(query) }),
        };
    };
    Issues.prototype.getIssuesEndpoint = function () {
        var _a = this.props, version = _a.version, orgId = _a.orgId, location = _a.location;
        var issuesType = this.state.issuesType;
        var queryParams = __assign(__assign({}, pick(location.query, __spread(Object.values(URL_PARAM), ['cursor']))), { limit: 50, sort: 'new' });
        switch (issuesType) {
            case IssuesType.ALL:
                return {
                    path: "/organizations/" + orgId + "/issues/",
                    queryParams: __assign(__assign({}, queryParams), { query: "release:\"" + version + "\"" }),
                };
            case IssuesType.RESOLVED:
                return {
                    path: "/organizations/" + orgId + "/releases/" + version + "/resolved/",
                    queryParams: __assign(__assign({}, queryParams), { query: '' }),
                };
            case IssuesType.NEW:
            default:
                return {
                    path: "/organizations/" + orgId + "/issues/",
                    queryParams: __assign(__assign({}, queryParams), { query: "first-release:\"" + version + "\"" }),
                };
        }
    };
    Issues.prototype.render = function () {
        var _this = this;
        var issuesType = this.state.issuesType;
        var orgId = this.props.orgId;
        var _a = this.getIssuesEndpoint(), path = _a.path, queryParams = _a.queryParams;
        var issuesTypes = [
            { value: 'new', label: t('New Issues') },
            { value: 'resolved', label: t('Resolved Issues') },
            { value: 'all', label: t('All Issues') },
        ];
        return (<React.Fragment>
        <ControlsWrapper>
          <DropdownControl button={function (_a) {
            var getActorProps = _a.getActorProps;
            var _b;
            return (<FilterButton prefix={t('Filter')} {...getActorProps()} isOpen={false}>
                {(_b = issuesTypes.find(function (i) { return i.value === issuesType; })) === null || _b === void 0 ? void 0 : _b.label}
              </FilterButton>);
        }}>
            {issuesTypes.map(function (_a) {
            var value = _a.value, label = _a.label;
            return (<DropdownItem key={value} onSelect={_this.handleIssuesTypeSelection} eventKey={value} isActive={value === issuesType}>
                {label}
              </DropdownItem>);
        })}
          </DropdownControl>

          <ButtonBar gap={1}>
            <Feature features={['discover-basic']}>
              <OpenDiscoverButton to={this.getDiscoverUrl()}>
                {t('Open in Discover')}
              </OpenDiscoverButton>
            </Feature>

            <OpenInButton to={this.getIssuesUrl()}>{t('Open in Issues')}</OpenInButton>
          </ButtonBar>
        </ControlsWrapper>

        <TableWrapper>
          <GroupList orgId={orgId} endpointPath={path} queryParams={queryParams} query="" canSelectGroups={false} withChart={false} renderEmptyMessage={this.renderEmptyMessage}/>
        </TableWrapper>
      </React.Fragment>);
    };
    return Issues;
}(React.Component));
// used in media query
var FilterButton = styled(DropdownButton)(templateObject_1 || (templateObject_1 = __makeTemplateObject([""], [""])));
var OpenInButton = styled(Button)(templateObject_2 || (templateObject_2 = __makeTemplateObject([""], [""])));
var OpenDiscoverButton = styled(DiscoverButton)(templateObject_3 || (templateObject_3 = __makeTemplateObject([""], [""])));
var ControlsWrapper = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  margin-bottom: ", ";\n  @media (max-width: ", ") {\n    ", ",\n    ", ",\n    ", " {\n      font-size: ", ";\n    }\n  }\n\n  @media (max-width: ", ") {\n    display: block;\n    ", " {\n      margin-bottom: ", ";\n    }\n  }\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  margin-bottom: ", ";\n  @media (max-width: ", ") {\n    " /* sc-selector */, ",\n    " /* sc-selector */, ",\n    " /* sc-selector */, " {\n      font-size: ", ";\n    }\n  }\n\n  @media (max-width: ", ") {\n    display: block;\n    ", " {\n      margin-bottom: ", ";\n    }\n  }\n"])), space(1), function (p) { return p.theme.breakpoints[2]; }, /* sc-selector */ FilterButton, /* sc-selector */ OpenInButton, /* sc-selector */ OpenDiscoverButton, function (p) { return p.theme.fontSizeSmall; }, function (p) { return p.theme.breakpoints[0]; }, FilterButton, space(1));
var TableWrapper = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  margin-bottom: ", ";\n  ", " {\n    /* smaller space between table and pagination */\n    margin-bottom: -", ";\n  }\n"], ["\n  margin-bottom: ", ";\n  ", " {\n    /* smaller space between table and pagination */\n    margin-bottom: -", ";\n  }\n"])), space(4), Panel, space(1));
export default Issues;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=issues.jsx.map