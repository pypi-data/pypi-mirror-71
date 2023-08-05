import React from 'react';
import Reflux from 'reflux';
import createReactClass from 'create-react-class';
import getDisplayName from 'app/utils/getDisplayName';
import TagStore from 'app/stores/tagStore';
/**
 * HOC for getting *only* tags from the TagStore.
 */
var withTags = function (WrappedComponent) {
    return createReactClass({
        displayName: "withTags(" + getDisplayName(WrappedComponent) + ")",
        mixins: [Reflux.listenTo(TagStore, 'onTagsUpdate')],
        getInitialState: function () {
            return {
                tags: TagStore.getAllTags(),
            };
        },
        onTagsUpdate: function (tags) {
            this.setState({
                tags: tags,
            });
        },
        render: function () {
            return <WrappedComponent tags={this.state.tags} {...this.props}/>;
        },
    });
};
export default withTags;
//# sourceMappingURL=withTags.jsx.map