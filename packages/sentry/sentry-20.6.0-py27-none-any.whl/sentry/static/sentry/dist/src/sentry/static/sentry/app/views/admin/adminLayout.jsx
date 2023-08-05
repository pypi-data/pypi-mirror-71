import { __makeTemplateObject } from "tslib";
import DocumentTitle from 'react-document-title';
import React from 'react';
import styled from '@emotion/styled';
import space from 'app/styles/space';
import ListLink from 'app/components/links/listLink';
var AdminLayout = function (_a) {
    var children = _a.children;
    return (<DocumentTitle title="Sentry Admin">
    <Page>
      <div>
        <h6 className="nav-header">System</h6>
        <ul className="nav nav-stacked">
          <ListLink index to="/manage/">
            Overview
          </ListLink>
          <ListLink index to="/manage/buffer/">
            Buffer
          </ListLink>
          <ListLink index to="/manage/queue/">
            Queue
          </ListLink>
          <ListLink index to="/manage/quotas/">
            Quotas
          </ListLink>
          <ListLink index to="/manage/status/environment/">
            Environment
          </ListLink>
          <ListLink index to="/manage/status/packages/">
            Packages
          </ListLink>
          <ListLink index to="/manage/status/mail/">
            Mail
          </ListLink>
          <ListLink index to="/manage/status/warnings/">
            Warnings
          </ListLink>
          <ListLink index to="/manage/settings/">
            Settings
          </ListLink>
        </ul>
        <h6 className="nav-header">Manage</h6>
        <ul className="nav nav-stacked">
          <ListLink to="/manage/organizations/">Organizations</ListLink>
          <ListLink to="/manage/projects/">Projects</ListLink>
          <ListLink to="/manage/users/">Users</ListLink>
        </ul>
      </div>
      <div>{children}</div>
    </Page>
  </DocumentTitle>);
};
var Page = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 200px 1fr;\n  margin: ", ";\n  flex-grow: 1;\n"], ["\n  display: grid;\n  grid-template-columns: 200px 1fr;\n  margin: ", ";\n  flex-grow: 1;\n"])), space(4));
export default AdminLayout;
var templateObject_1;
//# sourceMappingURL=adminLayout.jsx.map