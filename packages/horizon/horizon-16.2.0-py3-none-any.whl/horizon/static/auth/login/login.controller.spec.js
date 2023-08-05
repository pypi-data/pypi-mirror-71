/**
 * Copyright 2015 ThoughtWorks Inc.
 *
 * Licensed under the Apache License, Version 2.0 (the "License"); you may
 * not use this file except in compliance with the License. You may obtain
 * a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
 * WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
 * License for the specific language governing permissions and limitations
 * under the License.
 */

(function() {
  'use strict';

  describe('hzLoginController', function() {
    var $controller;
    beforeEach(module('horizon.auth.login'));
    beforeEach(inject(function(_$controller_) {
      $controller = _$controller_;
    }));

    describe('should set auth_type', function() {
      it('should initialize to credentials', function() {
        var controller = $controller('hzLoginController');
        expect(controller.auth_type).toEqual('credentials');
      });
    });
  });
})();
