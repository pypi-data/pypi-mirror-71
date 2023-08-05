import { __makeTemplateObject } from "tslib";
import PropTypes from 'prop-types';
import React from 'react';
import styled from '@emotion/styled';
import space from 'app/styles/space';
import SettingsBreadcrumb from './settingsBreadcrumb';
import SettingsHeader from './settingsHeader';
import SettingsSearch from './settingsSearch';
function SettingsLayout(props) {
    var params = props.params, routes = props.routes, route = props.route, router = props.router, renderNavigation = props.renderNavigation, children = props.children;
    // We want child's view's props
    var childProps = children && React.isValidElement(children) ? children.props : props;
    var childRoutes = childProps.routes || routes || [];
    var childRoute = childProps.route || route || {};
    return (<React.Fragment>
      <SettingsColumn>
        <SettingsHeader>
          <HeaderContent>
            <StyledSettingsBreadcrumb params={params} routes={childRoutes} route={childRoute}/>
            <SettingsSearch routes={routes} router={router} params={params}/>
          </HeaderContent>
        </SettingsHeader>

        <MaxWidthContainer>
          {typeof renderNavigation === 'function' && (<SidebarWrapper>{renderNavigation()}</SidebarWrapper>)}
          <Content>{children}</Content>
        </MaxWidthContainer>
      </SettingsColumn>
    </React.Fragment>);
}
SettingsLayout.propTypes = {
    renderNavigation: PropTypes.func,
    route: PropTypes.object,
    router: PropTypes.object,
    routes: PropTypes.array,
};
var MaxWidthContainer = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  max-width: ", ";\n  min-width: 600px; /* for small screen sizes, we need a min width to make it semi digestible */\n  flex: 1;\n"], ["\n  display: flex;\n  max-width: ", ";\n  min-width: 600px; /* for small screen sizes, we need a min width to make it semi digestible */\n  flex: 1;\n"])), function (p) { return p.theme.settings.containerWidth; });
var SidebarWrapper = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  flex-shrink: 0;\n  width: ", ";\n  background: ", ";\n  border-right: 1px solid ", ";\n  padding: ", ";\n  padding-right: ", ";\n"], ["\n  flex-shrink: 0;\n  width: ", ";\n  background: ", ";\n  border-right: 1px solid ", ";\n  padding: ", ";\n  padding-right: ", ";\n"])), function (p) { return p.theme.settings.sidebarWidth; }, function (p) { return p.theme.white; }, function (p) { return p.theme.borderLight; }, space(4), space(2));
var HeaderContent = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n"], ["\n  display: flex;\n  align-items: center;\n"])));
var StyledSettingsBreadcrumb = styled(SettingsBreadcrumb)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  flex: 1;\n"], ["\n  flex: 1;\n"])));
var SettingsColumn = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  display: flex;\n  flex-direction: column;\n  flex: 1; /* so this stretches vertically so that footer is fixed at bottom */\n  min-width: 0; /* fixes problem when child content stretches beyond layout width */\n  footer {\n    margin-top: 0;\n  }\n"], ["\n  display: flex;\n  flex-direction: column;\n  flex: 1; /* so this stretches vertically so that footer is fixed at bottom */\n  min-width: 0; /* fixes problem when child content stretches beyond layout width */\n  footer {\n    margin-top: 0;\n  }\n"])));
/**
 * Note: `overflow: hidden` will cause some buttons in `SettingsPageHeader` to be cut off because it has negative margin.
 * Will also cut off tooltips.
 */
var Content = styled('div')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  flex: 1;\n  padding: ", ";\n  min-width: 0; /* keep children from stretching container */\n"], ["\n  flex: 1;\n  padding: ", ";\n  min-width: 0; /* keep children from stretching container */\n"])), space(4));
export default SettingsLayout;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6;
//# sourceMappingURL=settingsLayout.jsx.map