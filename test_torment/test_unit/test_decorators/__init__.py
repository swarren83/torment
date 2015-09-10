# Copyright 2015 Alex Brandt
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import typing  # noqa (use mypy typing)

from torment import contexts
from torment import fixtures
from torment import helpers

from torment import decorators


class LogDecoratorFixture(fixtures.Fixture):
    def initialize(self):
        if not hasattr(self, 'parameters'):
            self.parameters = {}

    @property
    def description(self) -> str:
        _description = super().description + '.log'

        if self.parameters.get('prefix') is not None:
            _description += '({0.parameters[prefix]})'

        _description += '({0.function.__name__})'

        return _description.format(self, self.context.module)

    def run(self) -> None:
        with self.context.assertLogs(decorators.logger) as mocked_logger:
            try:
                decorators.log(self.parameters.get('prefix', ''))(self.function)()
            except RuntimeError:
                pass

        self.mocked_logger = mocked_logger

    def check(self) -> None:
        self.context.assertEqual(self.mocked_logger.output, self.expected)


class MockDecoratorFixture(fixtures.Fixture):
    @property
    def description(self) -> str:
        return super().description + '.mock({0.mock.name})'

    def run(self) -> None:
        pass  # TODO mock symbol

    def check(self) -> None:
        pass  # TODO mock symbol

helpers.import_directory(__name__, os.path.dirname(__file__))


class DecoratorUnitTest(contexts.TestContext, metaclass = contexts.MetaContext):
    fixture_classes = (
        LogDecoratorFixture,
        MockDecoratorFixture,
    )
