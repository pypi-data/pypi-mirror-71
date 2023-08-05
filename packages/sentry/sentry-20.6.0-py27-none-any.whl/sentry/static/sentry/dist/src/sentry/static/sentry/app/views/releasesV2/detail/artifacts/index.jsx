import { __extends } from "tslib";
import React from 'react';
import { t, tct } from 'app/locale';
import ReleaseArtifactsV1 from 'app/views/releases/detail/releaseArtifacts';
import AsyncView from 'app/views/asyncView';
import routeTitleGen from 'app/utils/routeTitle';
import { formatVersion } from 'app/utils/formatters';
import withOrganization from 'app/utils/withOrganization';
import AlertLink from 'app/components/alertLink';
import Feature from 'app/components/acl/feature';
import { ReleaseContext } from '..';
var ReleaseArtifacts = /** @class */ (function (_super) {
    __extends(ReleaseArtifacts, _super);
    function ReleaseArtifacts() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    ReleaseArtifacts.prototype.getTitle = function () {
        var _a = this.props, params = _a.params, organization = _a.organization;
        return routeTitleGen(t('Artifacts - Release %s', formatVersion(params.release)), organization.slug, false);
    };
    ReleaseArtifacts.prototype.renderBody = function () {
        var project = this.context.project;
        var _a = this.props, params = _a.params, location = _a.location, organization = _a.organization;
        return (<React.Fragment>
        <Feature features={['artifacts-in-settings']}>
          {function (_a) {
            var hasFeature = _a.hasFeature;
            return hasFeature ? (<AlertLink to={"/settings/" + organization.slug + "/projects/" + project.slug + "/source-maps/" + encodeURIComponent(params.release) + "/"} priority="info">
                {tct('Artifacts were moved to [sourceMaps] in Settings.', {
                sourceMaps: <u>{t('Source Maps')}</u>,
            })}
              </AlertLink>) : (<ReleaseArtifactsV1 params={params} location={location} projectId={project.slug} smallEmptyMessage/>);
        }}
        </Feature>
      </React.Fragment>);
    };
    ReleaseArtifacts.contextType = ReleaseContext;
    return ReleaseArtifacts;
}(AsyncView));
export default withOrganization(ReleaseArtifacts);
//# sourceMappingURL=index.jsx.map