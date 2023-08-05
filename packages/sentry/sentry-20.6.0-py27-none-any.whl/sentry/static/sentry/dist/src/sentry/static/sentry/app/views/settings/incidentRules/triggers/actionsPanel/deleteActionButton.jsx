import React from 'react';
import { t } from 'app/locale';
import Button from 'app/components/button';
import { IconDelete } from 'app/icons';
export default function DeleteActionButton(props) {
    var handleClick = function (e) {
        var index = props.index, onClick = props.onClick;
        onClick(index, e);
    };
    return (<Button type="button" size="small" icon={<IconDelete size="xs"/>} aria-label={t('Remove action')} {...props} onClick={handleClick}/>);
}
//# sourceMappingURL=deleteActionButton.jsx.map