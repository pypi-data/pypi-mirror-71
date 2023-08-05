import { __awaiter, __extends, __generator, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { t } from 'app/locale';
import Button from 'app/components/button';
import InlineSvg from 'app/components/inlineSvg';
import { loadIncidents } from 'app/actionCreators/serviceIncidents';
import space from 'app/styles/space';
import SidebarPanelEmpty from './sidebarPanelEmpty';
import SidebarItem from './sidebarItem';
import SidebarPanel from './sidebarPanel';
var ServiceIncidents = /** @class */ (function (_super) {
    __extends(ServiceIncidents, _super);
    function ServiceIncidents() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            status: null,
        };
        return _this;
    }
    ServiceIncidents.prototype.componentDidMount = function () {
        this.fetchData();
    };
    ServiceIncidents.prototype.fetchData = function () {
        return __awaiter(this, void 0, void 0, function () {
            var _a, _b;
            return __generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        _a = this.setState;
                        _b = {};
                        return [4 /*yield*/, loadIncidents()];
                    case 1:
                        _a.apply(this, [(_b.status = _c.sent(), _b)]);
                        return [2 /*return*/];
                }
            });
        });
    };
    ServiceIncidents.prototype.render = function () {
        var _a = this.props, currentPanel = _a.currentPanel, showPanel = _a.showPanel, onShowPanel = _a.onShowPanel, hidePanel = _a.hidePanel, collapsed = _a.collapsed, orientation = _a.orientation;
        var status = this.state.status;
        if (!status) {
            return null;
        }
        var active = currentPanel === 'statusupdate';
        var isEmpty = !status.incidents || status.incidents.length === 0;
        if (isEmpty) {
            return null;
        }
        return (<React.Fragment>
        <SidebarItem id="statusupdate" orientation={orientation} collapsed={collapsed} active={active} icon={<InlineSvg src="icon-circle-exclamation" className="animated pulse infinite"/>} label={t('Service status')} onClick={onShowPanel}/>
        {showPanel && active && status && (<SidebarPanel orientation={orientation} title={t('Recent status updates')} hidePanel={hidePanel} collapsed={collapsed}>
            {isEmpty && (<SidebarPanelEmpty>
                {t('There are no incidents to report')}
              </SidebarPanelEmpty>)}
            <IncidentList className="incident-list">
              {status.incidents.map(function (incident) { return (<IncidentItem key={incident.id}>
                  <IncidentTitle>{incident.name}</IncidentTitle>
                  {incident.updates ? (<div>
                      <StatusHeader>{t('Latest updates:')}</StatusHeader>
                      <StatusList>
                        {incident.updates.map(function (update, key) { return (<StatusItem key={key}>{update}</StatusItem>); })}
                      </StatusList>
                    </div>) : null}
                  <div>
                    <Button href={incident.url} size="small" external>
                      {t('Learn more')}
                    </Button>
                  </div>
                </IncidentItem>); })}
            </IncidentList>
          </SidebarPanel>)}
      </React.Fragment>);
    };
    return ServiceIncidents;
}(React.Component));
export default ServiceIncidents;
var IncidentList = styled('ul')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  font-size: 13px;\n  list-style: none;\n  padding: ", " ", " 0;\n"], ["\n  font-size: 13px;\n  list-style: none;\n  padding: ", " ", " 0;\n"])), space(3), space(3));
var IncidentItem = styled('li')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  border-bottom: 1px solid ", ";\n  margin-bottom: ", ";\n  padding-bottom: ", ";\n"], ["\n  border-bottom: 1px solid ", ";\n  margin-bottom: ", ";\n  padding-bottom: ", ";\n"])), function (p) { return p.theme.borderLight; }, space(3), space(0.75));
var IncidentTitle = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  font-size: ", ";\n  font-weight: 600;\n  line-height: 1.2;\n  margin-bottom: ", ";\n"], ["\n  font-size: ", ";\n  font-weight: 600;\n  line-height: 1.2;\n  margin-bottom: ", ";\n"])), function (p) { return p.theme.fontSizeExtraLarge; }, space(2));
var StatusHeader = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  color: #7c6a8e;\n  margin-bottom: ", ";\n  font-size: ", ";\n  font-weight: 600;\n  line-height: 1;\n"], ["\n  color: #7c6a8e;\n  margin-bottom: ", ";\n  font-size: ", ";\n  font-weight: 600;\n  line-height: 1;\n"])), space(2), function (p) { return p.theme.fontSizeMedium; });
var StatusList = styled('ul')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  list-style: none;\n  padding: 0;\n"], ["\n  list-style: none;\n  padding: 0;\n"])));
var StatusItem = styled('li')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  margin-bottom: ", ";\n  line-height: 1.5;\n"], ["\n  margin-bottom: ", ";\n  line-height: 1.5;\n"])), space(2));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6;
//# sourceMappingURL=serviceIncidents.jsx.map