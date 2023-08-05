import { __extends, __rest } from "tslib";
import * as Sentry from '@sentry/browser';
import React from 'react';
import SettingsNavigationGroup from 'app/views/settings/components/settingsNavigationGroup';
var SettingsNavigation = /** @class */ (function (_super) {
    __extends(SettingsNavigation, _super);
    function SettingsNavigation() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    SettingsNavigation.prototype.componentDidCatch = function (error, errorInfo) {
        Sentry.withScope(function (scope) {
            Object.keys(errorInfo).forEach(function (key) {
                scope.setExtra(key, errorInfo[key]);
            });
            scope.setExtra('url', window.location.href);
            Sentry.captureException(error);
        });
    };
    SettingsNavigation.prototype.render = function () {
        var _a = this.props, navigationObjects = _a.navigationObjects, hooks = _a.hooks, hookConfigs = _a.hookConfigs, otherProps = __rest(_a, ["navigationObjects", "hooks", "hookConfigs"]);
        var navWithHooks = navigationObjects.concat(hookConfigs);
        return (<div>
        {navWithHooks.map(function (config) { return (<SettingsNavigationGroup key={config.name} {...otherProps} {...config}/>); })}
        {hooks.map(function (Hook, i) { return React.cloneElement(Hook, { key: "hook-" + i }); })}
      </div>);
    };
    SettingsNavigation.defaultProps = {
        hooks: [],
        hookConfigs: [],
    };
    return SettingsNavigation;
}(React.Component));
export default SettingsNavigation;
//# sourceMappingURL=settingsNavigation.jsx.map