/*
 * (c) Copyright 2015 Hewlett-Packard Development Company, L.P.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

(function () {
  'use strict';

  /**
   * @ngdoc overview
   * @name horizon.framework.util.promise-toggle
   * @description
   *
   * This supports declarative directives that compile in their
   * content only after the related promises resolve.  This is typically
   * intended to be used for very fast checks (often cached) of whether or
   * not a particular setting or required service is enabled.
   */
  angular
    .module('horizon.framework.util.promise-toggle', []);

})();
