/*
 * Copyright 2016 IBM Corp.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
(function() {
  'use strict';

  function digestMarkup(scope, compile, markup) {
    var element = angular.element(markup);
    compile(element)(scope);

    scope.$apply();
    return element;
  }

  describe('hzDynamicTable directive', function () {
    var $scope, $compile, $qExtensions, markup;

    beforeEach(module('templates'));
    beforeEach(module('smart-table'));
    beforeEach(module('horizon.framework'));

    beforeEach(function() {
      horizon.cookies = {
        get: function() {
          return;
        }
      };

      spyOn(horizon.cookies, 'get').and.callThrough();

    });

    beforeEach(inject(function ($injector) {
      $compile = $injector.get('$compile');
      $scope = $injector.get('$rootScope').$new();
      $qExtensions = $injector.get('horizon.framework.util.q.extensions');

      $scope.config = {
        selectAll: true,
        expand: true,
        trackId: 'id',
        columns: [
          {id: 'animal', title: 'Animal', priority: 1},
          {id: 'type', title: 'Type', priority: 2},
          {id: 'diet', title: 'Diet', priority: 1, sortDefault: true}
        ],
        needsFilterFirst: false
      };

      $scope.safeTableData = [
        { id: '1', animal: 'cat', type: 'mammal', diet: 'fish', domestic: true },
        { id: '2', animal: 'snake', type: 'reptile', diet: 'mice', domestic: false },
        { id: '3', animal: 'sparrow', type: 'bird', diet: 'worms', domestic: false }
      ];

      markup =
        '<hz-dynamic-table config="config" items="safeTableData">' +
        '</hz-dynamic-table>';
    }));

    it('has the correct number of column headers', function() {
      var $element = digestMarkup($scope, $compile, markup);
      expect($element).toBeDefined();
      expect($element.find('thead tr:nth-child(2) th').length).toBe(5);
    });

    it('displays selectAll checkbox when config selectAll set to True', function() {
      var $element = digestMarkup($scope, $compile, markup);
      expect($element.find('thead tr:nth-child(2) th:first input').attr(
        'hz-select-all')).toBe('items');
    });

    it('does not display selectAll checkbox when config selectAll set to False', function() {
      $scope.config = {
        selectAll: false,
        expand: true,
        trackId: 'id',
        columns: [
          {id: 'animal', title: 'Animal', priority: 1},
          {id: 'type', title: 'Type', priority: 2},
          {id: 'diet', title: 'Diet', priority: 1, sortDefault: true}
        ],
        needsFilterFirst: false
      };
      var $element = digestMarkup($scope, $compile, markup);
      expect($element.find('thead tr:nth-child(2) th:first').hasClass('ng-hide')).toBe(true);
    });

    it('displays expander when config expand set to True', function() {
      var $element = digestMarkup($scope, $compile, markup);
      expect($element.find('thead tr:nth-child(2) th:eq(1)').hasClass('expander')).toBe(true);
    });

    it('does not display expander when config expand set to False', function() {
      $scope.config = {
        selectAll: true,
        expand: false,
        trackId: 'id',
        columns: [
          {id: 'animal', title: 'Animal', priority: 1},
          {id: 'type', title: 'Type', priority: 2},
          {id: 'diet', title: 'Diet', priority: 1, sortDefault: true}
        ],
        needsFilterFirst: false
      };
      var $element = digestMarkup($scope, $compile, markup);
      expect($element.find('thead tr:nth-child(2) th:eq(1)').hasClass('ng-hide')).toBe(true);
    });

    it('has the correct responsive priority classes', function() {
      var $element = digestMarkup($scope, $compile, markup);
      expect($element.find('tbody tr').length).toBe(8);
      expect($element.find('tbody tr:eq(0) td').length).toBe(5);
      expect($element.find('tbody tr:eq(2) td:eq(2)').hasClass('rsp-p1')).toBe(true);
      expect($element.find('tbody tr:eq(2) td:eq(3)').hasClass('rsp-p2')).toBe(true);
      expect($element.find('tbody tr:eq(2) td:eq(4)').hasClass('rsp-p1')).toBe(true);
    });

    it('has the correct number of rows (including detail rows and no items row)', function() {
      var $element = digestMarkup($scope, $compile, markup);
      expect($element.find('tbody tr').length).toBe(8);
      expect($element.find('tbody tr:eq(0) td').length).toBe(5);
      expect($element.find('tbody tr:eq(2) td:eq(2)').text()).toContain('snake');
      expect($element.find('tbody tr:eq(2) td:eq(3)').text()).toContain('reptile');
      expect($element.find('tbody tr:eq(2) td:eq(4)').text()).toContain('mice');
    });

    it('displays the default no items message if noItemsMessage is not set', function() {
      $scope.safeTableData = [];
      var $element = digestMarkup($scope, $compile, markup);
      expect($element.find('tbody td.no-rows-help').text()).toBe('No items to display.');
    });

    it('displays a custom no items message if noItemsMessage is provided', function() {
      $scope.safeTableData = [];
      $scope.config.noItemsMessage = 'A sample message';
      var $element = digestMarkup($scope, $compile, markup);
      expect($element.find('tbody td.no-rows-help').text()).toBe('A sample message');
    });

    it('has no search or action buttons if none configured', function() {
      var $element = digestMarkup($scope, $compile, markup);
      expect($element.find('.hz-dynamic-table-preamble').length).toBe(1);
      expect($element.find('.hz-dynamic-table-preamble').text().trim()).toBe('');
    });

    it('displays the default  needsFilterFirstMessage', function() {
      $scope.safeTableData = [];
      $scope.config.needsFilterFirst = true;
      var $element = digestMarkup($scope, $compile, markup);
      expect($element.find('tbody td.no-rows-help').text())
        .toBe('Please provide a search criteria first.');
    });

    describe('search & action button preamble', function () {
      beforeEach(function () {
        $scope.filterFacets = [{label: 'Name', name: 'name'}];
        $scope.batchActions = [
          {
            id: 'action',
            service: {
              allowed: function () {
                return $qExtensions.booleanAsPromise(false);
              }
            },
            template: {type: 'create'}
          }
        ];
        markup =
          '<hz-dynamic-table config="config" items="safeTableData" ' +
          'filter-facets="filterFacets" batch-actions="batchActions">' +
          '</hz-dynamic-table>';
      });
    });

    describe('hzDetailRow directive', function() {

      it('compiles default detail row template', function() {
        var $element = digestMarkup($scope, $compile, markup);
        expect($element.find('tbody tr:eq(3) dt').text()).toContain('Animal');
        expect($element.find('tbody tr:eq(3) dd').text()).toContain('snake');
        expect($element.find('tbody tr:eq(3) dt').text()).toContain('Type');
        expect($element.find('tbody tr:eq(3) dd').text()).toContain('reptile');
        expect($element.find('tbody tr:eq(3) dt').text()).toContain('Diet');
        expect($element.find('tbody tr:eq(3) dd').text()).toContain('mice');
      });
    });

    describe('hzCell directive', function() {

      it('compiles template passed in from column configuration', function() {
        $scope.config = {
          selectAll: true,
          expand: false,
          trackId: 'id',
          columns: [
            {id: 'animal', title: 'Animal', classes: 'rsp-p1'},
            {id: 'type', title: 'Type', classes: 'rsp-p2',
              template: '<span class="fa fa-bolt">{$ item.type $}</span>'},
            {id: 'diet', title: 'Diet', classes: 'rsp-p1', sortDefault: true}
          ]
        };
        var $element = digestMarkup($scope, $compile, markup);
        expect($element.find('tbody tr:eq(2) td:eq(3) span').hasClass('fa fa-bolt')).toBe(true);
        expect($element.find('tbody tr:eq(2) td:eq(3) span').text()).toBe('bird');
      });

      it('properly filters the cell content given the filter name', function() {
        $scope.config = {
          selectAll: true,
          expand: false,
          trackId: 'id',
          columns: [
            {id: 'animal', title: 'Animal', priority: 1},
            {id: 'type', title: 'Type', priority: 2,
              template: '<span class="fa fa-bolt">{$ item.type $}</span>'},
            {id: 'diet', title: 'Diet', priority: 1, sortDefault: true},
            {id: 'domestic', title: 'Domestic', priority: 2, filters: ['yesno']}
          ]
        };
        var $element = digestMarkup($scope, $compile, markup);
        expect($element.find('tbody tr:eq(0) td:eq(5)').text()).toContain('Yes');
        expect($element.find('tbody tr:eq(1) td:eq(5)').text()).toContain('No');
        expect($element.find('tbody tr:eq(2) td:eq(5)').text()).toContain('No');
      });

      it('properly filters the cell content given a filter function', function() {
        function ishFunc(input) {
          return input.concat('-ish');
        }

        $scope.config = {
          selectAll: true,
          expand: false,
          trackId: 'id',
          columns: [
            {id: 'animal', title: 'Animal', priority: 1},
            {id: 'type', title: 'Type', priority: 2, filters: [ishFunc]},
            {id: 'diet', title: 'Diet', priority: 1, sortDefault: true},
            {id: 'domestic', title: 'Domestic', priority: 2}
          ]
        };
        var $element = digestMarkup($scope, $compile, markup);
        expect($element.find('tbody tr:eq(0) td:eq(3)').text()).toContain('mammal-ish');
        expect($element.find('tbody tr:eq(1) td:eq(3)').text()).toContain('reptile-ish');
        expect($element.find('tbody tr:eq(2) td:eq(3)').text()).toContain('bird-ish');
      });

      it('properly maps the cell content given a mapping', function() {

        $scope.config = {
          selectAll: true,
          expand: false,
          trackId: 'id',
          columns: [
            {id: 'animal', title: 'Animal', priority: 1,
              values: {
                cat: "Catamount",
                snake: "Serpent",
                sparrow: "CAPTAIN Jack Sparrow"
              }
            },
            {id: 'type', title: 'Type', priority: 2},
            {id: 'diet', title: 'Diet', priority: 1, sortDefault: true},
            {id: 'domestic', title: 'Domestic', priority: 2}
          ]
        };
        var $element = digestMarkup($scope, $compile, markup);
        expect($element.find('tbody tr:eq(0) td:eq(2)').text()).toContain('Catamount');
        expect($element.find('tbody tr:eq(1) td:eq(2)').text()).toContain('Serpent');
        expect($element.find('tbody tr:eq(2) td:eq(2)').text()).toContain('CAPTAIN Jack Sparrow');
      });

      it('properly adds a link with urlFunction', function() {
        $scope.config = {
          selectAll: true,
          expand: false,
          trackId: 'id',
          columns: [
            {id: 'animal', title: 'Animal', priority: 1,
              urlFunction: myFunction
            },
            {id: 'type', title: 'Type', priority: 2},
            {id: 'diet', title: 'Diet', priority: 1, sortDefault: true},
            {id: 'domestic', title: 'Domestic', priority: 2}
          ]
        };
        var $element = digestMarkup($scope, $compile, markup);
        expect($element.find('tbody tr:eq(0) td:eq(2) a').attr('href')).toBe('/here/cat');
        expect($element.find('tbody tr:eq(1) td:eq(2) a').attr('href')).toBe('/here/snake');
        expect($element.find('tbody tr:eq(2) td:eq(2) a').attr('href')).toBe('/here/sparrow');
        function myFunction(item) {
          return '/here/' + item.animal;
        }
      });
    });

  });
}());

