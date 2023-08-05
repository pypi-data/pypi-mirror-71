import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { t } from 'app/locale';
import space from 'app/styles/space';
import TimeSince from 'app/components/timeSince';
import Button from 'app/components/button';
import { IconClock, IconFile, IconDelete } from 'app/icons';
import ButtonBar from 'app/components/buttonBar';
import Version from 'app/components/version';
import Count from 'app/components/count';
import Confirm from 'app/components/confirm';
import Link from 'app/components/links/link';
var SourceMapsArchiveRow = function (_a) {
    var archive = _a.archive, orgId = _a.orgId, projectId = _a.projectId, onDelete = _a.onDelete;
    var id = archive.id, name = archive.name, date = archive.date, fileCount = archive.fileCount;
    var archiveLink = "/settings/" + orgId + "/projects/" + projectId + "/source-maps/" + encodeURIComponent(name);
    return (<React.Fragment>
      <Column>
        <Name>
          <Link to={archiveLink}>
            <Version version={name} anchor={false} truncate/>
          </Link>
        </Name>
        <TimeWrapper>
          <IconClock size="xs"/>
          <TimeSince date={date}/>
        </TimeWrapper>
      </Column>
      <Column>
        <Count value={fileCount}/>
      </Column>
      <RightColumn>
        <ButtonBar gap={0.5}>
          <Button size="xsmall" icon={<IconFile size="xs"/>} to={archiveLink}>
            {t('Open')}
          </Button>
          <Confirm onConfirm={function () { return onDelete(id); }} message={t('Are you sure you want to remove all artifacts in this archive?')}>
            <Button size="xsmall" icon={<IconDelete size="xs"/>} priority="danger"/>
          </Confirm>
        </ButtonBar>
      </RightColumn>
    </React.Fragment>);
};
var Column = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  flex-direction: column;\n  align-items: flex-start;\n  justify-content: center;\n  font-size: ", ";\n"], ["\n  display: flex;\n  flex-direction: column;\n  align-items: flex-start;\n  justify-content: center;\n  font-size: ", ";\n"])), function (p) { return p.theme.fontSizeMedium; });
var RightColumn = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  justify-content: flex-end;\n  align-items: center;\n"], ["\n  display: flex;\n  justify-content: flex-end;\n  align-items: center;\n"])));
var Name = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  max-width: 100%;\n"], ["\n  max-width: 100%;\n"])));
var TimeWrapper = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n  grid-template-columns: min-content 1fr;\n  margin-top: ", ";\n  font-size: ", ";\n  color: ", ";\n"], ["\n  display: grid;\n  grid-gap: ", ";\n  grid-template-columns: min-content 1fr;\n  margin-top: ", ";\n  font-size: ", ";\n  color: ", ";\n"])), space(0.5), space(1), function (p) { return p.theme.fontSizeSmall; }, function (p) { return p.theme.gray600; });
export default SourceMapsArchiveRow;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=sourceMapsArchiveRow.jsx.map