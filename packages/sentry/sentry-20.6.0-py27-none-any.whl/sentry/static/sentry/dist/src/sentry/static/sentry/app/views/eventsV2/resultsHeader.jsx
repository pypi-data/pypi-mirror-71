import { __extends } from "tslib";
import React from 'react';
import { fetchSavedQuery } from 'app/actionCreators/discoverSavedQueries';
import Feature from 'app/components/acl/feature';
import FeatureDisabled from 'app/components/acl/featureDisabled';
import Hovercard from 'app/components/hovercard';
import { t } from 'app/locale';
import withApi from 'app/utils/withApi';
import { HeaderBox, HeaderTopControls } from 'app/utils/discover/styles';
import DiscoverBreadcrumb from './breadcrumb';
import EventInputName from './eventInputName';
import SavedQueryButtonGroup from './savedQuery';
var ResultsHeader = /** @class */ (function (_super) {
    __extends(ResultsHeader, _super);
    function ResultsHeader() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            savedQuery: undefined,
            loading: true,
        };
        return _this;
    }
    ResultsHeader.prototype.componentDidMount = function () {
        if (this.props.eventView.id) {
            this.fetchData();
        }
    };
    ResultsHeader.prototype.componentDidUpdate = function (prevProps) {
        if (prevProps.eventView &&
            this.props.eventView &&
            prevProps.eventView.id !== this.props.eventView.id) {
            this.fetchData();
        }
    };
    ResultsHeader.prototype.fetchData = function () {
        var _this = this;
        var _a = this.props, api = _a.api, eventView = _a.eventView, organization = _a.organization;
        if (typeof eventView.id === 'string') {
            this.setState({ loading: true });
            fetchSavedQuery(api, organization.slug, eventView.id).then(function (savedQuery) {
                _this.setState({ savedQuery: savedQuery, loading: false });
            });
        }
    };
    ResultsHeader.prototype.render = function () {
        var _a = this.props, organization = _a.organization, location = _a.location, errorCode = _a.errorCode, eventView = _a.eventView;
        var _b = this.state, savedQuery = _b.savedQuery, loading = _b.loading;
        var renderDisabled = function (p) { return (<Hovercard body={<FeatureDisabled features={p.features} hideHelpToggle message={t('Discover queries are disabled')} featureName={t('Discover queries')}/>}>
        {p.children(p)}
      </Hovercard>); };
        return (<HeaderBox>
        <DiscoverBreadcrumb eventView={eventView} organization={organization} location={location}/>
        <EventInputName savedQuery={savedQuery} organization={organization} eventView={eventView}/>
        <HeaderTopControls>
          <Feature organization={organization} features={['discover-query']} hookName="feature-disabled:discover-saved-query-create" renderDisabled={renderDisabled}>
            {function (_a) {
            var hasFeature = _a.hasFeature;
            return (<SavedQueryButtonGroup location={location} organization={organization} eventView={eventView} savedQuery={savedQuery} savedQueryLoading={loading} disabled={!hasFeature || (errorCode >= 400 && errorCode < 500)}/>);
        }}
          </Feature>
        </HeaderTopControls>
      </HeaderBox>);
    };
    return ResultsHeader;
}(React.Component));
export default withApi(ResultsHeader);
//# sourceMappingURL=resultsHeader.jsx.map