import urllib
import requests

from st2actions.runners.pythonrunner import Action

class SlackAction(Action):

    
    def run(self, **kwargs):
        if kwargs['token'] is None:
            kwargs['token'] = self.config['action_token']

        return self._get_request(kwargs)

    def _get_request(self, params):
        end_point = params['end_point']
        url = "https://slack.com/api/%s" % end_point
        del params['end_point']

        headers = {}
        headers['Content-Type'] = 'application/x-www-form-urlencoded'

        data = urllib.urlencode(params)
        self.logger.info(data)
        response = requests.get(url=url,
                                headers=headers, params=data)

        results = response.json()
        if results['ok'] is True:
            return results
        else:
            failure_reason = ('Failed to perform action %s: %s \
                              (status code: %s)' % (end_point, response.text,
                              response.status_code))
            self.logger.exception(failure_reason)
            raise Exception(failure_reason)