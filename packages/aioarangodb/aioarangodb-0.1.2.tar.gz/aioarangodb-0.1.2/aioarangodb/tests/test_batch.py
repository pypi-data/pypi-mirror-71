from __future__ import absolute_import, unicode_literals

import json

import mock
import pytest
from six import string_types

from aioarangodb.database import BatchDatabase
from aioarangodb.exceptions import (
    DocumentInsertError,
    BatchExecuteError,
    BatchJobResultError,
    BatchStateError
)
from aioarangodb.job import BatchJob
from aioarangodb.tests.helpers import extract, clean_doc
pytestmark = pytest.mark.asyncio

async def test_batch_wrapper_attributes(db, col, username):
    batch_db = db.begin_batch_execution()
    assert isinstance(batch_db, BatchDatabase)
    assert batch_db.username == username
    assert batch_db.context == 'batch'
    assert batch_db.db_name == db.name
    assert batch_db.name == db.name
    assert repr(batch_db) == '<BatchDatabase {}>'.format(db.name)

    batch_col = batch_db.collection(col.name)
    assert batch_col.username == username
    assert batch_col.context == 'batch'
    assert batch_col.db_name == db.name
    assert batch_col.name == col.name

    batch_aql = batch_db.aql
    assert batch_aql.username == username
    assert batch_aql.context == 'batch'
    assert batch_aql.db_name == db.name

    job = await batch_aql.execute('INVALID QUERY')
    assert isinstance(job, BatchJob)
    assert isinstance(job.id, string_types)
    assert repr(job) == '<BatchJob {}>'.format(job.id)


async def test_batch_execute_without_result(db, col, docs):
    async with db.begin_batch_execution(return_result=False) as batch_db:
        batch_col = batch_db.collection(col.name)
        # Ensure that no jobs are returned
        assert await batch_col.insert(docs[0]) is None
        assert await batch_col.delete(docs[0]) is None
        assert await batch_col.insert(docs[1]) is None
        assert await batch_col.delete(docs[1]) is None
        assert await batch_col.insert(docs[2]) is None
        assert await batch_col.get(docs[2]) is None
        assert batch_db.queued_jobs() is None

    # Ensure that the operations went through
    assert batch_db.queued_jobs() is None
    assert await extract('_key', await col.all()) == [docs[2]['_key']]


async def test_batch_execute_with_result(db, col, docs):
    async with db.begin_batch_execution(return_result=True) as batch_db:
        batch_col = batch_db.collection(col.name)
        job1 = await batch_col.insert(docs[0])
        job2 = await batch_col.insert(docs[1])
        job3 = await batch_col.insert(docs[1])  # duplicate
        jobs = batch_db.queued_jobs()
        assert jobs == [job1, job2, job3]
        assert all(job.status() == 'pending' for job in jobs)

    assert batch_db.queued_jobs() == [job1, job2, job3]
    assert all(job.status() == 'done' for job in batch_db.queued_jobs())
    assert await extract('_key', await col.all()) == await extract('_key', docs[:2])

    # Test successful results
    assert job1.result()['_key'] == docs[0]['_key']
    assert job2.result()['_key'] == docs[1]['_key']

    # Test insert error result
    with pytest.raises(DocumentInsertError) as err:
        await job3.result()
    assert err.value.error_code == 1210


async def test_batch_empty_commit(db):
    batch_db = db.begin_batch_execution(return_result=False)
    assert await batch_db.commit() is None

    batch_db = db.begin_batch_execution(return_result=True)
    assert await batch_db.commit() == []


async def test_batch_double_commit(db, col, docs):
    batch_db = db.begin_batch_execution()
    job = await batch_db.collection(col.name).insert(docs[0])

    # Test first commit
    assert await batch_db.commit() == [job]
    assert job.status() == 'done'
    assert await col.count() == 1
    assert await clean_doc(await col.random()) == docs[0]

    # Test second commit which should fail
    with pytest.raises(BatchStateError) as err:
        await batch_db.commit()
    assert 'already committed' in str(err.value)
    assert await col.count() == 1
    assert await clean_doc(await col.random()) == docs[0]


async def test_batch_action_after_commit(db, col):
    async with db.begin_batch_execution() as batch_db:
        await batch_db.collection(col.name).insert({})

    # Test insert after the batch has been committed
    with pytest.raises(BatchStateError) as err:
        await batch_db.collection(col.name).insert({})
    assert 'already committed' in str(err.value)
    assert await col.count() == 1


async def test_batch_execute_error(bad_db, col, docs):
    batch_db = bad_db.begin_batch_execution(return_result=True)
    job = await batch_db.collection(col.name).insert_many(docs)

    # Test batch execute with bad database
    with pytest.raises(BatchExecuteError) as err:
        await batch_db.commit()
    assert err.value.error_code in {11, 1228}
    assert await col.count() == 0
    assert job.status() == 'pending'


async def test_batch_job_result_not_ready(db, col, docs):
    batch_db = db.begin_batch_execution(return_result=True)
    job = await batch_db.collection(col.name).insert_many(docs)

    # Test get job result before commit
    with pytest.raises(BatchJobResultError) as err:
        await job.result()
    assert str(err.value) == 'result not available yet'

    # Test commit to make sure it still works after the errors
    assert await batch_db.commit() == [job]
    assert len(job.result()) == len(docs)
    assert await extract('_key', await col.all()) == await extract('_key', docs)


class AsyncMock(mock.MagicMock):
    async def __call__(self, *args, **kwargs):
        return super(AsyncMock, self).__call__(*args, **kwargs)

async def test_batch_bad_state(db, col, docs):
    batch_db = db.begin_batch_execution()
    batch_col = batch_db.collection(col.name)
    await batch_col.insert(docs[0])
    await batch_col.insert(docs[1])
    await batch_col.insert(docs[2])

    # Monkey patch the connection object
    mock_resp = mock.MagicMock()
    mock_resp.is_success = True
    mock_resp.raw_body = ''
    mock_send_request = AsyncMock()
    mock_send_request.return_value = mock_resp
    mock_connection = mock.MagicMock()
    mock_connection.send_request = mock_send_request
    mock_connection.serialize = json.dumps
    mock_connection.deserialize = json.loads
    batch_db._executor._conn = mock_connection

    # Test commit with invalid batch state
    with pytest.raises(BatchStateError) as err:
        await batch_db.commit()
    assert 'expecting 3 parts in batch response but got 0' in str(err.value)
