import { __assign } from "tslib";
import React from 'react';
import Reflux from 'reflux';
import createReactClass from 'create-react-class';
import getDisplayName from 'app/utils/getDisplayName';
import RepositoryStore from 'app/stores/repositoryStore';
import { getRepositories } from 'app/actionCreators/repositories';
var withRepositories = function (WrappedComponent) {
    return createReactClass({
        displayName: "withRepositories(" + getDisplayName(WrappedComponent) + ")",
        mixins: [Reflux.listenTo(RepositoryStore, 'onStoreUpdate')],
        getInitialState: function () {
            var orgSlug = this.props.orgSlug;
            var repoData = RepositoryStore.get(orgSlug);
            return __assign({ repositories: undefined, repositoriesLoading: undefined, repositoriesError: undefined }, repoData);
        },
        componentDidMount: function () {
            // XXX(leedongwei): Do not move this function call unless you modify the
            // unit test named "prevents repeated calls"
            this.fetchRepositories();
        },
        fetchRepositories: function () {
            var _a = this.props, api = _a.api, orgSlug = _a.orgSlug;
            var repoData = RepositoryStore.get(orgSlug);
            if (!repoData.repositories && !repoData.repositoriesLoading) {
                getRepositories(api, { orgSlug: orgSlug });
            }
        },
        onStoreUpdate: function () {
            var orgSlug = this.props.orgSlug;
            var repoData = RepositoryStore.get(orgSlug);
            this.setState(__assign({}, repoData));
        },
        render: function () {
            return <WrappedComponent {...this.props} {...this.state}/>;
        },
    });
};
export default withRepositories;
//# sourceMappingURL=withRepositories.jsx.map