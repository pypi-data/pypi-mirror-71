import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import partition from 'lodash/partition';
import flatten from 'lodash/flatten';
import GlobalSelectionLink from 'app/components/globalSelectionLink';
import { PanelHeader, PanelBody, PanelItem } from 'app/components/panels';
import { t, tn } from 'app/locale';
import space from 'app/styles/space';
import Count from 'app/components/count';
import { defined } from 'app/utils';
import theme from 'app/utils/theme';
import ScoreBar from 'app/components/scoreBar';
import Tooltip from 'app/components/tooltip';
import ProjectBadge from 'app/components/idBadge/projectBadge';
import TextOverflow from 'app/components/textOverflow';
import Placeholder from 'app/components/placeholder';
import Link from 'app/components/links/link';
import HealthStatsChart from './healthStatsChart';
import { convertAdoptionToProgress, getReleaseNewIssuesUrl } from '../utils';
import HealthStatsSubject from './healthStatsSubject';
import HealthStatsPeriod from './healthStatsPeriod';
import AdoptionTooltip from './adoptionTooltip';
import NotAvailable from './notAvailable';
import ClippedHealthRows from './clippedHealthRows';
import CrashFree from './crashFree';
var ReleaseHealth = function (_a) {
    var release = _a.release, orgSlug = _a.orgSlug, location = _a.location, selection = _a.selection, showPlaceholders = _a.showPlaceholders;
    var activeStatsPeriod = (location.query.healthStatsPeriod || '24h');
    var activeStatsSubject = (location.query.healthStat || 'sessions');
    // sort health rows inside release card alphabetically by project name,
    // but put the ones with project selected in global header to top
    var sortedProjects = flatten(partition(release.projects.sort(function (a, b) { return a.slug.localeCompare(b.slug); }), function (p) { return selection.projects.includes(p.id); }));
    return (<React.Fragment>
      <StyledPanelHeader>
        <HeaderLayout>
          <ProjectColumn>{t('Project name')}</ProjectColumn>
          <AdoptionColumn>{t('Release adoption')}</AdoptionColumn>
          <CrashFreeUsersColumn>{t('Crash free users')}</CrashFreeUsersColumn>
          <CrashFreeSessionsColumn>{t('Crash free sessions')}</CrashFreeSessionsColumn>
          <DailyUsersColumn>
            <HealthStatsSubject location={location} activeSubject={activeStatsSubject}/>
            <HealthStatsPeriod location={location} activePeriod={activeStatsPeriod}/>
          </DailyUsersColumn>
          <CrashesColumn>{t('Crashes')}</CrashesColumn>
          <NewIssuesColumn>{t('New Issues')}</NewIssuesColumn>
        </HeaderLayout>
      </StyledPanelHeader>

      <PanelBody>
        <ClippedHealthRows fadeHeight="46px" maxVisibleItems={4}>
          {sortedProjects.map(function (project, index) {
        var id = project.id, slug = project.slug, healthData = project.healthData, newGroups = project.newGroups;
        var _a = healthData || {}, hasHealthData = _a.hasHealthData, adoption = _a.adoption, stats = _a.stats, crashFreeUsers = _a.crashFreeUsers, crashFreeSessions = _a.crashFreeSessions, sessionsCrashed = _a.sessionsCrashed, totalUsers = _a.totalUsers, totalUsers24h = _a.totalUsers24h, totalSessions = _a.totalSessions, totalSessions24h = _a.totalSessions24h;
        return (<StyledPanelItem key={release.version + "-" + slug + "-health"} isLast={index === sortedProjects.length - 1}>
                <Layout>
                  <ProjectColumn>
                    <GlobalSelectionLink to={{
            pathname: "/organizations/" + orgSlug + "/releases/" + encodeURIComponent(release.version) + "/",
            query: { project: id },
        }}>
                      <ProjectBadge project={project} avatarSize={16} key={slug}/>
                    </GlobalSelectionLink>
                  </ProjectColumn>

                  <AdoptionColumn>
                    {showPlaceholders ? (<StyledPlaceholder width="150px"/>) : defined(adoption) ? (<AdoptionWrapper>
                        <Tooltip title={<AdoptionTooltip totalUsers={totalUsers} totalSessions={totalSessions} totalUsers24h={totalUsers24h} totalSessions24h={totalSessions24h}/>}>
                          <StyledScoreBar score={convertAdoptionToProgress(adoption)} size={20} thickness={5} radius={0} palette={Array(10).fill(theme.purple500)}/>
                        </Tooltip>
                        <TextOverflow>
                          <Count value={totalUsers24h !== null && totalUsers24h !== void 0 ? totalUsers24h : 0}/>{' '}
                          {tn('user', 'users', totalUsers24h)}
                        </TextOverflow>
                      </AdoptionWrapper>) : (<NotAvailable />)}
                  </AdoptionColumn>

                  <CrashFreeUsersColumn>
                    {showPlaceholders ? (<StyledPlaceholder width="60px"/>) : defined(crashFreeUsers) ? (<CrashFree percent={crashFreeUsers}/>) : (<NotAvailable />)}
                  </CrashFreeUsersColumn>

                  <CrashFreeSessionsColumn>
                    {showPlaceholders ? (<StyledPlaceholder width="60px"/>) : defined(crashFreeSessions) ? (<CrashFree percent={crashFreeSessions}/>) : (<NotAvailable />)}
                  </CrashFreeSessionsColumn>

                  <DailyUsersColumn>
                    {showPlaceholders ? (<StyledPlaceholder />) : hasHealthData && defined(stats) ? (<ChartWrapper>
                        <HealthStatsChart data={stats} height={20} period={activeStatsPeriod} subject={activeStatsSubject}/>
                      </ChartWrapper>) : (<NotAvailable />)}
                  </DailyUsersColumn>

                  <CrashesColumn>
                    {showPlaceholders ? (<StyledPlaceholder width="30px"/>) : hasHealthData && defined(sessionsCrashed) ? (<Count value={sessionsCrashed}/>) : (<NotAvailable />)}
                  </CrashesColumn>

                  <NewIssuesColumn>
                    <Tooltip title={t('Open in Issues')}>
                      <Link to={getReleaseNewIssuesUrl(orgSlug, project.id, release.version)}>
                        <Count value={newGroups || 0}/>
                      </Link>
                    </Tooltip>
                  </NewIssuesColumn>
                </Layout>
              </StyledPanelItem>);
    })}
        </ClippedHealthRows>
      </PanelBody>
    </React.Fragment>);
};
var StyledPanelHeader = styled(PanelHeader)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  border-top: 1px solid ", ";\n  border-top-left-radius: 0;\n  border-top-right-radius: 0;\n  color: ", ";\n  font-size: ", ";\n"], ["\n  border-top: 1px solid ", ";\n  border-top-left-radius: 0;\n  border-top-right-radius: 0;\n  color: ", ";\n  font-size: ", ";\n"])), function (p) { return p.theme.borderDark; }, function (p) { return p.theme.gray500; }, function (p) { return p.theme.fontSizeSmall; });
var StyledPanelItem = styled(PanelItem)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  padding: ", " ", ";\n  min-height: 46px;\n  border: ", ";\n"], ["\n  padding: ", " ", ";\n  min-height: 46px;\n  border: ", ";\n"])), space(1), space(2), function (p) { return (p.isLast ? 'none' : null); });
var Layout = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: grid;\n  grid-template-areas: 'project adoption crash-free-users crash-free-sessions daily-users crashes new-issues';\n  grid-template-columns: 2fr 2fr 1.4fr 1.4fr 2.1fr 0.7fr 0.8fr;\n  grid-column-gap: ", ";\n  width: 100%;\n  align-items: center;\n  @media (max-width: ", ") {\n    grid-template-areas: 'project adoption crash-free-users crash-free-sessions crashes new-issues';\n    grid-template-columns: 2fr 2fr 1.5fr 1.5fr 1fr 1fr;\n  }\n  @media (max-width: ", ") {\n    grid-template-areas: 'project crash-free-users crash-free-sessions crashes new-issues';\n    grid-template-columns: 2fr 1.5fr 1.5fr 1fr 1fr;\n  }\n  @media (max-width: ", ") {\n    grid-template-areas: 'project crash-free-sessions new-issues';\n    grid-template-columns: 2fr 1.5fr 1fr;\n  }\n"], ["\n  display: grid;\n  grid-template-areas: 'project adoption crash-free-users crash-free-sessions daily-users crashes new-issues';\n  grid-template-columns: 2fr 2fr 1.4fr 1.4fr 2.1fr 0.7fr 0.8fr;\n  grid-column-gap: ", ";\n  width: 100%;\n  align-items: center;\n  @media (max-width: ", ") {\n    grid-template-areas: 'project adoption crash-free-users crash-free-sessions crashes new-issues';\n    grid-template-columns: 2fr 2fr 1.5fr 1.5fr 1fr 1fr;\n  }\n  @media (max-width: ", ") {\n    grid-template-areas: 'project crash-free-users crash-free-sessions crashes new-issues';\n    grid-template-columns: 2fr 1.5fr 1.5fr 1fr 1fr;\n  }\n  @media (max-width: ", ") {\n    grid-template-areas: 'project crash-free-sessions new-issues';\n    grid-template-columns: 2fr 1.5fr 1fr;\n  }\n"])), space(1.5), function (p) { return p.theme.breakpoints[2]; }, function (p) { return p.theme.breakpoints[1]; }, function (p) { return p.theme.breakpoints[0]; });
var HeaderLayout = styled(Layout)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  align-items: flex-end;\n"], ["\n  align-items: flex-end;\n"])));
var Column = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  overflow: hidden;\n"], ["\n  overflow: hidden;\n"])));
var RightColumn = styled(Column)(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  text-align: right;\n"], ["\n  text-align: right;\n"])));
var CenterColumn = styled(Column)(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  text-align: center;\n"], ["\n  text-align: center;\n"])));
var ProjectColumn = styled(Column)(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  grid-area: project;\n"], ["\n  grid-area: project;\n"])));
var DailyUsersColumn = styled(Column)(templateObject_9 || (templateObject_9 = __makeTemplateObject(["\n  grid-area: daily-users;\n  display: flex;\n  align-items: flex-end;\n  @media (max-width: ", ") {\n    display: none;\n  }\n"], ["\n  grid-area: daily-users;\n  display: flex;\n  align-items: flex-end;\n  @media (max-width: ", ") {\n    display: none;\n  }\n"])), function (p) { return p.theme.breakpoints[2]; });
var AdoptionColumn = styled(Column)(templateObject_10 || (templateObject_10 = __makeTemplateObject(["\n  grid-area: adoption;\n  @media (max-width: ", ") {\n    display: none;\n  }\n"], ["\n  grid-area: adoption;\n  @media (max-width: ", ") {\n    display: none;\n  }\n"])), function (p) { return p.theme.breakpoints[1]; });
var CrashFreeUsersColumn = styled(CenterColumn)(templateObject_11 || (templateObject_11 = __makeTemplateObject(["\n  grid-area: crash-free-users;\n  @media (max-width: ", ") {\n    text-align: left;\n  }\n  @media (max-width: ", ") {\n    display: none;\n  }\n"], ["\n  grid-area: crash-free-users;\n  @media (max-width: ", ") {\n    text-align: left;\n  }\n  @media (max-width: ", ") {\n    display: none;\n  }\n"])), function (p) { return p.theme.breakpoints[2]; }, function (p) { return p.theme.breakpoints[0]; });
var CrashFreeSessionsColumn = styled(CenterColumn)(templateObject_12 || (templateObject_12 = __makeTemplateObject(["\n  grid-area: crash-free-sessions;\n  @media (max-width: ", ") {\n    text-align: left;\n  }\n"], ["\n  grid-area: crash-free-sessions;\n  @media (max-width: ", ") {\n    text-align: left;\n  }\n"])), function (p) { return p.theme.breakpoints[2]; });
var CrashesColumn = styled(RightColumn)(templateObject_13 || (templateObject_13 = __makeTemplateObject(["\n  grid-area: crashes;\n  @media (max-width: ", ") {\n    display: none;\n  }\n"], ["\n  grid-area: crashes;\n  @media (max-width: ", ") {\n    display: none;\n  }\n"])), function (p) { return p.theme.breakpoints[0]; });
var NewIssuesColumn = styled(RightColumn)(templateObject_14 || (templateObject_14 = __makeTemplateObject(["\n  grid-area: new-issues;\n"], ["\n  grid-area: new-issues;\n"])));
var AdoptionWrapper = styled('div')(templateObject_15 || (templateObject_15 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: flex-start;\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: flex-start;\n"])));
var StyledScoreBar = styled(ScoreBar)(templateObject_16 || (templateObject_16 = __makeTemplateObject(["\n  margin-right: ", ";\n"], ["\n  margin-right: ", ";\n"])), space(1));
var ChartWrapper = styled('div')(templateObject_17 || (templateObject_17 = __makeTemplateObject(["\n  flex: 1;\n  g > .barchart-rect {\n    background: ", ";\n    fill: ", ";\n  }\n"], ["\n  flex: 1;\n  g > .barchart-rect {\n    background: ", ";\n    fill: ", ";\n  }\n"])), function (p) { return p.theme.gray400; }, function (p) { return p.theme.gray400; });
var StyledPlaceholder = styled(Placeholder)(templateObject_18 || (templateObject_18 = __makeTemplateObject(["\n  height: 20px;\n  display: inline-block;\n  position: relative;\n  top: ", ";\n"], ["\n  height: 20px;\n  display: inline-block;\n  position: relative;\n  top: ", ";\n"])), space(0.25));
export default ReleaseHealth;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10, templateObject_11, templateObject_12, templateObject_13, templateObject_14, templateObject_15, templateObject_16, templateObject_17, templateObject_18;
//# sourceMappingURL=releaseHealth.jsx.map