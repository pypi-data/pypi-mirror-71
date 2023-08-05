import PropTypes from 'prop-types';
import React from 'react';
import classNames from 'classnames';
import withProfiler from 'app/utils/withProfiler';
function LoadingIndicator(props) {
    var hideMessage = props.hideMessage, mini = props.mini, triangle = props.triangle, overlay = props.overlay, dark = props.dark, children = props.children, finished = props.finished, className = props.className, style = props.style, relative = props.relative, size = props.size, hideSpinner = props.hideSpinner;
    var cx = classNames(className, {
        overlay: overlay,
        dark: dark,
        loading: true,
        mini: mini,
        triangle: triangle,
    });
    var loadingCx = classNames({
        relative: relative,
        'loading-indicator': true,
        'load-complete': finished,
    });
    var loadingStyle = {};
    if (size) {
        loadingStyle = {
            width: size,
            height: size,
        };
    }
    return (<div className={cx} style={style}>
      {!hideSpinner && (<div className={loadingCx} style={loadingStyle}>
          {finished ? <div className="checkmark draw" style={style}/> : null}
        </div>)}

      {!hideMessage && <div className="loading-message">{children}</div>}
    </div>);
}
LoadingIndicator.propTypes = {
    overlay: PropTypes.bool,
    dark: PropTypes.bool,
    mini: PropTypes.bool,
    triangle: PropTypes.bool,
    finished: PropTypes.bool,
    relative: PropTypes.bool,
    hideMessage: PropTypes.bool,
    size: PropTypes.number,
    hideSpinner: PropTypes.bool,
};
export default withProfiler(LoadingIndicator);
//# sourceMappingURL=loadingIndicator.jsx.map