import { __extends } from "tslib";
import React from 'react';
import { PageContent } from 'app/styles/organization';
import { Panel } from 'app/components/panels';
import { t } from 'app/locale';
import AsyncView from 'app/views/asyncView';
import EmptyMessage from 'app/views/settings/components/emptyMessage';
import ErrorBoundary from 'app/components/errorBoundary';
import LoadingIndicator from 'app/components/loadingIndicator';
import PageHeading from 'app/components/pageHeading';
import Pagination from 'app/components/pagination';
import routeTitle from 'app/utils/routeTitle';
import space from 'app/styles/space';
import withOrganization from 'app/utils/withOrganization';
import ActivityFeedItem from './activityFeedItem';
var OrganizationActivity = /** @class */ (function (_super) {
    __extends(OrganizationActivity, _super);
    function OrganizationActivity() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    OrganizationActivity.prototype.getTitle = function () {
        var orgId = this.props.params.orgId;
        return routeTitle(t('Activity'), orgId);
    };
    OrganizationActivity.prototype.getEndpoints = function () {
        return [['activity', "/organizations/" + this.props.params.orgId + "/activity/"]];
    };
    OrganizationActivity.prototype.renderLoading = function () {
        return this.renderBody();
    };
    OrganizationActivity.prototype.renderEmpty = function () {
        return (<EmptyMessage icon="icon-circle-exclamation">
        {t('Nothing to show here, move along.')}
      </EmptyMessage>);
    };
    OrganizationActivity.prototype.renderBody = function () {
        var _this = this;
        var _a = this.state, loading = _a.loading, activity = _a.activity, activityPageLinks = _a.activityPageLinks;
        return (<PageContent>
        <PageHeading withMargins>{t('Activity')}</PageHeading>
        <Panel>
          {loading && <LoadingIndicator />}
          {!loading && !activity.length && this.renderEmpty()}
          {!loading && !!activity.length && (<div data-test-id="activity-feed-list">
              {activity.map(function (item) { return (<ErrorBoundary mini css={{ marginBottom: space(1), borderRadius: 0 }} key={item.id}>
                  <ActivityFeedItem organization={_this.props.organization} item={item}/>
                </ErrorBoundary>); })}
            </div>)}
        </Panel>
        {activityPageLinks && (<Pagination pageLinks={activityPageLinks} {...this.props}/>)}
      </PageContent>);
    };
    return OrganizationActivity;
}(AsyncView));
export default withOrganization(OrganizationActivity);
//# sourceMappingURL=index.jsx.map