import { __extends, __makeTemplateObject } from "tslib";
import sortBy from 'lodash/sortBy';
import property from 'lodash/property';
import React from 'react';
import styled from '@emotion/styled';
import { isUrl, percent } from 'app/utils';
import { t } from 'app/locale';
import AsyncComponent from 'app/components/asyncComponent';
import UserBadge from 'app/components/idBadge/userBadge';
import Button from 'app/components/button';
import DeviceName from 'app/components/deviceName';
import ExternalLink from 'app/components/links/externalLink';
import GlobalSelectionLink from 'app/components/globalSelectionLink';
import { IconMail, IconOpen } from 'app/icons';
import DetailedError from 'app/components/errors/detailedError';
import Pagination from 'app/components/pagination';
import TimeSince from 'app/components/timeSince';
import DataExport, { ExportQueryType } from 'app/components/dataExport';
import space from 'app/styles/space';
var GroupTagValues = /** @class */ (function (_super) {
    __extends(GroupTagValues, _super);
    function GroupTagValues() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    GroupTagValues.prototype.getEndpoints = function () {
        var environment = this.props.environments;
        var _a = this.props.params, groupId = _a.groupId, tagKey = _a.tagKey;
        return [
            ['tag', "/issues/" + groupId + "/tags/" + tagKey + "/"],
            [
                'tagValueList',
                "/issues/" + groupId + "/tags/" + tagKey + "/values/",
                { query: { environment: environment } },
            ],
        ];
    };
    GroupTagValues.prototype.renderBody = function () {
        var _a = this.props, group = _a.group, _b = _a.params, orgId = _b.orgId, tagKey = _b.tagKey, environments = _a.environments;
        var _c = this.state, tag = _c.tag, tagValueList = _c.tagValueList, tagValueListPageLinks = _c.tagValueListPageLinks;
        var sortedTagValueList = sortBy(tagValueList, property('count')).reverse();
        if (sortedTagValueList.length === 0 && environments.length > 0) {
            return (<DetailedError heading={t('Sorry, the tags for this issue could not be found.')} message={t('No tags were found for the currently selected environments')}/>);
        }
        var issuesPath = "/organizations/" + orgId + "/issues/";
        var children = sortedTagValueList.map(function (tagValue, tagValueIdx) {
            var pct = tag.totalValues
                ? percent(tagValue.count, tag.totalValues).toFixed(2) + "%"
                : '--';
            var query = tagValue.query || tag.key + ":\"" + tagValue.value + "\"";
            return (<tr key={tagValueIdx}>
          <td className="bar-cell">
            <span className="label">{pct}</span>
          </td>
          <td>
            <ValueWrapper>
              <GlobalSelectionLink to={{
                pathname: issuesPath,
                query: { query: query },
            }}>
                {tag.key === 'user' ? (<UserBadge user={tagValue} avatarSize={20} hideEmail/>) : (<DeviceName value={tagValue.name}/>)}
              </GlobalSelectionLink>
              {tagValue.email && (<StyledExternalLink href={"mailto:" + tagValue.email}>
                  <IconMail size="xs" color="gray500"/>
                </StyledExternalLink>)}
              {isUrl(tagValue.value) && (<StyledExternalLink href={tagValue.value}>
                  <IconOpen size="xs" color="gray500"/>
                </StyledExternalLink>)}
            </ValueWrapper>
          </td>
          <td>
            <TimeSince date={tagValue.lastSeen}/>
          </td>
        </tr>);
        });
        return (<React.Fragment>
        <Header>
          {tag.key === 'user' ? t('Affected Users') : tag.name}
          <BrowserExportButton size="small" priority="default" href={"/" + orgId + "/" + group.project.slug + "/issues/" + group.id + "/tags/" + tagKey + "/export/"}>
            {t('Export Page to CSV')}
          </BrowserExportButton>
          <a />
          <DataExport payload={{
            queryType: ExportQueryType.IssuesByTag,
            queryInfo: {
                project: group.project.id,
                group: group.id,
                key: tagKey,
            },
        }}/>
        </Header>
        <table className="table table-striped">
          <thead>
            <tr>
              <TableHeader width={20}>%</TableHeader>
              <th />
              <TableHeader width={300}>{t('Last Seen')}</TableHeader>
            </tr>
          </thead>
          <tbody>{children}</tbody>
        </table>
        <Pagination pageLinks={tagValueListPageLinks}/>
        <p>
          <small>
            {t('Note: Percentage of issue is based on events seen in the last 7 days.')}
          </small>
        </p>
      </React.Fragment>);
    };
    return GroupTagValues;
}(AsyncComponent));
var Header = styled('h3')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  align-items: flex-end;\n"], ["\n  display: flex;\n  align-items: flex-end;\n"])));
var BrowserExportButton = styled(Button)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  margin: 0 ", ";\n"], ["\n  margin: 0 ", ";\n"])), space(1.5));
var TableHeader = styled('th')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  width: ", "px;\n"], ["\n  width: ", "px;\n"])), function (p) { return p.width; });
var ValueWrapper = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n"], ["\n  display: flex;\n  align-items: center;\n"])));
var StyledExternalLink = styled(ExternalLink)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  margin-left: ", ";\n"], ["\n  margin-left: ", ";\n"])), space(0.5));
export { GroupTagValues };
export default GroupTagValues;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=groupTagValues.jsx.map