import { __assign, __extends, __rest } from "tslib";
import isEqual from 'lodash/isEqual';
import createReactClass from 'create-react-class';
import React from 'react';
import Reflux from 'reflux';
import PropTypes from 'prop-types';
import BaseBadge from 'app/components/idBadge/baseBadge';
import BadgeDisplayName from 'app/components/idBadge/badgeDisplayName';
import SentryTypes from 'app/sentryTypes';
import TeamStore from 'app/stores/teamStore';
var TeamBadge = /** @class */ (function (_super) {
    __extends(TeamBadge, _super);
    function TeamBadge() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    TeamBadge.prototype.render = function () {
        var _a = this.props, hideOverflow = _a.hideOverflow, team = _a.team, props = __rest(_a, ["hideOverflow", "team"]);
        return (<BaseBadge displayName={<BadgeDisplayName hideOverflow={hideOverflow}>#{team.slug}</BadgeDisplayName>} team={team} {...props}/>);
    };
    TeamBadge.propTypes = __assign(__assign({}, BaseBadge.propTypes), { team: SentryTypes.Team.isRequired, avatarSize: PropTypes.number, hideOverflow: PropTypes.oneOfType([PropTypes.bool, PropTypes.string]), hideAvatar: PropTypes.bool });
    TeamBadge.defaultProps = {
        avatarSize: 24,
        hideOverflow: true,
        hideAvatar: false,
    };
    return TeamBadge;
}(React.Component));
var TeamBadgeContainer = createReactClass({
    displayName: 'TeamBadgeContainer',
    propTypes: {
        team: SentryTypes.Team.isRequired,
    },
    mixins: [Reflux.listenTo(TeamStore, 'onTeamStoreUpdate')],
    getInitialState: function () {
        return {
            team: this.props.team,
        };
    },
    componentWillReceiveProps: function (nextProps) {
        if (this.state.team === nextProps.team) {
            return;
        }
        if (isEqual(this.state.team, nextProps.team)) {
            return;
        }
        this.setState({
            team: nextProps.team,
        });
    },
    onTeamStoreUpdate: function (updatedTeam) {
        if (!updatedTeam.has(this.state.team.id)) {
            return;
        }
        var team = TeamStore.getById(this.state.team.id);
        if (!team || isEqual(team.avatar, this.state.team.avatar)) {
            return;
        }
        this.setState({ team: team });
    },
    render: function () {
        return <TeamBadge {...this.props} team={this.state.team}/>;
    },
});
export default TeamBadgeContainer;
//# sourceMappingURL=teamBadge.jsx.map