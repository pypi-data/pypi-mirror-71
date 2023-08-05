import * as Sentry from '@sentry/browser';
import ReleaseActions from 'app/actions/releaseActions';
import ReleaseStore, { getReleaseStoreKey } from 'app/stores/releaseStore';
export function getProjectRelease(api, params) {
    var orgSlug = params.orgSlug, projectSlug = params.projectSlug, releaseVersion = params.releaseVersion;
    var path = "/projects/" + orgSlug + "/" + projectSlug + "/releases/" + encodeURIComponent(releaseVersion) + "/";
    // HACK(leedongwei): Actions fired by the ActionCreators are queued to
    // the back of the event loop, allowing another getRelease for the same
    // release to be fired before the loading state is updated in store.
    // This hack short-circuits that and update the state immediately.
    ReleaseStore.state.releaseLoading[getReleaseStoreKey(projectSlug, releaseVersion)] = true;
    ReleaseActions.loadRelease(orgSlug, projectSlug, releaseVersion);
    return api
        .requestPromise(path, {
        method: 'GET',
    })
        .then(function (res) {
        ReleaseActions.loadReleaseSuccess(projectSlug, releaseVersion, res);
    })
        .catch(function (err) {
        ReleaseActions.loadReleaseError(projectSlug, releaseVersion, err);
        Sentry.withScope(function (scope) {
            scope.setLevel(Sentry.Severity.Warning);
            scope.setFingerprint(['getRelease-action-creator']);
            Sentry.captureException(err);
        });
    });
}
export function getReleaseDeploys(api, params) {
    var orgSlug = params.orgSlug, projectSlug = params.projectSlug, releaseVersion = params.releaseVersion;
    var path = "/organizations/" + orgSlug + "/releases/" + encodeURIComponent(releaseVersion) + "/deploys/";
    // HACK(leedongwei): Same as above
    ReleaseStore.state.deploysLoading[getReleaseStoreKey(projectSlug, releaseVersion)] = true;
    ReleaseActions.loadDeploys(orgSlug, projectSlug, releaseVersion);
    return api
        .requestPromise(path, {
        method: 'GET',
    })
        .then(function (res) {
        ReleaseActions.loadDeploysSuccess(projectSlug, releaseVersion, res);
    })
        .catch(function (err) {
        ReleaseActions.loadDeploysError(projectSlug, releaseVersion, err);
        Sentry.withScope(function (scope) {
            scope.setLevel(Sentry.Severity.Warning);
            scope.setFingerprint(['getReleaseDeploys-action-creator']);
            Sentry.captureException(err);
        });
    });
}
//# sourceMappingURL=release.jsx.map