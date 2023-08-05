import { __assign, __rest } from "tslib";
import Reflux from 'reflux';
import RepoActions from 'app/actions/repositoryActions';
export var RepositoryStoreConfig = {
    listenables: RepoActions,
    state: {
        orgSlug: undefined,
        repositories: undefined,
        repositoriesLoading: undefined,
        repositoriesError: undefined,
    },
    init: function () {
        this.resetRepositories();
    },
    resetRepositories: function () {
        this.state = {
            orgSlug: undefined,
            repositories: undefined,
            repositoriesLoading: undefined,
            repositoriesError: undefined,
        };
        this.trigger(this.state);
    },
    loadRepositories: function (orgSlug) {
        this.state = {
            orgSlug: orgSlug,
            repositories: orgSlug === this.state.orgSlug ? this.state.repositories : undefined,
            repositoriesLoading: true,
            repositoriesError: undefined,
        };
        this.trigger(this.state);
    },
    loadRepositoriesError: function (err) {
        this.state = __assign(__assign({}, this.state), { repositories: undefined, repositoriesLoading: false, repositoriesError: err });
        this.trigger(this.state);
    },
    loadRepositoriesSuccess: function (data) {
        this.state = __assign(__assign({}, this.state), { repositories: data, repositoriesLoading: false, repositoriesError: undefined });
        this.trigger(this.state);
    },
    /**
     * `orgSlug` is optional. If present, method will run a check if data in the
     * store originated from the same organization
     */
    get: function (orgSlug) {
        var _a = this.state, stateOrgSlug = _a.orgSlug, data = __rest(_a, ["orgSlug"]);
        if (orgSlug !== undefined && orgSlug !== stateOrgSlug) {
            return {
                repositories: undefined,
                repositoriesLoading: undefined,
                repositoriesError: undefined,
            };
        }
        return __assign({}, data);
    },
};
export default Reflux.createStore(RepositoryStoreConfig);
//# sourceMappingURL=repositoryStore.jsx.map