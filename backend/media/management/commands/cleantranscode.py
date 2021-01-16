from django.core.management.base import BaseCommand, CommandError
from django.contrib.sessions.models import Session
from datetime import datetime
from backend.settings import pause_transcodes_after, terminate_transcodes_after
import re
import os
import signal

class Command(BaseCommand):
    help = 'pasue/terminate nonactive transcodes'

    def handle(self, *args, **options):
        sessions = Session.objects.all()
        uuid_re = '[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'

        terminated = 0
        paused = 0
        not_exist = 0

        for session in sessions:
            data = session.get_decoded()
            for key, value in data.items():
                if not re.search(uuid_re, key) and not isinstance(value, dict):
                    continue
                updated_time = value.get('updating_time')
                group_pid = value.get('group_pid')
                if not updated_time or not group_pid:
                    continue
                updated_time = datetime.fromisoformat(updated_time)
                try:
                    # pause transcoding
                    if (datetime.now() - updated_time).seconds > terminate_transcodes_after:
                        os.killpg(group_pid, signal.SIGTERM)
                        terminated += 1
                    # terminate transcoding
                    elif (datetime.now() - updated_time).seconds > pause_transcodes_after:
                        os.killpg(group_pid, signal.SIGSTOP)
                        paused += 1
                except ProcessLookupError:
                    not_exist += 1
        self.stdout.write('{}\tterminated: {}, paused: {}, not_exist: {}'.format(datetime.now().isoformat(), terminated, paused, not_exist))