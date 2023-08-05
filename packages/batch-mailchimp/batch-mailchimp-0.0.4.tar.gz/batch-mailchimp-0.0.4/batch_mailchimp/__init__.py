from mailchimp3 import MailChimp

from .batch_operations import BatchOperations


class Batch:
    def __init__(self, client):
        self._mc_client = client
        self.operations = []
        self._run = False
        self.id = None

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
            self._mc_client._pause_batch = True
            resp = fn(self, *args, **kwargs)
            self._mc_client._pause_batch = False
            return resp
        return wrapper

    @_pause_batch
    def status(self, **kwargs):
        return self._mc_client.batch_operations.get(self, **kwargs)

    @_pause_batch
    def run(self):
        resp = self._mc_client.batch_operations.create(self)
        self._mc_client.reset_batch()
        return resp

    @_pause_batch
    def delete(self):
        return self._mc_client.batch_operations.delete(self)


class FakeRequest:
    def __init__(self, batch, **kwargs):
        self.status_code = 200
        self.batch = batch
        operation = {
            'method': kwargs.get('method'),
            'path': kwargs.get('url'),
        }
        if 'body' in kwargs:
            operation['body'] = kwargs['body']
        self.batch.operations.append(operation)

    def json(self):
        return self.batch


class BatchMailChimp(MailChimp):
    def run_batch(self):
        return self.batch.run()

    def reset_batch(self):
        self.batch = Batch(self)
        return self.batch

    def __init__(self, *args, batch=False, **kwargs):
        super(BatchMailChimp, self).__init__(*args, **kwargs)
        if batch:
            self.reset_batch()
            self._pause_batch = False
        else:
            self.batch = False
        # Batch Operations
        self.batches = self.batch_operations = BatchOperations(self)

    def _make_request(self, **kwargs):
        if self.batch and not self._pause_batch:
            return FakeRequest(self.batch, **kwargs)
        return super(BatchMailChimp, self)._make_request(**kwargs)
