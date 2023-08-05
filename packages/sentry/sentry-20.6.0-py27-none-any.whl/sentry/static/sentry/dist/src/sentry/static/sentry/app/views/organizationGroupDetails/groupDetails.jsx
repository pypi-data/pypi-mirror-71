import { __assign, __awaiter, __extends, __generator } from "tslib";
import DocumentTitle from 'react-document-title';
import PropTypes from 'prop-types';
import React from 'react';
import * as ReactRouter from 'react-router';
import * as Sentry from '@sentry/browser';
import { PageContent } from 'app/styles/organization';
import { callIfFunction } from 'app/utils/callIfFunction';
import { t } from 'app/locale';
import GlobalSelectionHeader from 'app/components/organizations/globalSelectionHeader';
import GroupStore from 'app/stores/groupStore';
import LoadingError from 'app/components/loadingError';
import LoadingIndicator from 'app/components/loadingIndicator';
import Projects from 'app/utils/projects';
import SentryTypes from 'app/sentryTypes';
import recreateRoute from 'app/utils/recreateRoute';
import withApi from 'app/utils/withApi';
import withProfiler from 'app/utils/withProfiler';
import { ERROR_TYPES } from './constants';
import GroupHeader from './header';
var GroupDetails = /** @class */ (function (_super) {
    __extends(GroupDetails, _super);
    function GroupDetails() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = _this.initialState;
        _this.remountComponent = function () {
            _this.setState(_this.initialState);
            _this.fetchData();
        };
        _this.listener = GroupStore.listen(function (itemIds) { return _this.onGroupChange(itemIds); });
        return _this;
    }
    GroupDetails.prototype.getChildContext = function () {
        return {
            group: this.state.group,
            location: this.props.location,
        };
    };
    GroupDetails.prototype.componentDidMount = function () {
        this.fetchData();
    };
    GroupDetails.prototype.componentDidUpdate = function (prevProps, prevState) {
        if (prevState.loading && !this.state.loading) {
            callIfFunction(this.props.finishProfile);
        }
        if (prevProps.isGlobalSelectionReady !== this.props.isGlobalSelectionReady) {
            this.fetchData();
        }
    };
    GroupDetails.prototype.componentWillUnmount = function () {
        callIfFunction(this.listener);
    };
    Object.defineProperty(GroupDetails.prototype, "initialState", {
        get: function () {
            return {
                group: null,
                loading: true,
                error: false,
                errorType: null,
                project: null,
            };
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(GroupDetails.prototype, "groupDetailsEndpoint", {
        get: function () {
            return "/issues/" + this.props.params.groupId + "/";
        },
        enumerable: true,
        configurable: true
    });
    GroupDetails.prototype.fetchData = function () {
        return __awaiter(this, void 0, void 0, function () {
            var _a, environments, api, isGlobalSelectionReady, data, _b, routes, params, location_1, project, locationWithProject, err_1, errorType;
            return __generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        _a = this.props, environments = _a.environments, api = _a.api, isGlobalSelectionReady = _a.isGlobalSelectionReady;
                        // Need to wait for global selection store to be ready before making request
                        if (!isGlobalSelectionReady) {
                            return [2 /*return*/];
                        }
                        _c.label = 1;
                    case 1:
                        _c.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, api.requestPromise(this.groupDetailsEndpoint, {
                                query: __assign({}, (environments ? { environment: environments } : {})),
                            })];
                    case 2:
                        data = _c.sent();
                        // TODO(billy): See if this is even in use and if not, can we just rip this out?
                        if (this.props.params.groupId !== data.id) {
                            _b = this.props, routes = _b.routes, params = _b.params, location_1 = _b.location;
                            ReactRouter.browserHistory.push(recreateRoute('', {
                                routes: routes,
                                location: location_1,
                                params: __assign(__assign({}, params), { groupId: data.id }),
                            }));
                            return [2 /*return*/];
                        }
                        project = data.project;
                        if (!project) {
                            Sentry.withScope(function () {
                                Sentry.captureException(new Error('Project not found'));
                            });
                        }
                        else {
                            locationWithProject = __assign({}, this.props.location);
                            if (locationWithProject.query.project === undefined &&
                                locationWithProject.query._allp === undefined) {
                                //We use _allp as a temporary measure to know they came from the issue list page with no project selected (all projects included in filter).
                                //If it is not defined, we add the locked project id to the URL (this is because if someone navigates directly to an issue on single-project priveleges, then goes back - they were getting assigned to the first project).
                                //If it is defined, we do not so that our back button will bring us to the issue list page with no project selected instead of the locked project.
                                locationWithProject.query.project = project.id;
                            }
                            delete locationWithProject.query._allp; //We delete _allp from the URL to keep the hack a bit cleaner, but this is not an ideal solution and will ultimately be replaced with something smarter.
                            ReactRouter.browserHistory.replace(locationWithProject);
                        }
                        this.setState({
                            error: false,
                            loading: false,
                            errorType: null,
                            project: project,
                        });
                        GroupStore.loadInitialData([data]);
                        return [3 /*break*/, 4];
                    case 3:
                        err_1 = _c.sent();
                        errorType = null;
                        switch (err_1 === null || err_1 === void 0 ? void 0 : err_1.status) {
                            case 404:
                                errorType = ERROR_TYPES.GROUP_NOT_FOUND;
                                break;
                            default:
                        }
                        this.setState({
                            loading: false,
                            error: true,
                            errorType: errorType,
                        });
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        });
    };
    GroupDetails.prototype.onGroupChange = function (itemIds) {
        var id = this.props.params.groupId;
        if (itemIds.has(id)) {
            var group = GroupStore.get(id);
            if (group) {
                if (group.stale) {
                    this.fetchData();
                    return;
                }
                this.setState({
                    group: group,
                });
            }
        }
    };
    GroupDetails.prototype.getTitle = function () {
        var group = this.state.group;
        var defaultTitle = 'Sentry';
        if (!group) {
            return defaultTitle;
        }
        switch (group.type) {
            case 'error':
                if (group.metadata.type && group.metadata.value) {
                    return group.metadata.type + ": " + group.metadata.value;
                }
                return group.metadata.type || group.metadata.value || defaultTitle;
            case 'csp':
                return group.metadata.message || defaultTitle;
            case 'expectct':
            case 'expectstaple':
            case 'hpkp':
                return group.metadata.message || defaultTitle;
            case 'default':
                return group.metadata.title || defaultTitle;
            default:
                return '';
        }
    };
    GroupDetails.prototype.renderContent = function (project) {
        var _a = this.props, children = _a.children, environments = _a.environments;
        var group = this.state.group;
        return (<React.Fragment>
        <GroupHeader project={project} group={group}/>
        {React.isValidElement(children)
            ? React.cloneElement(children, {
                environments: environments,
                group: group,
                project: project,
            })
            : children}
      </React.Fragment>);
    };
    GroupDetails.prototype.renderError = function () {
        if (!this.state.error) {
            return null;
        }
        switch (this.state.errorType) {
            case ERROR_TYPES.GROUP_NOT_FOUND:
                return (<LoadingError message={t('The issue you were looking for was not found.')}/>);
            default:
                return <LoadingError onRetry={this.remountComponent}/>;
        }
    };
    GroupDetails.prototype.render = function () {
        var _this = this;
        var organization = this.props.organization;
        var _a = this.state, error = _a.error, group = _a.group, project = _a.project, loading = _a.loading;
        var isError = error;
        var isLoading = loading || (!group && !isError);
        return (<DocumentTitle title={this.getTitle()}>
        <React.Fragment>
          <GlobalSelectionHeader skipLoadLastUsed forceProject={project} showDateSelector={false} shouldForceProject lockedMessageSubject={t('issue')} showIssueStreamLink showProjectSettingsLink>
            <PageContent>
              {isLoading ? (<LoadingIndicator />) : isError ? (this.renderError()) : (<Projects orgId={organization.slug} slugs={[project.slug]}>
                  {function (_a) {
            var projects = _a.projects, initiallyLoaded = _a.initiallyLoaded, fetchError = _a.fetchError;
            return initiallyLoaded ? (fetchError ? (<LoadingError message={t('Error loading the specified project')}/>) : (_this.renderContent(projects[0]))) : (<LoadingIndicator />);
        }}
                </Projects>)}
            </PageContent>
          </GlobalSelectionHeader>
        </React.Fragment>
      </DocumentTitle>);
    };
    GroupDetails.childContextTypes = {
        group: SentryTypes.Group,
        location: PropTypes.object,
    };
    return GroupDetails;
}(React.Component));
export default withApi(withProfiler(GroupDetails));
//# sourceMappingURL=groupDetails.jsx.map