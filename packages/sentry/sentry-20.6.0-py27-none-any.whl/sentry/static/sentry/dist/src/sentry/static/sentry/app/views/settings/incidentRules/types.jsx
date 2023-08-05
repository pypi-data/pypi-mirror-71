export var AlertRuleThreshold;
(function (AlertRuleThreshold) {
    AlertRuleThreshold[AlertRuleThreshold["INCIDENT"] = 0] = "INCIDENT";
    AlertRuleThreshold[AlertRuleThreshold["RESOLUTION"] = 1] = "RESOLUTION";
})(AlertRuleThreshold || (AlertRuleThreshold = {}));
export var AlertRuleThresholdType;
(function (AlertRuleThresholdType) {
    AlertRuleThresholdType[AlertRuleThresholdType["ABOVE"] = 0] = "ABOVE";
    AlertRuleThresholdType[AlertRuleThresholdType["BELOW"] = 1] = "BELOW";
})(AlertRuleThresholdType || (AlertRuleThresholdType = {}));
export var Dataset;
(function (Dataset) {
    Dataset["ERRORS"] = "events";
    Dataset["TRANSACTIONS"] = "transactions";
})(Dataset || (Dataset = {}));
export var TimeWindow;
(function (TimeWindow) {
    TimeWindow[TimeWindow["ONE_MINUTE"] = 1] = "ONE_MINUTE";
    TimeWindow[TimeWindow["FIVE_MINUTES"] = 5] = "FIVE_MINUTES";
    TimeWindow[TimeWindow["TEN_MINUTES"] = 10] = "TEN_MINUTES";
    TimeWindow[TimeWindow["FIFTEEN_MINUTES"] = 15] = "FIFTEEN_MINUTES";
    TimeWindow[TimeWindow["THIRTY_MINUTES"] = 30] = "THIRTY_MINUTES";
    TimeWindow[TimeWindow["ONE_HOUR"] = 60] = "ONE_HOUR";
    TimeWindow[TimeWindow["TWO_HOURS"] = 120] = "TWO_HOURS";
    TimeWindow[TimeWindow["FOUR_HOURS"] = 240] = "FOUR_HOURS";
    TimeWindow[TimeWindow["ONE_DAY"] = 1440] = "ONE_DAY";
})(TimeWindow || (TimeWindow = {}));
export var ActionType;
(function (ActionType) {
    ActionType["EMAIL"] = "email";
    ActionType["SLACK"] = "slack";
    ActionType["PAGER_DUTY"] = "pagerduty";
})(ActionType || (ActionType = {}));
export var TargetType;
(function (TargetType) {
    // The name can be customized for each integration. Email for email, channel for slack, service for Pagerduty). We probably won't support this for email at first, since we need to be careful not to enable spam
    TargetType["SPECIFIC"] = "specific";
    // Just works with email for now, grabs given user's email address
    TargetType["USER"] = "user";
    // Just works with email for now, grabs the emails for all team members
    TargetType["TEAM"] = "team";
})(TargetType || (TargetType = {}));
//# sourceMappingURL=types.jsx.map