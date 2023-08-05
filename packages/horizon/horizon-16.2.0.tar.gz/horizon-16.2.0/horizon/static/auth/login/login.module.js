/**
 * Copyright 2015 IBM Corp.
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
(function () {
  'use strict';

  angular
    .module('horizon.auth.login', [], config);

  config.$inject = [
    '$provide',
    '$windowProvider'
  ];

  /**
   * @description
   *
   * In the config function:
   * - define constant `horizon.auth.login.basePath` as the
   *   base path for auth login code.
   */
  function config($provide, $windowProvider) {
    var path = $windowProvider.$get().STATIC_URL + 'auth/login/';
    $provide.constant('horizon.auth.login.basePath', path);
  }

})();
