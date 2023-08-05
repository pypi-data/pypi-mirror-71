from __future__ import absolute_import, unicode_literals

import pytest

from aioarangodb.exceptions import (
    CollectionCreateError,
    CollectionListError,
    CollectionPropertiesError,
    DocumentInsertError,
    PermissionResetError,
    PermissionGetError,
    PermissionUpdateError,
    PermissionListError
)
from aioarangodb.tests.helpers import (
    assert_raises,
    extract,
    generate_col_name,
    generate_db_name,
    generate_string,
    generate_username
)
pytestmark = pytest.mark.asyncio


async def test_permission_management(client, sys_db, bad_db, cluster):
    if cluster:
        pytest.skip('Not tested in a cluster setup')

    username = generate_username()
    password = generate_string()
    db_name = generate_db_name()
    col_name_1 = generate_col_name()
    col_name_2 = generate_col_name()

    await sys_db.create_database(
        name=db_name,
        users=[{
            'username': username,
            'password': password,
            'active': True
        }]
    )
    db = await client.db(db_name, username, password)
    assert isinstance(await sys_db.permissions(username), dict)

    # Test list permissions with bad database
    with assert_raises(PermissionListError) as err:
        await bad_db.permissions(username)
    assert err.value.error_code in {11, 1228}

    # Test get permission with bad database
    with assert_raises(PermissionGetError) as err:
        await bad_db.permission(username, db_name)
    assert err.value.error_code in {11, 1228}

    # The user should not have read and write permissions
    assert await sys_db.permission(username, db_name) == 'rw'
    assert await sys_db.permission(username, db_name, col_name_1) == 'rw'

    # Test update permission (database level) with bad database
    with assert_raises(PermissionUpdateError):
        await bad_db.update_permission(username, 'ro', db_name)
    assert await sys_db.permission(username, db_name) == 'rw'

    # Test update permission (database level) to read only and verify access
    assert await sys_db.update_permission(username, 'ro', db_name) is True
    assert await sys_db.permission(username, db_name) == 'ro'
    with assert_raises(CollectionCreateError) as err:
        await db.create_collection(col_name_2)
    assert err.value.http_code == 403
    assert col_name_1 not in await extract('name', await db.collections())
    assert col_name_2 not in await extract('name', await db.collections())

    # Test reset permission (database level) with bad database
    with assert_raises(PermissionResetError) as err:
        await bad_db.reset_permission(username, db_name)
    assert err.value.error_code in {11, 1228}
    assert await sys_db.permission(username, db_name) == 'ro'

    # Test reset permission (database level) and verify access
    assert await sys_db.reset_permission(username, db_name) is True
    assert await sys_db.permission(username, db_name) == 'none'
    with assert_raises(CollectionCreateError) as err:
        await db.create_collection(col_name_1)
    assert err.value.http_code == 401
    with assert_raises(CollectionListError) as err:
        await db.collections()
    assert err.value.http_code == 401

    # Test update permission (database level) and verify access
    assert await sys_db.update_permission(username, 'rw', db_name) is True
    assert await sys_db.permission(username, db_name, col_name_2) == 'rw'
    assert await db.create_collection(col_name_1) is not None
    assert await db.create_collection(col_name_2) is not None
    assert col_name_1 in await extract('name', await db.collections())
    assert col_name_2 in await extract('name', await db.collections())

    col_1 = await db.collection(col_name_1)
    col_2 = await db.collection(col_name_2)

    # Verify that user has read and write access to both collections
    assert isinstance(await col_1.properties(), dict)
    assert isinstance(await col_1.insert({}), dict)
    assert isinstance(await col_2.properties(), dict)
    assert isinstance(await col_2.insert({}), dict)

    # Test update permission (collection level) to read only and verify access
    assert await sys_db.update_permission(username, 'ro', db_name, col_name_1)
    assert await sys_db.permission(username, db_name, col_name_1) == 'ro'
    assert isinstance(await col_1.properties(), dict)
    with assert_raises(DocumentInsertError) as err:
        await col_1.insert({})
    assert err.value.http_code == 403
    assert isinstance(await col_2.properties(), dict)
    assert isinstance(await col_2.insert({}), dict)

    # Test update permission (collection level) to none and verify access
    assert await sys_db.update_permission(username, 'none', db_name, col_name_1)
    assert await sys_db.permission(username, db_name, col_name_1) == 'none'
    with assert_raises(CollectionPropertiesError) as err:
        await col_1.properties()
    assert err.value.http_code == 403
    with assert_raises(DocumentInsertError) as err:
        await col_1.insert({})
    assert err.value.http_code == 403
    assert isinstance(await col_2.properties(), dict)
    assert isinstance(await col_2.insert({}), dict)

    # Test reset permission (collection level)
    assert await sys_db.reset_permission(username, db_name, col_name_1) is True
    assert await sys_db.permission(username, db_name, col_name_1) == 'rw'
    assert isinstance(await col_1.properties(), dict)
    assert isinstance(await col_1.insert({}), dict)
    assert isinstance(await col_2.properties(), dict)
    assert isinstance(await col_2.insert({}), dict)
