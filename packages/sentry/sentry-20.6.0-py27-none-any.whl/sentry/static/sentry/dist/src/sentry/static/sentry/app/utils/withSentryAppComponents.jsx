import React from 'react';
import Reflux from 'reflux';
import createReactClass from 'create-react-class';
import getDisplayName from 'app/utils/getDisplayName';
import SentryAppComponentsStore from 'app/stores/sentryAppComponentsStore';
var withSentryAppComponents = function (WrappedComponent, _a) {
    var componentType = (_a === void 0 ? {} : _a).componentType;
    return createReactClass({
        displayName: "withSentryAppComponents(" + getDisplayName(WrappedComponent) + ")",
        mixins: [Reflux.connect(SentryAppComponentsStore, 'components')],
        render: function () {
            return (<WrappedComponent components={SentryAppComponentsStore.getComponentByType(componentType)} {...this.props}/>);
        },
    });
};
export default withSentryAppComponents;
//# sourceMappingURL=withSentryAppComponents.jsx.map