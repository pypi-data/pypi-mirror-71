import { __assign, __extends, __read } from "tslib";
import React from 'react';
import withApi from 'app/utils/withApi';
import { isAPIPayloadSimilar } from 'app/utils/discover/eventView';
var DiscoverQuery = /** @class */ (function (_super) {
    __extends(DiscoverQuery, _super);
    function DiscoverQuery() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            isLoading: true,
            tableFetchID: undefined,
            error: null,
            tableData: null,
            pageLinks: null,
        };
        _this.shouldRefetchData = function (prevProps) {
            var thisAPIPayload = _this.props.eventView.getEventsAPIPayload(_this.props.location);
            var otherAPIPayload = prevProps.eventView.getEventsAPIPayload(prevProps.location);
            return (!isAPIPayloadSimilar(thisAPIPayload, otherAPIPayload) ||
                prevProps.limit !== _this.props.limit);
        };
        _this.fetchData = function () {
            var _a = _this.props, eventView = _a.eventView, orgSlug = _a.orgSlug, location = _a.location, limit = _a.limit, keyTransactions = _a.keyTransactions;
            if (!eventView.isValid()) {
                return;
            }
            var route = keyTransactions ? 'key-transactions' : 'eventsv2';
            var url = "/organizations/" + orgSlug + "/" + route + "/";
            var tableFetchID = Symbol('tableFetchID');
            var apiPayload = eventView.getEventsAPIPayload(location);
            _this.setState({ isLoading: true, tableFetchID: tableFetchID });
            if (limit) {
                apiPayload.per_page = limit;
            }
            _this.props.api
                .requestPromise(url, {
                method: 'GET',
                includeAllArgs: true,
                query: __assign({}, apiPayload),
            })
                .then(function (_a) {
                var _b = __read(_a, 3), data = _b[0], _ = _b[1], jqXHR = _b[2];
                if (_this.state.tableFetchID !== tableFetchID) {
                    // invariant: a different request was initiated after this request
                    return;
                }
                _this.setState(function (prevState) { return ({
                    isLoading: false,
                    tableFetchID: undefined,
                    error: null,
                    pageLinks: jqXHR ? jqXHR.getResponseHeader('Link') : prevState.pageLinks,
                    tableData: data,
                }); });
            })
                .catch(function (err) {
                var _a, _b;
                _this.setState({
                    isLoading: false,
                    tableFetchID: undefined,
                    error: (_b = (_a = err === null || err === void 0 ? void 0 : err.responseJSON) === null || _a === void 0 ? void 0 : _a.detail) !== null && _b !== void 0 ? _b : null,
                    tableData: null,
                });
            });
        };
        return _this;
    }
    DiscoverQuery.prototype.componentDidMount = function () {
        this.fetchData();
    };
    DiscoverQuery.prototype.componentDidUpdate = function (prevProps) {
        // Reload data if we aren't already loading,
        var refetchCondition = !this.state.isLoading && this.shouldRefetchData(prevProps);
        // or if we've moved from an invalid view state to a valid one,
        var eventViewValidation = prevProps.eventView.isValid() === false && this.props.eventView.isValid();
        // or if toggling between key transactions and all transactions
        var togglingTransactionsView = prevProps.keyTransactions !== this.props.keyTransactions;
        if (refetchCondition || eventViewValidation || togglingTransactionsView) {
            this.fetchData();
        }
    };
    DiscoverQuery.prototype.render = function () {
        var _a = this.state, isLoading = _a.isLoading, error = _a.error, tableData = _a.tableData, pageLinks = _a.pageLinks;
        var childrenProps = {
            isLoading: isLoading,
            error: error,
            tableData: tableData,
            pageLinks: pageLinks,
        };
        return this.props.children(childrenProps);
    };
    DiscoverQuery.defaultProps = {
        keyTransactions: false,
    };
    return DiscoverQuery;
}(React.Component));
export default withApi(DiscoverQuery);
//# sourceMappingURL=discoverQuery.jsx.map