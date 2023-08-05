import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { t } from 'app/locale';
import ConfigStore from 'app/stores/configStore';
import ExternalLink from 'app/components/links/externalLink';
import Hook from 'app/components/hook';
import getDynamicText from 'app/utils/getDynamicText';
import space from 'app/styles/space';
var Footer = function () {
    var config = ConfigStore.getConfig();
    return (<footer>
      <div className="container">
        <div className="pull-right">
          <FooterLink className="hidden-xs" href="/api/">
            {t('API')}
          </FooterLink>
          <FooterLink href="/docs/">{t('Docs')}</FooterLink>
          <FooterLink className="hidden-xs" href="https://github.com/getsentry/sentry">
            {t('Contribute')}
          </FooterLink>
          {config.isOnPremise && (<FooterLink className="hidden-xs" href="/out/">
              {t('Migrate to SaaS')}
            </FooterLink>)}
        </div>
        {config.isOnPremise && (<div className="version pull-left">
            {'Sentry '}
            {getDynamicText({
        fixed: 'Acceptance Test',
        value: config.version.current,
    })}
            <Build>
              {getDynamicText({
        fixed: 'test',
        value: config.version.build.substring(0, 7),
    })}
            </Build>
          </div>)}
        <a href="/" tabIndex={-1} className="icon-sentry-logo"/>
        <Hook name="footer"/>
      </div>
    </footer>);
};
var FooterLink = styled(ExternalLink)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  &.focus-visible {\n    outline: none;\n    box-shadow: ", " 0 2px 0;\n  }\n"], ["\n  &.focus-visible {\n    outline: none;\n    box-shadow: ", " 0 2px 0;\n  }\n"])), function (p) { return p.theme.blue400; });
var Build = styled('span')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  font-size: ", ";\n  color: ", ";\n  font-weight: bold;\n  margin-left: ", ";\n"], ["\n  font-size: ", ";\n  color: ", ";\n  font-weight: bold;\n  margin-left: ", ";\n"])), function (p) { return p.theme.fontSizeRelativeSmall; }, function (p) { return p.theme.gray400; }, space(1));
export default Footer;
var templateObject_1, templateObject_2;
//# sourceMappingURL=footer.jsx.map