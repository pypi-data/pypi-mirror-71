# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2016 CERN.
#
# Invenio is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.
"""Pytest configuration."""
from __future__ import absolute_import
from __future__ import print_function

import datetime
import io
import json
import os
import shutil
import tempfile
import unittest.mock
from time import sleep

import pytest
from celery.canvas import Signature
from celery.task import Task
from elasticsearch.exceptions import RequestError
from flask import Flask
from flask_babelex import Babel
from flask_breadcrumbs import Breadcrumbs
from flask_celeryext import FlaskCeleryExt
from flask_oauthlib.provider import OAuth2Provider
from flask_security import login_user
from helpers import fill_oauth2_headers
from helpers import make_pdf_fixture
from invenio_access import InvenioAccess
from invenio_access.models import ActionUsers
from invenio_accounts import InvenioAccounts
from invenio_accounts.views import blueprint as accounts_blueprint
from invenio_assets import InvenioAssets
from invenio_db import db
from invenio_db import InvenioDB
from invenio_deposit import InvenioDeposit
from invenio_deposit import InvenioDepositREST
from invenio_deposit.api import Deposit
from invenio_deposit.scopes import write_scope
from invenio_files_rest import InvenioFilesREST
from invenio_files_rest.models import Location
from invenio_files_rest.views import blueprint as files_rest_blueprint
from invenio_files_rest.views import blueprint as invenio_files_rest_blueprint
from invenio_indexer import InvenioIndexer
from invenio_jsonschemas import InvenioJSONSchemas
from invenio_oauth2server import InvenioOAuth2Server
from invenio_oauth2server import InvenioOAuth2ServerREST
from invenio_oauth2server.models import Client
from invenio_oauth2server.models import Token
from invenio_oauth2server.views import (
    settings_blueprint as oauth2server_settings_blueprint,
)
from invenio_pidstore import InvenioPIDStore
from invenio_records import InvenioRecords
from invenio_records_rest import InvenioRecordsREST
from invenio_records_rest.utils import PIDConverter
from invenio_records_rest.views import create_blueprint_from_app as records_rest_bp
from invenio_records_ui import InvenioRecordsUI
from invenio_records_ui.views import create_blueprint_from_app as records_ui_bp
from invenio_rest import InvenioREST
from invenio_search import current_search
from invenio_search import current_search_client
from invenio_search import InvenioSearch
from invenio_search.errors import IndexAlreadyExistsError
from invenio_search_ui import InvenioSearchUI
from six import BytesIO
from six import get_method_self
from sqlalchemy import inspect
from sqlalchemy_utils.functions import create_database
from sqlalchemy_utils.functions import database_exists
from sqlalchemy_utils.functions import drop_database
from werkzeug.wsgi import DispatcherMiddleware

from invenio_sword import InvenioSword
from invenio_sword.metadata import Metadata
from invenio_sword.typing import BytesReader


def object_as_dict(obj):
    """Make a dict from SQLAlchemy object."""
    return {c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs}


@pytest.fixture()
def test_metadata_format():
    return "http://example.org/TestMetadataFormat"


class TestMetadata(Metadata):
    name = "test"
    content_type = "application/binary"
    metadata_format = "http://example.org/TestMetadataFormat"
    filename = "test.bin"

    def __init__(self, data):
        self.data = data

    @classmethod
    def from_document(
        cls, document: BytesReader, content_type: str, encoding: str = "utf_8"
    ) -> Metadata:
        return cls(document.read())

    def __bytes__(self):
        return self.data


@pytest.yield_fixture()
def base_app(request, test_metadata_format):
    """Flask application fixture."""
    instance_path = tempfile.mkdtemp()

    def init_app(app_):
        app_.config.update(
            CELERY_ALWAYS_EAGER=False,
            CELERY_CACHE_BACKEND="memory",
            CELERY_EAGER_PROPAGATES_EXCEPTIONS=True,
            CELERY_RESULT_BACKEND="cache",
            JSONSCHEMAS_URL_SCHEME="http",
            SECRET_KEY="CHANGE_ME",
            SECURITY_PASSWORD_SALT="CHANGE_ME_ALSO",
            SQLALCHEMY_DATABASE_URI=os.environ.get(
                "SQLALCHEMY_DATABASE_URI", "sqlite:///test.db"
            ),
            SQLALCHEMY_TRACK_MODIFICATIONS=True,
            SQLALCHEMY_ECHO=False,
            TESTING=True,
            WTF_CSRF_ENABLED=False,
            DEPOSIT_SEARCH_API="/api/search",
            SECURITY_PASSWORD_HASH="plaintext",
            SECURITY_PASSWORD_SCHEMES=["plaintext"],
            SECURITY_DEPRECATED_PASSWORD_SCHEMES=[],
            THEME_SITENAME="Test Site",
            OAUTHLIB_INSECURE_TRANSPORT=True,
            OAUTH2_CACHE_TYPE="simple",
            ACCOUNTS_JWT_ENABLE=False,
            # This allows access to files across all of invenio-files-rest
            FILES_REST_PERMISSION_FACTORY=lambda *a, **kw: type(
                "Allow", (object,), {"can": lambda self: True}
            )(),
            FILES_REST_MULTIPART_CHUNKSIZE_MIN=10,
        )
        Babel(app_)
        FlaskCeleryExt(app_)
        Breadcrumbs(app_)
        OAuth2Provider(app_)
        InvenioDB(app_)
        InvenioAccounts(app_)
        InvenioAccess(app_)
        InvenioIndexer(app_)
        InvenioJSONSchemas(app_)
        InvenioOAuth2Server(app_)
        InvenioPIDStore(app_)
        InvenioRecords(app_)
        search = InvenioSearch(app_)
        search.register_mappings("deposits", "invenio_deposit.mappings")

    api_app = Flask("testapiapp", instance_path=instance_path)
    api_app.url_map.converters["pid"] = PIDConverter
    # initialize InvenioDeposit first in order to detect any invalid dependency
    InvenioDepositREST(api_app)

    init_app(api_app)
    InvenioREST(api_app)
    InvenioOAuth2ServerREST(api_app)
    InvenioRecordsREST(api_app)
    InvenioFilesREST(api_app)
    InvenioSword(api_app)
    api_app.register_blueprint(files_rest_blueprint)
    # api_app.register_blueprint(records_files_bp(api_app))
    api_app.register_blueprint(records_rest_bp(api_app))
    api_app.register_blueprint(invenio_files_rest_blueprint)

    # Register a test (alternate) metadata format
    api_app.config["SWORD_ENDPOINTS"]["depid"]["metadata_formats"][
        test_metadata_format
    ] = TestMetadata

    app = Flask("testapp", instance_path=instance_path)
    app.url_map.converters["pid"] = PIDConverter
    # initialize InvenioDeposit first in order to detect any invalid dependency
    InvenioDeposit(app)
    init_app(app)
    app.register_blueprint(accounts_blueprint)
    app.register_blueprint(oauth2server_settings_blueprint)
    InvenioAssets(app)
    InvenioSearchUI(app)
    InvenioRecordsUI(app)
    app.register_blueprint(records_ui_bp(app))
    app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {"/api": api_app.wsgi_app})

    with app.app_context():
        if str(db.engine.url) != "sqlite://" and not database_exists(
            str(db.engine.url)
        ):
            create_database(str(db.engine.url))
        db.create_all()

    yield app

    with app.app_context():
        if str(db.engine.url) != "sqlite://":
            drop_database(str(db.engine.url))
        shutil.rmtree(instance_path)


@pytest.yield_fixture()
def app(base_app):
    """Yield the REST API application in its context."""
    with base_app.app_context():
        yield base_app


@pytest.yield_fixture()
def api(base_app):
    """Yield the REST API application in its context."""
    api = get_method_self(base_app.wsgi_app.mounts["/api"])
    # api.register_blueprint(records_rest_bp(api))
    with api.app_context():
        yield api


@pytest.yield_fixture()
def test_client(base_app):
    """Test client."""
    with base_app.test_client() as client_:
        yield client_


@pytest.fixture()
def users(app):
    """Create users."""
    with db.session.begin_nested():
        datastore = app.extensions["security"].datastore
        user1 = datastore.create_user(
            email="info@inveniosoftware.org", password="tester", active=True
        )
        user2 = datastore.create_user(
            email="test@inveniosoftware.org", password="tester2", active=True
        )
        admin = datastore.create_user(
            email="admin@inveniosoftware.org", password="tester3", active=True
        )
        # Assign deposit-admin-access to admin only.
        db.session.add(ActionUsers(action="deposit-admin-access", user=admin))
    db.session.commit()
    return [object_as_dict(user1), object_as_dict(user2)]


@pytest.fixture()
def client(app, users):
    """Create client."""
    with db.session.begin_nested():
        # create resource_owner -> client_1
        client_ = Client(
            client_id="client_test_u1c1",
            client_secret="client_test_u1c1",
            name="client_test_u1c1",
            description="",
            is_confidential=False,
            user_id=users[0]["id"],
            _redirect_uris="",
            _default_scopes="",
        )
        db.session.add(client_)
    db.session.commit()
    return client_


@pytest.fixture()
def write_token_user_1(app, client, users):
    """Create token."""
    with db.session.begin_nested():
        token_ = Token(
            client=client,
            user_id=users[0]["id"],
            access_token="dev_access_1",
            refresh_token="dev_refresh_1",
            expires=datetime.datetime.now() + datetime.timedelta(hours=10),
            is_personal=False,
            is_internal=True,
            _scopes=write_scope.id,
        )
        db.session.add(token_)
    db.session.commit()
    return token_


@pytest.fixture()
def write_token_user_2(app, client, users):
    """Create token."""
    with db.session.begin_nested():
        token_ = Token(
            client=client,
            user_id=users[1]["id"],
            access_token="dev_access_2",
            refresh_token="dev_refresh_2",
            expires=datetime.datetime.now() + datetime.timedelta(hours=10),
            is_personal=False,
            is_internal=True,
            _scopes=write_scope.id,
        )
        db.session.add(token_)
    db.session.commit()
    return token_


@pytest.fixture()
def fake_schemas(app, api, es, tmpdir):
    """Fake schema."""
    schemas = tmpdir.mkdir("schemas")
    empty_schema = '{"title": "Empty"}'
    for path in (
        ("deposit-v1.0.0.json",),
        ("deposits", "test-v1.0.0.json"),
        ("test-v1.0.0.json",),
    ):
        schema = schemas
        for section in path[:-1]:
            schema = schema.mkdir(section)
        schema = schema.join(path[-1])
        schema.write(empty_schema)

    app.extensions["invenio-jsonschemas"].register_schemas_dir(schemas.strpath)
    api.extensions["invenio-jsonschemas"].register_schemas_dir(schemas.strpath)


@pytest.yield_fixture()
def es(app):
    """Elasticsearch fixture."""
    try:
        list(current_search.create())
    except (RequestError, IndexAlreadyExistsError):
        list(current_search.delete(ignore=[404]))
        list(current_search.create(ignore=[400]))
    current_search_client.indices.refresh()
    yield current_search_client
    list(current_search.delete(ignore=[404]))


@pytest.fixture()
def location(app):
    """Create default location."""
    tmppath = tempfile.mkdtemp()
    with db.session.begin_nested():
        Location.query.delete()
        loc = Location(name="local", uri=tmppath, default=True)
        db.session.add(loc)
    db.session.commit()
    return location


@pytest.fixture()
def deposit(app, es, users, location):
    """New deposit with files."""
    record = {"title": "fuu"}
    with app.test_request_context():
        datastore = app.extensions["security"].datastore
        login_user(datastore.find_user(email=users[0]["email"]))
        deposit = Deposit.create(record)
        deposit.commit()
        db.session.commit()
    sleep(2)
    return deposit


@pytest.fixture()
def files(app, deposit):
    """Add a file to the deposit."""
    content = b"### Testing textfile ###"
    stream = BytesIO(content)
    key = "hello.txt"
    deposit.files[key] = stream
    deposit.commit()
    db.session.commit()
    return list(deposit.files)


@pytest.fixture()
def pdf_file(app):
    """Create a test pdf file."""
    return {"file": make_pdf_fixture("test.pdf"), "name": "test.pdf"}


@pytest.fixture()
def pdf_file2(app):
    """Create a test pdf file."""
    return {"file": make_pdf_fixture("test2.pdf", "test"), "name": "test2.pdf"}


@pytest.fixture()
def pdf_file2_samename(app):
    """Create a test pdf file."""
    return {"file": make_pdf_fixture("test2.pdf", "test same"), "name": "test2.pdf"}


@pytest.fixture()
def json_headers():
    """JSON headers."""
    return [("Content-Type", "application/json"), ("Accept", "application/json")]


@pytest.fixture()
def oauth2_headers_user_1(app, json_headers, write_token_user_1):
    """Authentication headers (with a valid oauth2 token).

    It uses the token associated with the first user.
    """
    return fill_oauth2_headers(json_headers, write_token_user_1)


@pytest.fixture()
def oauth2_headers_user_2(app, json_headers, write_token_user_2):
    """Authentication headers (with a valid oauth2 token).

    It uses the token associated with the second user.
    """
    return fill_oauth2_headers(json_headers, write_token_user_2)


@pytest.fixture()
def metadata_document():
    return io.BytesIO(
        json.dumps(
            {
                "@context": "https://swordapp.github.io/swordv3/swordv3.jsonld",
                "@id": "http://example.com/object/1/metadata",
                "@type": "Metadata",
                "dc:title": "The title",
                "dcterms:abstract": "This is my abstract",
                "dc:contributor": "A.N. Other",
            }
        ).encode()
    )


@pytest.yield_fixture()
def task_delay():
    mock_obj = unittest.mock.Mock()

    def delay(self):
        mock_obj(self)

    with unittest.mock.patch.object(
        Signature, "delay", delay
    ), unittest.mock.patch.object(Task, "delay", delay):
        yield mock_obj


@pytest.fixture()
def fixtures_path():
    return os.path.join(os.path.dirname(__file__), "fixtures")
