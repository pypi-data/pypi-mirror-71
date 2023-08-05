import { __awaiter, __generator } from "tslib";
import * as Sentry from '@sentry/browser';
import * as Router from 'react-router';
import { createMemoryHistory } from 'history';
import set from 'lodash/set';
import getRouteStringFromRoutes from 'app/utils/getRouteStringFromRoutes';
var createLocation = createMemoryHistory().createLocation;
/**
 * Sets the transaction name
 */
export function setTransactionName(name) {
    Sentry.configureScope(function (scope) {
        scope.setTransaction(name);
        scope.setTag('ui.route', name);
    });
}
export function normalizeTransactionName(appRoutes, event) {
    return __awaiter(this, void 0, void 0, function () {
        var prevTransactionName, transactionName;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    if (event.type !== 'transaction') {
                        return [2 /*return*/, event];
                    }
                    prevTransactionName = event.transaction;
                    if (typeof prevTransactionName === 'string' && prevTransactionName.length > 0) {
                        if (prevTransactionName.startsWith('/')) {
                            return [2 /*return*/, event];
                        }
                        set(event, ['tags', 'transaction.rename.source'], 'existing transaction name');
                    }
                    else {
                        set(event, ['tags', 'transaction.rename.source'], 'window.location.pathname');
                        prevTransactionName = window.location.pathname;
                    }
                    return [4 /*yield*/, new Promise(function (resolve) {
                            Router.match({
                                routes: appRoutes,
                                location: createLocation(prevTransactionName),
                            }, function (error, _redirectLocation, renderProps) {
                                var _a;
                                if (error) {
                                    set(event, ['tags', 'transaction.rename.router-match'], 'error');
                                    return resolve(window.location.pathname);
                                }
                                set(event, ['tags', 'transaction.rename.router-match'], 'success');
                                var routePath = getRouteStringFromRoutes((_a = renderProps === null || renderProps === void 0 ? void 0 : renderProps.routes) !== null && _a !== void 0 ? _a : []);
                                if (routePath.length === 0 || routePath === '/*') {
                                    return resolve(window.location.pathname);
                                }
                                return resolve(routePath);
                            });
                        })];
                case 1:
                    transactionName = _a.sent();
                    event.transaction = transactionName;
                    set(event, ['tags', 'transaction.rename.before'], prevTransactionName);
                    set(event, ['tags', 'transaction.rename.after'], transactionName);
                    set(event, ['tags', 'ui.route'], transactionName);
                    return [2 /*return*/, event];
            }
        });
    });
}
//# sourceMappingURL=apm.jsx.map