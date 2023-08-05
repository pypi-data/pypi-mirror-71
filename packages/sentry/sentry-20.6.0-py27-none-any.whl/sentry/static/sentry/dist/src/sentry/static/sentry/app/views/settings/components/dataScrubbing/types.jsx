export var RuleType;
(function (RuleType) {
    RuleType["PATTERN"] = "pattern";
    RuleType["CREDITCARD"] = "creditcard";
    RuleType["PASSWORD"] = "password";
    RuleType["IP"] = "ip";
    RuleType["IMEI"] = "imei";
    RuleType["EMAIL"] = "email";
    RuleType["UUID"] = "uuid";
    RuleType["PEMKEY"] = "pemkey";
    RuleType["URLAUTH"] = "urlauth";
    RuleType["USSSN"] = "usssn";
    RuleType["USER_PATH"] = "userpath";
    RuleType["MAC"] = "mac";
    RuleType["ANYTHING"] = "anything";
})(RuleType || (RuleType = {}));
export var MethodType;
(function (MethodType) {
    MethodType["MASK"] = "mask";
    MethodType["REMOVE"] = "remove";
    MethodType["HASH"] = "hash";
    MethodType["REPLACE"] = "replace";
})(MethodType || (MethodType = {}));
export var EventIdStatus;
(function (EventIdStatus) {
    EventIdStatus["LOADING"] = "loading";
    EventIdStatus["INVALID"] = "invalid";
    EventIdStatus["NOT_FOUND"] = "not_found";
    EventIdStatus["LOADED"] = "loaded";
    EventIdStatus["ERROR"] = "error";
})(EventIdStatus || (EventIdStatus = {}));
export var SourceSuggestionType;
(function (SourceSuggestionType) {
    SourceSuggestionType["VALUE"] = "value";
    SourceSuggestionType["UNARY"] = "unary";
    SourceSuggestionType["BINARY"] = "binary";
    SourceSuggestionType["STRING"] = "string";
})(SourceSuggestionType || (SourceSuggestionType = {}));
export var RequestError;
(function (RequestError) {
    RequestError["Unknown"] = "unknown";
    RequestError["InvalidSelector"] = "invalid-selector";
    RequestError["RegexParse"] = "regex-parse";
})(RequestError || (RequestError = {}));
//# sourceMappingURL=types.jsx.map