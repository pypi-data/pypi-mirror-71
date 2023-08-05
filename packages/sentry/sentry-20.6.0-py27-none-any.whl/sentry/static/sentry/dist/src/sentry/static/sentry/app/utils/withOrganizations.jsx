import React from 'react';
import Reflux from 'reflux';
import createReactClass from 'create-react-class';
import getDisplayName from 'app/utils/getDisplayName';
import OrganizationsStore from 'app/stores/organizationsStore';
var withOrganizations = function (WrappedComponent) {
    return createReactClass({
        displayName: "withOrganizations(" + getDisplayName(WrappedComponent) + ")",
        mixins: [Reflux.connect(OrganizationsStore, 'organizations')],
        render: function () {
            return (<WrappedComponent organizationsLoading={!OrganizationsStore.loaded} organizations={this.state.organizations} {...this.props}/>);
        },
    });
};
export default withOrganizations;
//# sourceMappingURL=withOrganizations.jsx.map