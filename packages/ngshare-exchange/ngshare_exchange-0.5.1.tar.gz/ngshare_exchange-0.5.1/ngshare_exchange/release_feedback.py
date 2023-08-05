import os
import glob
import re
import base64
import json

from nbgrader.exchange.abc import (
    ExchangeReleaseFeedback as ABCExchangeReleaseFeedback,
)
from .exchange import Exchange


class ExchangeReleaseFeedback(Exchange, ABCExchangeReleaseFeedback):
    def init_src(self):
        student_id = (
            self.coursedir.student_id if self.coursedir.student_id else '*'
        )
        self.src_path = self.coursedir.format_path(
            self.coursedir.feedback_directory,
            student_id,
            self.coursedir.assignment_id,
        )

    def init_dest(self):
        if self.coursedir.course_id == '':
            self.fail('No course id specified. Re-run with --course flag.')

    def copy_files(self):
        if self.coursedir.student_id_exclude:
            exclude_students = set(self.coursedir.student_id_exclude.split(','))
        else:
            exclude_students = set()

        staged_feedback = {}  # Maps student IDs to submissions.
        html_files = glob.glob(os.path.join(self.src_path, '*.html'))
        for html_file in html_files:
            regexp = re.escape(os.path.sep).join(
                [
                    self.coursedir.format_path(
                        self.coursedir.feedback_directory,
                        '(?P<student_id>.*)',
                        self.coursedir.assignment_id,
                        escape=True,
                    ),
                    '(?P<notebook_id>.*).html',
                ]
            )

            m = re.match(regexp, html_file)
            if m is None:
                msg = 'Could not match "%s" with regexp "%s"' % (
                    html_file,
                    regexp,
                )
                self.log.error(msg)
                continue

            gd = m.groupdict()
            student_id = gd['student_id']
            notebook_id = gd['notebook_id']
            if student_id in exclude_students:
                self.log.debug('Skipping student "{}"'.format(student_id))
                continue

            feedback_dir = os.path.split(html_file)[0]
            with open(
                os.path.join(feedback_dir, 'timestamp.txt')
            ) as timestamp_file:
                timestamp = timestamp_file.read()

            if student_id not in staged_feedback.keys():
                # Maps timestamp to feedback.
                staged_feedback[student_id] = {}
            if timestamp not in staged_feedback[student_id].keys():
                # List of info.
                staged_feedback[student_id][timestamp] = []
            staged_feedback[student_id][timestamp].append(
                {'notebook_id': notebook_id, 'path': html_file}
            )
        # Student.
        for student_id, submission in staged_feedback.items():
            # Submission.
            for timestamp, feedback_info in submission.items():
                self.log.info(
                    'Releasing feedback for student "{}" on '
                    'assignment "{}/{}/{}" ({})'.format(
                        student_id,
                        self.coursedir.course_id,
                        self.coursedir.assignment_id,
                        notebook_id,
                        timestamp,
                    )
                )
                retvalue = self.post_feedback(
                    student_id, timestamp, feedback_info
                )
                if retvalue is None:
                    self.fail('Failed to upload feedback to server.')
                else:
                    self.log.info('Feedback released.')

    def post_feedback(self, student_id, timestamp, feedback_info):
        '''
        Uploads feedback files for a specific submission.
        ``feedback_info`` - A list of feedback files. Each feedback file is
        represented as a dictionary with a 'path' to the local feedback file and
        'notebook_id' of the corresponding notebook.
        '''
        url = '/feedback/{}/{}/{}'.format(
            self.coursedir.course_id, self.coursedir.assignment_id, student_id
        )
        files = json.dumps(
            [
                self.encode_file(x['path'], '{}.html'.format(x['notebook_id']))
                for x in feedback_info
            ]
        )
        data = {'timestamp': timestamp, 'files': files}

        return self.ngshare_api_post(url, data)

    # TODO: Consider moving into Exchange.
    def encode_file(self, filesystem_path, assignment_path):
        with open(filesystem_path, 'rb') as f:
            content = f.read()
        return {
            'path': assignment_path,
            'content': base64.encodebytes(content).decode(),
        }
