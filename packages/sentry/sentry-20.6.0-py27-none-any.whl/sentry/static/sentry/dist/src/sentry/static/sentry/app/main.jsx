import { __extends } from "tslib";
import { CacheProvider } from '@emotion/core'; // This is needed to set "speedy" = false (for percy)
import { ThemeProvider } from 'emotion-theming';
import { cache } from 'emotion'; // eslint-disable-line emotion/no-vanilla
import React from 'react';
import { Router, browserHistory } from 'react-router';
import GlobalStyles from 'app/styles/global';
import routes from 'app/routes';
import theme from 'app/utils/theme';
import { loadPreferencesState } from 'app/actionCreators/preferences';
var Main = /** @class */ (function (_super) {
    __extends(Main, _super);
    function Main() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    Main.prototype.componentDidMount = function () {
        loadPreferencesState();
    };
    Main.prototype.render = function () {
        return (<CacheProvider value={cache}>
        <ThemeProvider theme={theme}>
          <GlobalStyles theme={theme}/>
          <Router history={browserHistory}>{routes()}</Router>
        </ThemeProvider>
      </CacheProvider>);
    };
    return Main;
}(React.Component));
export default Main;
//# sourceMappingURL=main.jsx.map