import { __assign, __extends } from "tslib";
import React from 'react';
import AsyncView from 'app/views/asyncView';
import RuleForm from 'app/views/settings/incidentRules/ruleForm';
import recreateRoute from 'app/utils/recreateRoute';
var IncidentRulesDetails = /** @class */ (function (_super) {
    __extends(IncidentRulesDetails, _super);
    function IncidentRulesDetails() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleSubmitSuccess = function () {
            var _a = _this.props, params = _a.params, routes = _a.routes, router = _a.router, location = _a.location;
            router.push(recreateRoute('', { params: params, routes: routes, location: location, stepBack: -2 }));
        };
        return _this;
    }
    IncidentRulesDetails.prototype.getDefaultState = function () {
        return __assign(__assign({}, _super.prototype.getDefaultState.call(this)), { actions: new Map() });
    };
    IncidentRulesDetails.prototype.getEndpoints = function () {
        var _a = this.props.params, orgId = _a.orgId, projectId = _a.projectId, ruleId = _a.ruleId;
        return [['rule', "/projects/" + orgId + "/" + projectId + "/alert-rules/" + ruleId + "/"]];
    };
    IncidentRulesDetails.prototype.renderBody = function () {
        var ruleId = this.props.params.ruleId;
        var rule = this.state.rule;
        return (<RuleForm {...this.props} ruleId={ruleId} rule={rule} onSubmitSuccess={this.handleSubmitSuccess}/>);
    };
    return IncidentRulesDetails;
}(AsyncView));
export default IncidentRulesDetails;
//# sourceMappingURL=details.jsx.map