import json

from mailchimp3 import MailChimp

from .batch_operations import BatchOperations


class Batch:
    def __init__(self, client):
        self._mc_client = client
        self.operations = []
        self._run = False
        self.id = None

    def __getitem__(self, item):
        if item == 'id':
            return self.id

    def __repr__(self):
        return '<{}.{}: {} operation{}{}>'.format(
            self.__class__.__module__,
            self.__class__.__name__,
            len(self.operations),
            's' if len(self.operations) != 1 else '',
            '*' if not self._run else '',
        )

    def _pause_batch(fn):
        def wrapper(self, *args, **kwargs):
            self._mc_client._is_paused = True
            resp = fn(self, *args, **kwargs)
            self._mc_client._is_paused = False
            return resp
        return wrapper

    @_pause_batch
    def status(self, **kwargs):
        return self._mc_client.batch_operations.get(self, **kwargs)

    @_pause_batch
    def run(self):
        self._mc_client.batch_operations.create(self)
        self._mc_client.batch = None
        return self

    @_pause_batch
    def delete(self):
        return self._mc_client.batch_operations.delete(self)


class FakeRequest:
    def __init__(self, batch, **kwargs):
        self.status_code = 200
        if not batch:
            batch = Batch(self)
        self.batch = batch
        operation = {
            'method': kwargs.get('method'),
            'path': kwargs.get('url'),
        }
        if 'json' in kwargs:
            operation['body'] = json.dumps(kwargs['json'])
        self.batch.operations.append(operation)

    def json(self):
        return self.batch


class BatchMailChimp(MailChimp):
    def __init__(self, *args, batch=False, **kwargs):
        super(BatchMailChimp, self).__init__(*args, **kwargs)
        self._is_batch = batch
        self._is_paused = False
        self.batch = None
        # Batch Operations
        self.batches = self.batch_operations = BatchOperations(self)

    def _make_request(self, **kwargs):
        if self._is_batch and not self._is_paused:
            return FakeRequest(self.batch, **kwargs)
        return super(BatchMailChimp, self)._make_request(**kwargs)
