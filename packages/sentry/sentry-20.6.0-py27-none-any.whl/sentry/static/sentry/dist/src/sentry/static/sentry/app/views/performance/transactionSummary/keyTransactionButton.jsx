import { __extends, __read } from "tslib";
import React from 'react';
import withApi from 'app/utils/withApi';
import Button from 'app/components/button';
import { IconStar } from 'app/icons';
import { t } from 'app/locale';
import { saveKeyTransaction, deleteKeyTransaction } from 'app/actionCreators/performance';
var KeyTransactionButton = /** @class */ (function (_super) {
    __extends(KeyTransactionButton, _super);
    function KeyTransactionButton() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            isLoading: true,
            keyFetchID: undefined,
            error: null,
            isKeyTransaction: false,
        };
        _this.fetchData = function () {
            var _a = _this.props, organization = _a.organization, eventView = _a.eventView, transactionName = _a.transactionName;
            var projects = eventView.project;
            if (projects.length !== 1) {
                return;
            }
            var url = "/organizations/" + organization.slug + "/is-key-transactions/";
            var keyFetchID = Symbol('keyFetchID');
            _this.setState({ isLoading: true, keyFetchID: keyFetchID });
            _this.props.api
                .requestPromise(url, {
                method: 'GET',
                includeAllArgs: true,
                query: {
                    project: projects.map(function (id) { return String(id); }),
                    transaction: transactionName,
                },
            })
                .then(function (_a) {
                var _b = __read(_a, 3), data = _b[0], _ = _b[1], _jqXHR = _b[2];
                if (_this.state.keyFetchID !== keyFetchID) {
                    // invariant: a different request was initiated after this request
                    return;
                }
                _this.setState({
                    isLoading: false,
                    keyFetchID: undefined,
                    error: null,
                    isKeyTransaction: !!(data === null || data === void 0 ? void 0 : data.isKey),
                });
            })
                .catch(function (err) {
                _this.setState({
                    isLoading: false,
                    keyFetchID: undefined,
                    error: err.responseJSON.detail,
                    isKeyTransaction: false,
                });
            });
        };
        _this.toggleKeyTransaction = function () {
            var _a = _this.props, eventView = _a.eventView, api = _a.api, organization = _a.organization, transactionName = _a.transactionName;
            var projects = eventView.project;
            if (!_this.state.isKeyTransaction) {
                _this.setState({
                    isKeyTransaction: true,
                });
                saveKeyTransaction(api, organization.slug, projects, transactionName).catch(function () {
                    _this.setState({
                        isKeyTransaction: false,
                    });
                });
            }
            else {
                _this.setState({
                    isKeyTransaction: false,
                });
                deleteKeyTransaction(api, organization.slug, projects, transactionName).catch(function () {
                    _this.setState({
                        isKeyTransaction: true,
                    });
                });
            }
        };
        return _this;
    }
    KeyTransactionButton.prototype.componentDidMount = function () {
        this.fetchData();
    };
    KeyTransactionButton.prototype.componentDidUpdate = function (prevProps) {
        var orgSlugChanged = prevProps.organization.slug !== this.props.organization.slug;
        var projectsChanged = prevProps.eventView.project.length === 1 &&
            this.props.eventView.project.length === 1 &&
            prevProps.eventView.project[0] !== this.props.eventView.project[0];
        if (orgSlugChanged || projectsChanged) {
            this.fetchData();
        }
    };
    KeyTransactionButton.prototype.render = function () {
        var _a = this.state, isKeyTransaction = _a.isKeyTransaction, isLoading = _a.isLoading;
        if (this.props.eventView.project.length !== 1 || isLoading) {
            return null;
        }
        return (<Button icon={<IconStar size="xs" color={isKeyTransaction ? 'yellow' : 'gray500'} isSolid={!!isKeyTransaction}/>} onClick={this.toggleKeyTransaction}>
        {t('Key Transaction')}
      </Button>);
    };
    return KeyTransactionButton;
}(React.Component));
export default withApi(KeyTransactionButton);
//# sourceMappingURL=keyTransactionButton.jsx.map