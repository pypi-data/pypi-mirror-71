var DEFAULT_EMPTY_ROUTING_NAME = 'none';
var DEFAULT_EMPTY_ENV_NAME = '(No Environment)';
export function getUrlRoutingName(env) {
    return encodeURIComponent(env.name) || DEFAULT_EMPTY_ROUTING_NAME;
}
export function getDisplayName(env) {
    return env.name || DEFAULT_EMPTY_ENV_NAME;
}
//# sourceMappingURL=environment.jsx.map