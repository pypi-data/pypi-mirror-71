import { __extends, __rest } from "tslib";
import React from 'react';
import PropTypes from 'prop-types';
import * as Sentry from '@sentry/browser';
import SentryTypes from 'app/sentryTypes';
import UserAvatar from 'app/components/avatar/userAvatar';
import TeamAvatar from 'app/components/avatar/teamAvatar';
import MemberListStore from 'app/stores/memberListStore';
import TeamStore from 'app/stores/teamStore';
var ActorAvatar = /** @class */ (function (_super) {
    __extends(ActorAvatar, _super);
    function ActorAvatar() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    ActorAvatar.prototype.render = function () {
        var _a = this.props, actor = _a.actor, props = __rest(_a, ["actor"]);
        if (actor.type === 'user') {
            var user = actor.id ? MemberListStore.getById(actor.id) : actor;
            return <UserAvatar user={user} {...props}/>;
        }
        if (actor.type === 'team') {
            var team = TeamStore.getById(actor.id);
            return <TeamAvatar team={team} {...props}/>;
        }
        Sentry.withScope(function (scope) {
            scope.setExtra('actor', actor);
            Sentry.captureException(new Error('Unknown avatar type'));
        });
        return null;
    };
    ActorAvatar.propTypes = {
        actor: SentryTypes.Actor.isRequired,
        size: PropTypes.number,
        default: PropTypes.string,
        title: PropTypes.string,
        gravatar: PropTypes.bool,
        hasTooltip: PropTypes.bool,
    };
    ActorAvatar.defaultProps = {
        hasTooltip: true,
    };
    return ActorAvatar;
}(React.Component));
export default ActorAvatar;
//# sourceMappingURL=actorAvatar.jsx.map