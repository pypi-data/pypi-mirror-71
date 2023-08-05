import { __assign, __extends, __makeTemplateObject } from "tslib";
import { browserHistory } from 'react-router';
import PropTypes from 'prop-types';
import React from 'react';
import styled from '@emotion/styled';
import { t } from 'app/locale';
import Button from 'app/components/button';
import ButtonBar from 'app/components/buttonBar';
import parseLinkHeader from 'app/utils/parseLinkHeader';
import { callIfFunction } from 'app/utils/callIfFunction';
var defaultProps = {
    onCursor: function (cursor, path, query, _direction) {
        browserHistory.push({
            pathname: path,
            query: __assign(__assign({}, query), { cursor: cursor }),
        });
    },
};
var Pagination = /** @class */ (function (_super) {
    __extends(Pagination, _super);
    function Pagination() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    Pagination.prototype.render = function () {
        var _a = this.props, className = _a.className, onCursor = _a.onCursor, pageLinks = _a.pageLinks;
        if (!pageLinks) {
            return null;
        }
        var location = this.context.location;
        var path = this.props.to || location.pathname;
        var query = location.query;
        var links = parseLinkHeader(pageLinks);
        var previousDisabled = links.previous.results === false;
        var nextDisabled = links.next.results === false;
        return (<div className={className}>
        <ButtonBar merged>
          <Button aria-label={t('Previous')} disabled={previousDisabled} onClick={function () {
            callIfFunction(onCursor, links.previous.cursor, path, query, -1);
        }}>
            <IconSpan className="icon-arrow-left" disabled={previousDisabled}/>
          </Button>
          <Button aria-label={t('Next')} disabled={nextDisabled} onClick={function () {
            callIfFunction(onCursor, links.next.cursor, path, query, 1);
        }}>
            <IconSpan className="icon-arrow-right" disabled={nextDisabled}/>
          </Button>
        </ButtonBar>
      </div>);
    };
    Pagination.propTypes = {
        pageLinks: PropTypes.string,
        to: PropTypes.string,
        onCursor: PropTypes.func,
        className: PropTypes.string,
    };
    Pagination.contextTypes = {
        location: PropTypes.object,
    };
    Pagination.defaultProps = defaultProps;
    return Pagination;
}(React.Component));
export default styled(Pagination)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: flex-end;\n  margin: 20px 0 0 0;\n\n  .icon-arrow-right,\n  .icon-arrow-left {\n    font-size: 20px !important;\n  }\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: flex-end;\n  margin: 20px 0 0 0;\n\n  .icon-arrow-right,\n  .icon-arrow-left {\n    font-size: 20px !important;\n  }\n"])));
// TODO this component and the icons should be replaced with IconChevron but
// that icon has rendering issues on percy.
var IconSpan = styled('span')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (p) { return (p.disabled ? p.theme.disabled : p.theme.gray700); });
var templateObject_1, templateObject_2;
//# sourceMappingURL=pagination.jsx.map