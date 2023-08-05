import { __extends } from "tslib";
import React from 'react';
import PropTypes from 'prop-types';
import { Metadata } from 'app/sentryTypes';
import { getTitle } from 'app/utils/events';
import GuideAnchor from 'app/components/assistant/guideAnchor';
var EventOrGroupTitle = /** @class */ (function (_super) {
    __extends(EventOrGroupTitle, _super);
    function EventOrGroupTitle() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    EventOrGroupTitle.prototype.render = function () {
        var _a = getTitle(this.props.data), title = _a.title, subtitle = _a.subtitle;
        var hasGuideAnchor = this.props.hasGuideAnchor;
        return subtitle ? (<span style={this.props.style}>
        <GuideAnchor disabled={!hasGuideAnchor} target="issue_title" position="bottom">
          <span>{title}</span>
        </GuideAnchor>
        <Spacer />
        <em title={subtitle}>{subtitle}</em>
        <br />
      </span>) : (<span style={this.props.style}>
        <GuideAnchor disabled={!hasGuideAnchor} target="issue_title" position="bottom">
          {title}
        </GuideAnchor>
      </span>);
    };
    EventOrGroupTitle.propTypes = {
        data: PropTypes.shape({
            type: PropTypes.oneOf([
                'error',
                'csp',
                'hpkp',
                'expectct',
                'expectstaple',
                'default',
                'transaction',
            ]).isRequired,
            title: PropTypes.string,
            metadata: Metadata.isRequired,
            culprit: PropTypes.string,
        }),
        style: PropTypes.object,
    };
    return EventOrGroupTitle;
}(React.Component));
export default EventOrGroupTitle;
/**
 * &nbsp; is used instead of margin/padding to split title and subtitle
 * into 2 separate text nodes on the HTML AST. This allows the
 * title to be highlighted without spilling over to the subtitle.
 */
var Spacer = function () { return <span style={{ display: 'inline-block', width: 10 }}>&nbsp;</span>; };
//# sourceMappingURL=eventOrGroupTitle.jsx.map