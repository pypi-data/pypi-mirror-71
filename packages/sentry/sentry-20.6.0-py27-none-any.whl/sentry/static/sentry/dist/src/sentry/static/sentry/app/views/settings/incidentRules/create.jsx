import { __assign, __extends, __rest } from "tslib";
import React from 'react';
import { createDefaultRule } from 'app/views/settings/incidentRules/constants';
import recreateRoute from 'app/utils/recreateRoute';
import RuleForm from './ruleForm';
/**
 * Show metric rules form with an empty rule. Redirects to alerts list after creation.
 */
var IncidentRulesCreate = /** @class */ (function (_super) {
    __extends(IncidentRulesCreate, _super);
    function IncidentRulesCreate() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleSubmitSuccess = function () {
            var _a = _this.props, params = _a.params, routes = _a.routes, router = _a.router, location = _a.location;
            router.push(recreateRoute('', { params: params, routes: routes, location: location, stepBack: -1 }));
        };
        return _this;
    }
    IncidentRulesCreate.prototype.render = function () {
        var _a = this.props, project = _a.project, props = __rest(_a, ["project"]);
        return (<RuleForm onSubmitSuccess={this.handleSubmitSuccess} rule={__assign(__assign({}, createDefaultRule()), { projects: [project.slug] })} {...props}/>);
    };
    return IncidentRulesCreate;
}(React.Component));
export default IncidentRulesCreate;
//# sourceMappingURL=create.jsx.map