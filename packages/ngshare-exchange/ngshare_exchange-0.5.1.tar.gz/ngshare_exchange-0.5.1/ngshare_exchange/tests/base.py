from logging import getLogger
from pathlib import Path
import urllib

import pytest
from requests import PreparedRequest
import requests_mock as rq_mock
from requests_mock import Mocker

from nbgrader.coursedir import CourseDirectory
from .. import Exchange


def parse_body(body: str):
    # https://stackoverflow.com/questions/48018622/how-can-see-the-request-data#51052385
    return dict(urllib.parse.parse_qsl(body))


class TestExchange:
    course_id = 'abc101'
    assignment_id = 'ps1'
    student_id = 'student_1'
    notebook_id = 'p1'
    test_failed = False
    test_completed = False

    def _init_cache_dir(self, tmpdir_factory):
        return Path(tmpdir_factory.mktemp('nbgrader_cache')).absolute()

    def _init_course_dir(self, tmpdir_factory):
        return Path(tmpdir_factory.mktemp(self.course_id)).absolute()

    def _mock_all(self, request: PreparedRequest, content):
        getLogger().fatal(
            'The request "%s" has not been mocked yet.', request.url
        )
        content.status_code = 404
        return ''

    def _new_exchange_object(self, cls, course_id, assignment_id, student_id):
        assert issubclass(cls, Exchange)
        cls.cache = str(self.cache_dir)
        coursedir = CourseDirectory()
        coursedir.root = str(self.course_dir)
        coursedir.course_id = course_id
        coursedir.assignment_id = assignment_id
        obj = cls(coursedir=coursedir)
        obj.username = student_id
        return obj

    @property
    def files_path(self) -> Path:
        return Path(__file__).parent / 'files'

    @pytest.fixture(autouse=True)
    def init(self, requests_mock: Mocker, tmpdir_factory):
        Exchange._ngshare_url = "http://example.com"
        self.base_url = Exchange.ngshare_url.fget(Exchange)
        self.course_dir = self._init_course_dir(tmpdir_factory)
        self.cache_dir = self._init_cache_dir(tmpdir_factory)
        self.requests_mocker = requests_mock
        requests_mock.register_uri(
            rq_mock.ANY, rq_mock.ANY, text=self._mock_all
        )

    def mock_404(self):
        self.requests_mocker.register_uri(
            rq_mock.ANY, rq_mock.ANY, status_code=404
        )

    def mock_unsuccessful(self):
        self.requests_mocker.register_uri(
            rq_mock.ANY,
            rq_mock.ANY,
            json={'success': False, 'message': 'Something happened'},
        )
