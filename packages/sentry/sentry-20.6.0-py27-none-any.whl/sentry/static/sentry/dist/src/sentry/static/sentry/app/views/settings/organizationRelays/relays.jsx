import { __assign, __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { Panel, PanelBody, PanelHeader, PanelAlert } from 'app/components/panels';
import { t, tct } from 'app/locale';
import AsyncComponent from 'app/components/asyncComponent';
import SettingsPageHeader from 'app/views/settings/components/settingsPageHeader';
import ExternalLink from 'app/components/links/externalLink';
import space from 'app/styles/space';
import Button from 'app/components/button';
import { IconDelete } from 'app/icons';
import Time from './time';
var RELAY_DOCS_LINK = 'https://getsentry.github.io/relay/';
var relaysMock = [
    {
        public_key: '1:bb:6e:af:66:b4:38:e0:62:83:62:15:22:7',
        name: 'First key',
        description: 'optional description for the key',
        first_seen: '2020-02-07T15:17:00Z',
        last_seen: '2020-02-07T15:17:00Z',
        created: '2020-02-07T15:17:00Z',
    },
    {
        public_key: '2:bb:6e:af:66:b4:38:e0:62:83:62:15:22:7',
        name: 'Second key',
        description: 'optional description for the key',
        first_seen: '2020-02-07T15:17:00Z',
        last_seen: '2020-02-07T15:17:00Z',
        last_modified: '2020-02-07T15:17:00Z',
        created: '2020-02-07T15:17:00Z',
    },
];
var Relays = /** @class */ (function (_super) {
    __extends(Relays, _super);
    function Relays() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        // TODO(Priscila): activate the code below as soon as the endpoint is provided
        // getEndpoints(): ReturnType<AsyncComponent['getEndpoints']> {
        //   return [['relays', `/organizations/${this.props.organization.slug}/relay-keys`]];
        // }
        // handleDelete = (id: Relay['public_key']) => () => {};
        _this.handleAdd = function () { };
        return _this;
    }
    Relays.prototype.getDefaultState = function () {
        return __assign(__assign({}, _super.prototype.getDefaultState.call(this)), { relays: relaysMock });
    };
    Relays.prototype.renderBody = function () {
        var relays = this.state.relays;
        return (<React.Fragment>
        <SettingsPageHeader title={t('Relays')}/>
        <Panel>
          <PanelHeader>{t('Relays')}</PanelHeader>
          <PanelAlert type="info">
            {tct('For more details, see [linkToDocs].', {
            linkToDocs: (<ExternalLink href={RELAY_DOCS_LINK}>
                  {t('full Relay documentation')}
                </ExternalLink>),
        })}
          </PanelAlert>
          <PanelBody>
            {relays.map(function (_a) {
            var public_key = _a.public_key, name = _a.name, created = _a.created, last_seen = _a.last_seen, first_seen = _a.first_seen, last_modified = _a.last_modified;
            return (<Content key={public_key}>
                  <Info>
                    <InfoItem>
                      <Name>{name}</Name>
                    </InfoItem>
                    <InfoItem>
                      <PublicKey>{public_key}</PublicKey>
                    </InfoItem>
                    <InfoItem>
                      <Time label={t('Created:')} date={created}/>
                    </InfoItem>
                    <InfoItem>
                      <Time label={t('First Seen:')} date={first_seen}/>
                    </InfoItem>
                    <InfoItem>
                      <Time label={t('Last Seen:')} date={last_seen}/>
                    </InfoItem>
                    <InfoItem>
                      <Time label={t('Last modified:')} date={last_modified}/>
                    </InfoItem>
                  </Info>
                  <Button title={t('Delete Rule')} label={t('Delete Rule')} size="small" icon={<IconDelete />}/>
                </Content>);
        })}
          </PanelBody>
          <PanelAction>
            <Button href={RELAY_DOCS_LINK} target="_blank">
              {t('Read the docs')}
            </Button>
            <Button onClick={this.handleAdd} priority="primary">
              {t('Add Relay')}
            </Button>
          </PanelAction>
        </Panel>
      </React.Fragment>);
    };
    return Relays;
}(AsyncComponent));
export default Relays;
var Content = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 1fr max-content;\n  align-items: center;\n  border-bottom: 1px solid ", ";\n  padding: ", " ", ";\n  :last-child {\n    border-bottom: 0;\n  }\n"], ["\n  display: grid;\n  grid-template-columns: 1fr max-content;\n  align-items: center;\n  border-bottom: 1px solid ", ";\n  padding: ", " ", ";\n  :last-child {\n    border-bottom: 0;\n  }\n"])), function (p) { return p.theme.borderDark; }, space(1), space(2));
var Info = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: repeat(4, 1fr);\n  grid-gap: ", ";\n  > *:nth-child(1),\n  > *:nth-child(2) {\n    grid-column: span 4;\n  }\n"], ["\n  display: grid;\n  grid-template-columns: repeat(4, 1fr);\n  grid-gap: ", ";\n  > *:nth-child(1),\n  > *:nth-child(2) {\n    grid-column: span 4;\n  }\n"])), space(1));
var InfoItem = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  height: 100%;\n"], ["\n  display: flex;\n  align-items: center;\n  height: 100%;\n"])));
var PanelAction = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  padding: ", " ", ";\n  display: grid;\n  grid-gap: ", ";\n  grid-template-columns: auto auto;\n  justify-content: flex-end;\n  border-top: 1px solid ", ";\n"], ["\n  padding: ", " ", ";\n  display: grid;\n  grid-gap: ", ";\n  grid-template-columns: auto auto;\n  justify-content: flex-end;\n  border-top: 1px solid ", ";\n"])), space(1), space(2), space(1), function (p) { return p.theme.borderDark; });
var Name = styled('h4')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  font-size: ", " !important;\n  font-weight: 600;\n  margin-bottom: 0 !important;\n  color: ", ";\n"], ["\n  font-size: ", " !important;\n  font-weight: 600;\n  margin-bottom: 0 !important;\n  color: ", ";\n"])), function (p) { return p.theme.fontSizeLarge; }, function (p) { return p.theme.gray600; });
var PublicKey = styled('h5')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  font-size: ", " !important;\n  font-weight: 400;\n  margin-bottom: 0 !important;\n"], ["\n  font-size: ", " !important;\n  font-weight: 400;\n  margin-bottom: 0 !important;\n"])), function (p) { return p.theme.fontSizeMedium; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6;
//# sourceMappingURL=relays.jsx.map