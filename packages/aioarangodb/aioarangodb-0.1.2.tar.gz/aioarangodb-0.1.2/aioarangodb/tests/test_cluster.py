from __future__ import absolute_import, unicode_literals

import pytest

from aioarangodb.errno import (
    DATABASE_NOT_FOUND,
    FORBIDDEN
)
from aioarangodb.exceptions import (
    ClusterEndpointsError,
    ClusterHealthError,
    ClusterMaintenanceModeError,
    ClusterServerEngineError,
    ClusterServerIDError,
    ClusterServerRoleError,
    ClusterServerStatisticsError,
    ClusterServerVersionError,
)
from aioarangodb.tests.helpers import assert_raises
pytestmark = pytest.mark.asyncio


async def test_cluster_server_id(sys_db, bad_db, cluster):
    if not cluster:
        pytest.skip('Only tested in a cluster setup')

    result = await sys_db.cluster.server_id()
    assert isinstance(result, str)

    with assert_raises(ClusterServerIDError) as err:
        await bad_db.cluster.server_id()
    assert err.value.error_code in {FORBIDDEN, DATABASE_NOT_FOUND}


async def test_cluster_server_role(sys_db, bad_db, cluster):
    if not cluster:
        pytest.skip('Only tested in a cluster setup')

    result = await sys_db.cluster.server_role()
    assert isinstance(result, str)

    with assert_raises(ClusterServerRoleError) as err:
        await bad_db.cluster.server_role()
    assert err.value.error_code in {FORBIDDEN, DATABASE_NOT_FOUND}


async def test_cluster_health(sys_db, bad_db, cluster):
    if not cluster:
        pytest.skip('Only tested in a cluster setup')

    result = await sys_db.cluster.health()
    assert 'Health' in result
    assert 'ClusterId' in result

    with assert_raises(ClusterHealthError) as err:
        await bad_db.cluster.health()
    assert err.value.error_code in {FORBIDDEN, DATABASE_NOT_FOUND}


async def test_cluster_server_version(sys_db, bad_db, cluster):
    if not cluster:
        pytest.skip('Only tested in a cluster setup')

    server_id = await sys_db.cluster.server_id()
    result = await sys_db.cluster.server_version(server_id)
    assert 'server' in result
    assert 'version' in result

    with assert_raises(ClusterServerVersionError) as err:
        await bad_db.cluster.server_version(server_id)
    assert err.value.error_code in {FORBIDDEN, DATABASE_NOT_FOUND}


async def test_cluster_server_engine(sys_db, bad_db, cluster):
    if not cluster:
        pytest.skip('Only tested in a cluster setup')

    server_id = await sys_db.cluster.server_id()
    result = await sys_db.cluster.server_engine(server_id)
    assert 'name' in result
    assert 'supports' in result

    with assert_raises(ClusterServerEngineError) as err:
        bad_db.cluster.server_engine(server_id)
    assert err.value.error_code in {FORBIDDEN, DATABASE_NOT_FOUND}


async def test_cluster_server_statistics(sys_db, bad_db, cluster):
    if not cluster:
        pytest.skip('Only tested in a cluster setup')

    server_id = await sys_db.cluster.server_id()
    result = await sys_db.cluster.server_statistics(server_id)
    assert 'time' in result
    assert 'system' in result
    assert 'enabled' in result

    with assert_raises(ClusterServerStatisticsError) as err:
        await bad_db.cluster.server_statistics(server_id)
    assert err.value.error_code in {FORBIDDEN, DATABASE_NOT_FOUND}


async def test_cluster_toggle_maintenance_mode(sys_db, bad_db, cluster):
    if not cluster:
        pytest.skip('Only tested in a cluster setup')

    result = await sys_db.cluster.toggle_maintenance_mode('on')
    assert 'error' in result
    assert 'warning' in result

    result = await sys_db.cluster.toggle_maintenance_mode('off')
    assert 'error' in result
    assert 'warning' in result

    with assert_raises(ClusterMaintenanceModeError) as err:
        await bad_db.cluster.toggle_maintenance_mode('on')
    assert err.value.error_code in {FORBIDDEN, DATABASE_NOT_FOUND}


async def test_cluster_endpoints(db, bad_db, cluster):
    if not cluster:
        pytest.skip('Only tested in a cluster setup')

    # Test get server endpoints
    assert len(await db.cluster.endpoints()) > 0

    # Test get server endpoints with bad database
    with assert_raises(ClusterEndpointsError) as err:
        await bad_db.cluster.endpoints()
    assert err.value.error_code in {11, 1228}
