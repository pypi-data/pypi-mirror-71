import { __assign } from "tslib";
import React from 'react';
import { mountWithTheme } from 'sentry-test/enzyme';
import { IconUser, IconLocation, IconSpan, IconSwitch, IconFix, IconFire } from 'app/icons';
import Filter from 'app/components/events/interfaces/breadcrumbsV2/filter/filter';
import Level from 'app/components/events/interfaces/breadcrumbsV2/level';
import Icon from 'app/components/events/interfaces/breadcrumbsV2/icon';
import { BreadcrumbType, BreadcrumbLevelType, } from 'app/components/events/interfaces/breadcrumbsV2/types';
var options = [
    [
        {
            type: BreadcrumbType.HTTP,
            description: 'HTTP request',
            levels: [BreadcrumbLevelType.INFO],
            symbol: <Icon color="green400" icon={IconSwitch} size="xs"/>,
            isChecked: true,
            isDisabled: false,
        },
        {
            type: BreadcrumbType.TRANSACTION,
            description: 'Transaction',
            levels: [BreadcrumbLevelType.ERROR],
            symbol: <Icon color="pink400" icon={IconSpan} size="xs"/>,
            isChecked: true,
            isDisabled: false,
        },
        {
            type: BreadcrumbType.UI,
            description: 'User Action',
            levels: [BreadcrumbLevelType.INFO],
            symbol: <Icon color="purple400" icon={IconUser} size="xs"/>,
            isChecked: true,
            isDisabled: false,
        },
        {
            type: BreadcrumbType.NAVIGATION,
            description: 'Navigation',
            levels: [BreadcrumbLevelType.INFO],
            symbol: <Icon color="green500" icon={IconLocation} size="xs"/>,
            isChecked: true,
            isDisabled: false,
        },
        {
            type: BreadcrumbType.DEBUG,
            description: 'Debug',
            levels: [BreadcrumbLevelType.INFO],
            symbol: <Icon color="purple500" icon={IconFix} size="xs"/>,
            isChecked: true,
            isDisabled: false,
        },
        {
            type: BreadcrumbType.ERROR,
            description: 'Error',
            levels: [BreadcrumbLevelType.ERROR],
            symbol: <Icon color="red400" icon={IconFire} size="xs"/>,
            isChecked: true,
            isDisabled: false,
        },
    ],
    [
        {
            type: BreadcrumbLevelType.INFO,
            symbol: <Level level={BreadcrumbLevelType.INFO}/>,
            isChecked: true,
            isDisabled: false,
        },
        {
            type: BreadcrumbLevelType.ERROR,
            symbol: <Level level={BreadcrumbLevelType.ERROR}/>,
            isChecked: true,
            isDisabled: false,
        },
    ],
];
describe('Filter', function () {
    var handleFilter;
    var handleCheckAll;
    beforeEach(function () {
        handleFilter = jest.fn();
        handleCheckAll = jest.fn();
    });
    it('default render', function () {
        var wrapper = mountWithTheme(<Filter options={options} onFilter={handleFilter} onCheckAll={handleCheckAll}/>);
        expect(wrapper.find('OptionsGroup')).toHaveLength(2);
        expect(wrapper
            .find('OptionsGroup')
            .at(0)
            .find('Header')
            .text()).toBe('Type');
        expect(wrapper
            .find('OptionsGroup')
            .at(0)
            .find('ListItem')).toHaveLength(6);
        expect(wrapper
            .find('OptionsGroup')
            .at(1)
            .find('Header')
            .text()).toBe('Level');
        expect(wrapper
            .find('OptionsGroup')
            .at(1)
            .find('ListItem')).toHaveLength(2);
        expect(wrapper).toMatchSnapshot();
    });
    it('Without Options', function () {
        var wrapper = mountWithTheme(<Filter options={[[], []]} onFilter={handleFilter} onCheckAll={handleCheckAll}/>);
        expect(wrapper.find('Header')).toHaveLength(0);
        expect(wrapper.find('OptionsGroup')).toHaveLength(0);
    });
    it('With Option Type only', function () {
        var wrapper = mountWithTheme(<Filter options={[options[0], []]} onFilter={handleFilter} onCheckAll={handleCheckAll}/>);
        var optionsGroup = wrapper.find('OptionsGroup');
        expect(optionsGroup).toHaveLength(1);
        expect(optionsGroup.find('Header').text()).toBe('Type');
        expect(optionsGroup.find('ListItem')).toHaveLength(6);
        var firstOptionLevel = wrapper
            .find('OptionsGroup')
            .at(0)
            .find('ListItem')
            .at(0);
        expect(firstOptionLevel.text()).toBe(options[0][0].description);
        expect(firstOptionLevel
            .find('[role="checkbox"]')
            .find('CheckboxFancyContent')
            .props().isChecked).toBeTruthy();
        firstOptionLevel.simulate('click');
        expect(handleFilter).toHaveBeenCalledTimes(1);
    });
    it('With Option Level only', function () {
        var wrapper = mountWithTheme(<Filter options={[[], options[1]]} onFilter={handleFilter} onCheckAll={handleCheckAll}/>);
        var optionsGroup = wrapper.find('OptionsGroup');
        expect(optionsGroup).toHaveLength(1);
        expect(optionsGroup.find('Header').text()).toBe('Level');
        expect(optionsGroup.find('ListItem')).toHaveLength(2);
        var firstOptionLevel = wrapper
            .find('OptionsGroup')
            .at(0)
            .find('ListItem')
            .at(0);
        expect(firstOptionLevel.text()).toBe(options[1][0].type.toLocaleLowerCase());
        expect(firstOptionLevel
            .find('[role="checkbox"]')
            .find('CheckboxFancyContent')
            .props().isChecked).toBeTruthy();
        firstOptionLevel.simulate('click');
        expect(handleFilter).toHaveBeenCalledTimes(1);
    });
    it('Uncheck All', function () {
        var wrapper = mountWithTheme(<Filter options={options} onFilter={handleFilter} onCheckAll={handleCheckAll}/>);
        var filterHeader = wrapper.find('Header').first();
        expect(filterHeader).toHaveLength(1);
        expect(filterHeader.text()).toBe(options[0].length + options[1].length + " checked");
        var checkAllButton = filterHeader.find('[role="checkbox"]');
        expect(checkAllButton).toHaveLength(1);
        checkAllButton.simulate('click');
        expect(wrapper.state().checkAll).toBeFalsy();
        expect(handleCheckAll).toHaveBeenCalled();
    });
    it('Check All', function () {
        var wrapper = mountWithTheme(<Filter options={options.map(function (option) {
            return option.map(function (optionItem) { return (__assign(__assign({}, optionItem), { isChecked: false })); });
        })} onFilter={handleFilter} onCheckAll={handleCheckAll}/>);
        expect(wrapper.state().checkedQuantity).toBe(0);
        var filterHeader = wrapper.find('Header').first();
        expect(filterHeader).toHaveLength(1);
        expect(filterHeader.text()).toBe('Check All');
        var checkAllButton = filterHeader.find('[role="checkbox"]');
        expect(checkAllButton).toHaveLength(1);
        checkAllButton.simulate('click');
        expect(handleCheckAll).toHaveBeenCalled();
    });
    it('Disable Options', function () {
        var wrapper = mountWithTheme(<Filter options={options.map(function (option) {
            return option.map(function (optionItem) { return (__assign(__assign({}, optionItem), { isDisabled: true })); });
        })} onFilter={handleFilter} onCheckAll={handleCheckAll}/>);
        var firstOptionType = wrapper
            .find('OptionsGroup')
            .at(0)
            .find('ListItem')
            .at(0);
        expect(firstOptionType.text()).toBe(options[0][0].description);
        firstOptionType.simulate('click');
        expect(handleFilter).toHaveBeenCalledTimes(0);
    });
});
//# sourceMappingURL=filter.spec.jsx.map