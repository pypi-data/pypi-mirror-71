from __future__ import absolute_import, unicode_literals

import asyncio

import pytest
from six import string_types

from aioarangodb.exceptions import (
    PregelJobCreateError,
    PregelJobGetError,
    PregelJobDeleteError
)
from aioarangodb.tests.helpers import (
    assert_raises,
    generate_string
)
pytestmark = pytest.mark.asyncio


async def test_pregel_attributes(db, username):
    assert db.pregel.context in ['default', 'async', 'batch', 'transaction']
    assert db.pregel.username == username
    assert db.pregel.db_name == db.name
    assert repr(db.pregel) == '<Pregel in {}>'.format(db.name)


async def test_pregel_management(db, graph, cluster):
    if cluster:
        pytest.skip('Not tested in a cluster setup')

    # Test create pregel job
    job_id = await db.pregel.create_job(
        graph.name,
        'pagerank',
        store=False,
        max_gss=100,
        thread_count=1,
        async_mode=False,
        result_field='result',
        algorithm_params={'threshold': 0.000001}
    )
    assert isinstance(job_id, int)

    # Test create pregel job with unsupported algorithm
    with assert_raises(PregelJobCreateError) as err:
        await db.pregel.create_job(graph.name, 'invalid')
    assert err.value.error_code in {4, 10, 1600}

    # Test get existing pregel job
    job = await db.pregel.job(job_id)
    assert isinstance(job['state'], string_types)
    assert isinstance(job['aggregators'], dict)
    assert isinstance(job['gss'], int)
    assert isinstance(job['received_count'], int)
    assert isinstance(job['send_count'], int)
    assert 'total_runtime' in job

    # Test delete existing pregel job
    assert await db.pregel.delete_job(job_id) is True
    await asyncio.sleep(0.2)
    with assert_raises(PregelJobGetError) as err:
        await db.pregel.job(job_id)
    assert err.value.error_code in {4, 10, 1600}

    # Test delete missing pregel job
    with assert_raises(PregelJobDeleteError) as err:
        await db.pregel.delete_job(generate_string())
    assert err.value.error_code in {4, 10, 1600}
