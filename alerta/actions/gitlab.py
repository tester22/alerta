import os
import logging
import requests

from alerta.actions import app
from alerta.actions import ActionBase

LOG = logging.getLogger('alerta.actions.gitlab')

GITLAB_URL = 'https://gitlab.com/api/v4'
GITLAB_PROJECT_ID = '7422767'
GITLAB_ACCESS_TOKEN=os.environ.get('GITLAB_PERSONAL_ACCESS_TOKEN')


class GitlabIssue(ActionBase):
    
    def get_fields(self, alert):
        metadata = {'name': 'Gitlab','text': alert.text, 'attributes': [
            {'name': 'title', 'type': 'text', 'required': True, 'default': '{} on {}'.format(alert.event, alert.resource)},
            {'name': 'weight', 'type': 'integer', 'required': False, 'regexp': '[0-9]'},
            {'name': 'confidential', 'type': 'bool', 'default': True, 'required': True},
            {'name': 'labels', 'type': 'string', 'required': False}]}
        return metadata
    

    def take_action(self, alert, action, text, attributes):
        """should return internal id of external system"""
        
        
        if action=='gitlab':
            print('take action to create gitlab issue')
            
                
            params = attributes
            # Clean up parameters and make http call.
            params['description'] = text or str(self.get_fields(alert)['text'])
            for field in self.get_fields(alert)['attributes']:
                if not field['name'] in params and field['required']:
                    params[field['name']] = field['default']

            url = '%s/projects/%s/issues' % (GITLAB_URL, GITLAB_PROJECT_ID)
            r = requests.post(url, headers={'Private-Token': GITLAB_ACCESS_TOKEN}, params=params)
            print(r.json())
            issue_id = r.json().get('id', None)
            alert.attributes = {'actionId': issue_id}
            return alert
        else:
            print('action ignored by gitlab action handler')
        return

    def update_alert(self, alert):
        # FIXME - handle updates to alert (eg. normal/ok/cleared)
        return alert
