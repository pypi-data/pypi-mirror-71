import shutil
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Mapping

import pytest
from _pytest.capture import CaptureFixture
from _pytest.tmpdir import TempdirFactory
from freezegun import freeze_time
from prance import ValidationError

from datamodel_code_generator.__main__ import Exit, main

DATA_PATH: Path = Path(__file__).parent / 'data'
OPEN_API_DATA_PATH: Path = DATA_PATH / 'openapi'
JSON_SCHEMA_DATA_PATH: Path = DATA_PATH / 'jsonschema'
JSON_DATA_PATH: Path = DATA_PATH / 'json'
YAML_DATA_PATH: Path = DATA_PATH / 'yaml'


TIMESTAMP = '1985-10-26T01:21:00-07:00'


@freeze_time('2019-07-26')
def test_main():
    with TemporaryDirectory() as output_dir:
        output_file: Path = Path(output_dir) / 'output.py'
        return_code: Exit = main(
            [
                '--input',
                str(OPEN_API_DATA_PATH / 'api.yaml'),
                '--output',
                str(output_file),
            ]
        )
        assert return_code == Exit.OK
        assert (
            output_file.read_text()
            == '''# generated by datamodel-codegen:
#   filename:  api.yaml
#   timestamp: 2019-07-26T00:00:00+00:00

from __future__ import annotations

from typing import List, Optional

from pydantic import AnyUrl, BaseModel, Field


class Pet(BaseModel):
    id: int
    name: str
    tag: Optional[str] = None


class Pets(BaseModel):
    __root__: List[Pet]


class User(BaseModel):
    id: int
    name: str
    tag: Optional[str] = None


class Users(BaseModel):
    __root__: List[User]


class Id(BaseModel):
    __root__: str


class Rules(BaseModel):
    __root__: List[str]


class Error(BaseModel):
    code: int
    message: str


class Api(BaseModel):
    apiKey: Optional[str] = Field(
        None, description='To be used as a dataset parameter value'
    )
    apiVersionNumber: Optional[str] = Field(
        None, description='To be used as a version parameter value'
    )
    apiUrl: Optional[AnyUrl] = Field(
        None, description="The URL describing the dataset\'s fields"
    )
    apiDocumentationUrl: Optional[AnyUrl] = Field(
        None, description='A URL to the API console for each API'
    )


class Apis(BaseModel):
    __root__: List[Api]


class Event(BaseModel):
    name: Optional[str] = None


class Result(BaseModel):
    event: Optional[Event] = None
'''
        )

    with pytest.raises(SystemExit):
        main()


@freeze_time('2019-07-26')
def test_main_base_class():
    with TemporaryDirectory() as output_dir:
        output_file: Path = Path(output_dir) / 'output.py'
        return_code: Exit = main(
            [
                '--input',
                str(OPEN_API_DATA_PATH / 'api.yaml'),
                '--output',
                str(output_file),
                '--base-class',
                'custom_module.Base',
            ]
        )
        assert return_code == Exit.OK
        assert (
            output_file.read_text()
            == '''# generated by datamodel-codegen:
#   filename:  api.yaml
#   timestamp: 2019-07-26T00:00:00+00:00

from __future__ import annotations

from typing import List, Optional

from pydantic import AnyUrl, Field

from custom_module import Base


class Pet(Base):
    id: int
    name: str
    tag: Optional[str] = None


class Pets(Base):
    __root__: List[Pet]


class User(Base):
    id: int
    name: str
    tag: Optional[str] = None


class Users(Base):
    __root__: List[User]


class Id(Base):
    __root__: str


class Rules(Base):
    __root__: List[str]


class Error(Base):
    code: int
    message: str


class Api(Base):
    apiKey: Optional[str] = Field(
        None, description='To be used as a dataset parameter value'
    )
    apiVersionNumber: Optional[str] = Field(
        None, description='To be used as a version parameter value'
    )
    apiUrl: Optional[AnyUrl] = Field(
        None, description="The URL describing the dataset\'s fields"
    )
    apiDocumentationUrl: Optional[AnyUrl] = Field(
        None, description='A URL to the API console for each API'
    )


class Apis(Base):
    __root__: List[Api]


class Event(Base):
    name: Optional[str] = None


class Result(Base):
    event: Optional[Event] = None
'''
        )

    with pytest.raises(SystemExit):
        main()


@freeze_time('2019-07-26')
def test_target_python_version():
    with TemporaryDirectory() as output_dir:
        output_file: Path = Path(output_dir) / 'output.py'
        return_code: Exit = main(
            [
                '--input',
                str(OPEN_API_DATA_PATH / 'api.yaml'),
                '--output',
                str(output_file),
                '--target-python-version',
                '3.6',
            ]
        )
        assert return_code == Exit.OK
        assert (
            output_file.read_text()
            == '''# generated by datamodel-codegen:
#   filename:  api.yaml
#   timestamp: 2019-07-26T00:00:00+00:00

from typing import List, Optional

from pydantic import AnyUrl, BaseModel, Field


class Pet(BaseModel):
    id: int
    name: str
    tag: Optional[str] = None


class Pets(BaseModel):
    __root__: List['Pet']


class User(BaseModel):
    id: int
    name: str
    tag: Optional[str] = None


class Users(BaseModel):
    __root__: List['User']


class Id(BaseModel):
    __root__: str


class Rules(BaseModel):
    __root__: List[str]


class Error(BaseModel):
    code: int
    message: str


class Api(BaseModel):
    apiKey: Optional[str] = Field(
        None, description='To be used as a dataset parameter value'
    )
    apiVersionNumber: Optional[str] = Field(
        None, description='To be used as a version parameter value'
    )
    apiUrl: Optional[AnyUrl] = Field(
        None, description="The URL describing the dataset\'s fields"
    )
    apiDocumentationUrl: Optional[AnyUrl] = Field(
        None, description='A URL to the API console for each API'
    )


class Apis(BaseModel):
    __root__: List['Api']


class Event(BaseModel):
    name: Optional[str] = None


class Result(BaseModel):
    event: Optional['Event'] = None
'''
        )

    with pytest.raises(SystemExit):
        main()


@freeze_time('2019-07-26')
def test_main_autodetect():
    with TemporaryDirectory() as output_dir:
        output_file: Path = Path(output_dir) / 'output.py'
        return_code: Exit = main(
            [
                '--input',
                str(JSON_SCHEMA_DATA_PATH / 'person.json'),
                '--output',
                str(output_file),
                '--input-file-type',
                'auto',
            ]
        )
        assert return_code == Exit.OK
        assert (
            output_file.read_text()
            == '''# generated by datamodel-codegen:
#   filename:  person.json
#   timestamp: 2019-07-26T00:00:00+00:00

from __future__ import annotations

from typing import Any, List, Optional

from pydantic import BaseModel, Field, conint


class Person(BaseModel):
    firstName: Optional[str] = Field(None, description="The person\'s first name.")
    lastName: Optional[str] = Field(None, description="The person\'s last name.")
    age: Optional[conint(ge=0)] = Field(
        None, description='Age in years which must be equal to or greater than zero.'
    )
    friends: Optional[List] = None
    comment: Optional[Any] = None
'''
        )

    with pytest.raises(SystemExit):
        main()


@freeze_time('2019-07-26')
def test_main_autodetect_failed():
    with TemporaryDirectory() as input_dir, TemporaryDirectory() as output_dir:
        input_file: Path = Path(input_dir) / 'input.yaml'
        output_file: Path = Path(output_dir) / 'output.py'

        input_file.write_text(':')

        return_code: Exit = main(
            [
                '--input',
                str(input_file),
                '--output',
                str(output_file),
                '--input-file-type',
                'auto',
            ]
        )
        assert return_code == Exit.ERROR

    with pytest.raises(SystemExit):
        main()


@freeze_time('2019-07-26')
def test_main_jsonschema():
    with TemporaryDirectory() as output_dir:
        output_file: Path = Path(output_dir) / 'output.py'
        return_code: Exit = main(
            [
                '--input',
                str(JSON_SCHEMA_DATA_PATH / 'person.json'),
                '--output',
                str(output_file),
                '--input-file-type',
                'jsonschema',
            ]
        )
        assert return_code == Exit.OK
        assert (
            output_file.read_text()
            == '''# generated by datamodel-codegen:
#   filename:  person.json
#   timestamp: 2019-07-26T00:00:00+00:00

from __future__ import annotations

from typing import Any, List, Optional

from pydantic import BaseModel, Field, conint


class Person(BaseModel):
    firstName: Optional[str] = Field(None, description="The person\'s first name.")
    lastName: Optional[str] = Field(None, description="The person\'s last name.")
    age: Optional[conint(ge=0)] = Field(
        None, description='Age in years which must be equal to or greater than zero.'
    )
    friends: Optional[List] = None
    comment: Optional[Any] = None
'''
        )
    with pytest.raises(SystemExit):
        main()


@freeze_time('2019-07-26')
def test_main_jsonschema_nested_deep():
    import os

    os.chdir(DATA_PATH / 'jsonschema')
    with TemporaryDirectory() as output_dir:
        output_init_file: Path = Path(output_dir) / '__init__.py'
        output_nested_file: Path = Path(output_dir) / 'nested/deep.py'
        output_empty_parent_nested_file: Path = Path(
            output_dir
        ) / 'empty_parent/nested/deep.py'

        return_code: Exit = main(
            [
                '--input',
                str(JSON_SCHEMA_DATA_PATH / 'nested_person.json'),
                '--output',
                str(output_dir),
                '--input-file-type',
                'jsonschema',
            ]
        )
        assert return_code == Exit.OK
        print(list(Path(output_dir).iterdir()))
        assert (
            output_init_file.read_text()
            == '''# generated by datamodel-codegen:
#   filename:  nested_person.json
#   timestamp: 2019-07-26T00:00:00+00:00

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel

from .empty_parent.nested import deep as deep_1
from .nested import deep


class NestedPerson(BaseModel):
    nested_deep_childJson: Optional[deep.Json] = None
    nested_deep_childAnother: Optional[deep.Another] = None
    empty_parent_nested_deep_childJson: Optional[deep_1.Json] = None
'''
        )

        assert (
            output_nested_file.read_text()
            == '''# generated by datamodel-codegen:
#   filename:  nested_person.json
#   timestamp: 2019-07-26T00:00:00+00:00

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class Json(BaseModel):
    firstName: Optional[str] = None


class Another(BaseModel):
    firstName: Optional[str] = None
'''
        )
        assert (
            output_empty_parent_nested_file.read_text()
            == '''# generated by datamodel-codegen:
#   filename:  nested_person.json
#   timestamp: 2019-07-26T00:00:00+00:00

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class Json(BaseModel):
    firstName: Optional[str] = None
'''
        )
    with pytest.raises(SystemExit):
        main()


@freeze_time('2019-07-26')
def test_main_json():
    with TemporaryDirectory() as output_dir:
        output_file: Path = Path(output_dir) / 'output.py'
        return_code: Exit = main(
            [
                '--input',
                str(JSON_DATA_PATH / 'pet.json'),
                '--output',
                str(output_file),
                '--input-file-type',
                'json',
            ]
        )
        assert return_code == Exit.OK
        assert (
            output_file.read_text()
            == '''# generated by datamodel-codegen:
#   filename:  pet.json
#   timestamp: 2019-07-26T00:00:00+00:00

from __future__ import annotations

from pydantic import BaseModel


class Pet(BaseModel):
    name: str
    age: int


class Model(BaseModel):
    Pet: Pet
'''
        )
    with pytest.raises(SystemExit):
        main()


@freeze_time('2019-07-26')
def test_main_json_failed():
    with TemporaryDirectory() as output_dir:
        output_file: Path = Path(output_dir) / 'output.py'
        return_code: Exit = main(
            [
                '--input',
                str(JSON_DATA_PATH / 'broken.json'),
                '--output',
                str(output_file),
                '--input-file-type',
                'json',
            ]
        )
        assert return_code == Exit.ERROR
    with pytest.raises(SystemExit):
        main()


@freeze_time('2019-07-26')
def test_main_yaml():
    with TemporaryDirectory() as output_dir:
        output_file: Path = Path(output_dir) / 'output.py'
        return_code: Exit = main(
            [
                '--input',
                str(YAML_DATA_PATH / 'pet.yaml'),
                '--output',
                str(output_file),
                '--input-file-type',
                'yaml',
            ]
        )
        assert return_code == Exit.OK
        assert (
            output_file.read_text()
            == '''# generated by datamodel-codegen:
#   filename:  pet.yaml
#   timestamp: 2019-07-26T00:00:00+00:00

from __future__ import annotations

from pydantic import BaseModel


class Pet(BaseModel):
    name: str
    age: int


class Model(BaseModel):
    Pet: Pet
'''
        )
    with pytest.raises(SystemExit):
        main()


@pytest.mark.parametrize(
    'expected',
    [
        {
            (
                '__init__.py',
            ): '''\
# generated by datamodel-codegen:
#   filename:  modular.yaml
#   timestamp: 1985-10-26T08:21:00+00:00

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel

from . import models


class Id(BaseModel):
    __root__: str


class Error(BaseModel):
    code: int
    message: str


class Result(BaseModel):
    event: Optional[models.Event] = None


class Source(BaseModel):
    country: Optional[str] = None
''',
            (
                'models.py',
            ): '''\
# generated by datamodel-codegen:
#   filename:  modular.yaml
#   timestamp: 1985-10-26T08:21:00+00:00

from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel


class Species(Enum):
    dog = 'dog'
    cat = 'cat'
    snake = 'snake'


class Pet(BaseModel):
    id: int
    name: str
    tag: Optional[str] = None
    species: Optional[Species] = None


class User(BaseModel):
    id: int
    name: str
    tag: Optional[str] = None


class Event(BaseModel):
    name: Optional[Union[str, float, int, bool, Dict[str, Any], List[str]]] = None
''',
            (
                'collections.py',
            ): '''\
# generated by datamodel-codegen:
#   filename:  modular.yaml
#   timestamp: 1985-10-26T08:21:00+00:00

from __future__ import annotations

from typing import List, Optional

from pydantic import AnyUrl, BaseModel, Field

from . import models


class Pets(BaseModel):
    __root__: List[models.Pet]


class Users(BaseModel):
    __root__: List[models.User]


class Rules(BaseModel):
    __root__: List[str]


class Api(BaseModel):
    apiKey: Optional[str] = Field(
        None, description='To be used as a dataset parameter value'
    )
    apiVersionNumber: Optional[str] = Field(
        None, description='To be used as a version parameter value'
    )
    apiUrl: Optional[AnyUrl] = Field(
        None, description="The URL describing the dataset\'s fields"
    )
    apiDocumentationUrl: Optional[AnyUrl] = Field(
        None, description='A URL to the API console for each API'
    )


class Apis(BaseModel):
    __root__: List[Api]
''',
            (
                'foo',
                '__init__.py',
            ): '''\
# generated by datamodel-codegen:
#   filename:  modular.yaml
#   timestamp: 1985-10-26T08:21:00+00:00

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel

from .. import Id


class Tea(BaseModel):
    flavour: Optional[str] = None
    id: Optional[Id] = None


class Cocoa(BaseModel):
    quality: Optional[int] = None
''',
            (
                'foo',
                'bar.py',
            ): '''\
# generated by datamodel-codegen:
#   filename:  modular.yaml
#   timestamp: 1985-10-26T08:21:00+00:00

from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class Thing(BaseModel):
    attributes: Optional[Dict[str, Any]] = None


class Thang(BaseModel):
    attributes: Optional[List[Dict[str, Any]]] = None


class Clone(Thing):
    pass
''',
            (
                'woo',
                '__init__.py',
            ): '''\
# generated by datamodel-codegen:
#   filename:  modular.yaml
#   timestamp: 1985-10-26T08:21:00+00:00
''',
            (
                'woo',
                'boo.py',
            ): '''\
# generated by datamodel-codegen:
#   filename:  modular.yaml
#   timestamp: 1985-10-26T08:21:00+00:00

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel

from .. import Source, foo


class Chocolate(BaseModel):
    flavour: Optional[str] = None
    source: Optional[Source] = None
    cocoa: Optional[foo.Cocoa] = None
''',
        }
    ],
)
def test_main_modular(
    tmpdir_factory: TempdirFactory, expected: Mapping[str, str]
) -> None:
    """Test main function on modular file."""

    output_directory = Path(tmpdir_factory.mktemp('output'))

    input_filename = OPEN_API_DATA_PATH / 'modular.yaml'
    output_path = output_directory / 'model'

    with freeze_time(TIMESTAMP):
        main(['--input', str(input_filename), '--output', str(output_path)])

    for key, value in expected.items():
        result = output_path.joinpath(*key).read_text()
        assert result == value


def test_main_modular_no_file() -> None:
    """Test main function on modular file with no output name."""

    input_filename = OPEN_API_DATA_PATH / 'modular.yaml'

    assert main(['--input', str(input_filename)]) == Exit.ERROR


def test_main_modular_filename(tmpdir_factory: TempdirFactory) -> None:
    """Test main function on modular file with filename."""

    output_directory = Path(tmpdir_factory.mktemp('output'))

    input_filename = OPEN_API_DATA_PATH / 'modular.yaml'
    output_filename = output_directory / 'model.py'

    assert (
        main(['--input', str(input_filename), '--output', str(output_filename)])
        == Exit.ERROR
    )


@pytest.mark.parametrize(
    'expected',
    [
        '''\
# generated by datamodel-codegen:
#   filename:  api.yaml
#   timestamp: 1985-10-26T08:21:00+00:00

from __future__ import annotations

from typing import List, Optional

from pydantic import AnyUrl, BaseModel, Field


class Pet(BaseModel):
    id: int
    name: str
    tag: Optional[str] = None


class Pets(BaseModel):
    __root__: List[Pet]


class User(BaseModel):
    id: int
    name: str
    tag: Optional[str] = None


class Users(BaseModel):
    __root__: List[User]


class Id(BaseModel):
    __root__: str


class Rules(BaseModel):
    __root__: List[str]


class Error(BaseModel):
    code: int
    message: str


class Api(BaseModel):
    apiKey: Optional[str] = Field(
        None, description='To be used as a dataset parameter value'
    )
    apiVersionNumber: Optional[str] = Field(
        None, description='To be used as a version parameter value'
    )
    apiUrl: Optional[AnyUrl] = Field(
        None, description="The URL describing the dataset\'s fields"
    )
    apiDocumentationUrl: Optional[AnyUrl] = Field(
        None, description='A URL to the API console for each API'
    )


class Apis(BaseModel):
    __root__: List[Api]


class Event(BaseModel):
    name: Optional[str] = None


class Result(BaseModel):
    event: Optional[Event] = None
'''
    ],
)
def test_main_no_file(capsys: CaptureFixture, expected: str) -> None:
    """Test main function on non-modular file with no output name."""

    input_filename = OPEN_API_DATA_PATH / 'api.yaml'

    with freeze_time(TIMESTAMP):
        main(['--input', str(input_filename)])

    captured = capsys.readouterr()
    assert captured.out == expected
    assert not captured.err


@pytest.mark.parametrize(
    'expected',
    [
        '''\
# generated by datamodel-codegen:
#   filename:  api.yaml
#   timestamp: 1985-10-26T08:21:00+00:00

from __future__ import annotations

from typing import List, Optional

from pydantic import AnyUrl, BaseModel, Field


class Pet(BaseModel):  # 1 2, 1 2, this is just a pet
    id: int
    name: str
    tag: Optional[str] = None


class Pets(BaseModel):
    __root__: List[Pet]


class User(BaseModel):
    id: int
    name: str
    tag: Optional[str] = None


class Users(BaseModel):
    __root__: List[User]


class Id(BaseModel):
    __root__: str


class Rules(BaseModel):
    __root__: List[str]


class Error(BaseModel):
    code: int
    message: str


class Api(BaseModel):
    apiKey: Optional[str] = None
    apiVersionNumber: Optional[str] = None
    apiUrl: Optional[AnyUrl] = None
    apiDocumentationUrl: Optional[AnyUrl] = None


class Apis(BaseModel):
    __root__: List[Api]


class Event(BaseModel):
    name: Optional[str] = None


class Result(BaseModel):
    event: Optional[Event] = None
'''
    ],
)
def test_main_custom_template_dir(capsys: CaptureFixture, expected: str) -> None:
    """Test main function with custom template directory."""

    input_filename = OPEN_API_DATA_PATH / 'api.yaml'
    custom_template_dir = DATA_PATH / 'templates'
    extra_template_data = OPEN_API_DATA_PATH / 'extra_data.json'

    with freeze_time(TIMESTAMP):
        main(
            [
                '--input',
                str(input_filename),
                '--custom-template-dir',
                str(custom_template_dir),
                '--extra-template-data',
                str(extra_template_data),
            ]
        )

    captured = capsys.readouterr()
    assert captured.out == expected
    assert not captured.err


@freeze_time('2019-07-26')
def test_pyproject():
    with TemporaryDirectory() as output_dir:
        output_dir = Path(output_dir)
        pyproject_toml = Path(DATA_PATH) / "project" / "pyproject.toml"
        shutil.copy(pyproject_toml, output_dir)
        output_file: Path = output_dir / 'output.py'
        return_code: Exit = main(
            [
                '--input',
                str(OPEN_API_DATA_PATH / 'api.yaml'),
                '--output',
                str(output_file),
            ]
        )
        assert return_code == Exit.OK
        assert (
            output_file.read_text()
            == '''# generated by datamodel-codegen:
#   filename:  api.yaml
#   timestamp: 2019-07-26T00:00:00+00:00

from __future__ import (
    annotations,
)

from typing import (
    List,
    Optional,
)

from pydantic import (
    AnyUrl,
    BaseModel,
    Field,
)


class Pet(BaseModel):
    id: int
    name: str
    tag: Optional[str] = None


class Pets(BaseModel):
    __root__: List[Pet]


class User(BaseModel):
    id: int
    name: str
    tag: Optional[str] = None


class Users(BaseModel):
    __root__: List[User]


class Id(BaseModel):
    __root__: str


class Rules(BaseModel):
    __root__: List[str]


class Error(BaseModel):
    code: int
    message: str


class Api(BaseModel):
    apiKey: Optional[
        str
    ] = Field(
        None,
        description="To be used as a dataset parameter value",
    )
    apiVersionNumber: Optional[
        str
    ] = Field(
        None,
        description="To be used as a version parameter value",
    )
    apiUrl: Optional[
        AnyUrl
    ] = Field(
        None,
        description="The URL describing the dataset\'s fields",
    )
    apiDocumentationUrl: Optional[
        AnyUrl
    ] = Field(
        None,
        description="A URL to the API console for each API",
    )


class Apis(BaseModel):
    __root__: List[Api]


class Event(BaseModel):
    name: Optional[str] = None


class Result(BaseModel):
    event: Optional[
        Event
    ] = None
'''
        )

    with pytest.raises(SystemExit):
        main()


@freeze_time('2019-07-26')
def test_validation():
    with TemporaryDirectory() as output_dir:
        output_file: Path = Path(output_dir) / 'output.py'
        return_code: Exit = main(
            [
                '--input',
                str(OPEN_API_DATA_PATH / 'api.yaml'),
                '--output',
                str(output_file),
                '--validation',
            ]
        )
        assert return_code == Exit.OK
        assert (
            output_file.read_text()
            == '''# generated by datamodel-codegen:
#   filename:  api.yaml
#   timestamp: 2019-07-26T00:00:00+00:00

from __future__ import annotations

from typing import List, Optional

from pydantic import AnyUrl, BaseModel, Field


class Pet(BaseModel):
    id: int
    name: str
    tag: Optional[str] = None


class Pets(BaseModel):
    __root__: List[Pet]


class User(BaseModel):
    id: int
    name: str
    tag: Optional[str] = None


class Users(BaseModel):
    __root__: List[User]


class Id(BaseModel):
    __root__: str


class Rules(BaseModel):
    __root__: List[str]


class Error(BaseModel):
    code: int
    message: str


class Api(BaseModel):
    apiKey: Optional[str] = Field(
        None, description='To be used as a dataset parameter value'
    )
    apiVersionNumber: Optional[str] = Field(
        None, description='To be used as a version parameter value'
    )
    apiUrl: Optional[AnyUrl] = Field(
        None, description="The URL describing the dataset\'s fields"
    )
    apiDocumentationUrl: Optional[AnyUrl] = Field(
        None, description='A URL to the API console for each API'
    )


class Apis(BaseModel):
    __root__: List[Api]


class Event(BaseModel):
    name: Optional[str] = None


class Result(BaseModel):
    event: Optional[Event] = None
'''
        )

    with pytest.raises(SystemExit):
        main()


@freeze_time('2019-07-26')
def test_validation_failed():
    with TemporaryDirectory() as output_dir:
        output_file: Path = Path(output_dir) / 'output.py'
        assert (
            main(
                [
                    '--input',
                    str(OPEN_API_DATA_PATH / 'invalid.yaml'),
                    '--output',
                    str(output_file),
                    '--input-file-type',
                    'openapi',
                    '--validation',
                ]
            )
            == Exit.ERROR
        )
