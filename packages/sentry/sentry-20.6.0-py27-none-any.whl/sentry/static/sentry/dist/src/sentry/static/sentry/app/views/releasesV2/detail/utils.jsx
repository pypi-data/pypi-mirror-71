import { Client } from 'app/api';
import { t } from 'app/locale';
export var deleteRelease = function (orgId, version) {
    var api = new Client();
    return api.requestPromise("/organizations/" + orgId + "/releases/" + encodeURIComponent(version) + "/", {
        method: 'DELETE',
    });
};
/**
 * Convert list of individual file changes into a per-file summary grouped by repository
 */
export function getFilesByRepository(fileList) {
    return fileList.reduce(function (filesByRepository, file) {
        var filename = file.filename, repoName = file.repoName, author = file.author, type = file.type;
        if (!filesByRepository.hasOwnProperty(repoName)) {
            filesByRepository[repoName] = {};
        }
        if (!filesByRepository[repoName].hasOwnProperty(filename)) {
            filesByRepository[repoName][filename] = {
                authors: {},
                types: new Set(),
            };
        }
        filesByRepository[repoName][filename].authors[author.email] = author;
        filesByRepository[repoName][filename].types.add(type);
        return filesByRepository;
    }, {});
}
/**
 * Convert list of individual commits into a summary grouped by repository
 */
export function getCommitsByRepository(commitList) {
    return commitList.reduce(function (commitsByRepository, commit) {
        var _a, _b;
        var repositoryName = (_b = (_a = commit.repository) === null || _a === void 0 ? void 0 : _a.name) !== null && _b !== void 0 ? _b : t('unknown');
        if (!commitsByRepository.hasOwnProperty(repositoryName)) {
            commitsByRepository[repositoryName] = [];
        }
        commitsByRepository[repositoryName].push(commit);
        return commitsByRepository;
    }, {});
}
//# sourceMappingURL=utils.jsx.map