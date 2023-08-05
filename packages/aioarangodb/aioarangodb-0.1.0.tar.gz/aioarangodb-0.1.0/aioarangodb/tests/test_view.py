from __future__ import absolute_import, unicode_literals
import pytest

from aioarangodb.exceptions import (
    ViewCreateError,
    ViewDeleteError,
    ViewGetError,
    ViewListError,
    ViewRenameError,
    ViewReplaceError,
    ViewUpdateError
)
from aioarangodb.tests.helpers import assert_raises, generate_view_name
pytestmark = pytest.mark.asyncio


async def test_view_management(db, bad_db, cluster):
    # Test create view
    view_name = generate_view_name()
    bad_view_name = generate_view_name()
    view_type = 'arangosearch'

    result = await db.create_view(
        view_name,
        view_type,
        {'consolidationIntervalMsec': 50000}
    )
    assert 'id' in result
    assert result['name'] == view_name
    assert result['type'] == view_type
    assert result['consolidation_interval_msec'] == 50000
    view_id = result['id']

    # Test create duplicate view
    with assert_raises(ViewCreateError) as err:
        await db.create_view(
            view_name,
            view_type,
            {'consolidationIntervalMsec': 50000}
        )
    assert err.value.error_code == 1207

    # Test list views
    result = await db.views()
    assert len(result) == 1
    view = result[0]
    assert view['id'] == view_id
    assert view['name'] == view_name
    assert view['type'] == view_type

    # Test list views with bad database
    with assert_raises(ViewListError) as err:
        await bad_db.views()
    assert err.value.error_code in {11, 1228}

    # Test get view
    view = await db.view(view_name)
    assert view['id'] == view_id
    assert view['name'] == view_name
    assert view['type'] == view_type
    assert view['consolidation_interval_msec'] == 50000

    # Test get missing view
    with assert_raises(ViewGetError) as err:
        await db.view(bad_view_name)
    assert err.value.error_code == 1203

    # Test update view
    view = await db.update_view(view_name, {'consolidationIntervalMsec': 70000})
    assert view['id'] == view_id
    assert view['name'] == view_name
    assert view['type'] == view_type
    assert view['consolidation_interval_msec'] == 70000

    # Test update view with bad database
    with assert_raises(ViewUpdateError) as err:
        await bad_db.update_view(view_name, {'consolidationIntervalMsec': 80000})
    assert err.value.error_code in {11, 1228}

    # Test replace view
    view = await db.replace_view(view_name, {'consolidationIntervalMsec': 40000})
    assert view['id'] == view_id
    assert view['name'] == view_name
    assert view['type'] == view_type
    assert view['consolidation_interval_msec'] == 40000

    # Test replace view with bad database
    with assert_raises(ViewReplaceError) as err:
        await bad_db.replace_view(view_name, {'consolidationIntervalMsec': 7000})
    assert err.value.error_code in {11, 1228}

    if cluster:
        new_view_name = view_name
    else:
        # Test rename view
        new_view_name = generate_view_name()
        assert await db.rename_view(view_name, new_view_name) is True
        result = await db.views()
        assert len(result) == 1
        view = result[0]
        assert view['id'] == view_id
        assert view['name'] == new_view_name

        # Test rename missing view
        with assert_raises(ViewRenameError) as err:
            await db.rename_view(bad_view_name, view_name)
        assert err.value.error_code == 1203

    # Test delete view
    assert await db.delete_view(new_view_name) is True
    assert len(await db.views()) == 0

    # Test delete missing view
    with assert_raises(ViewDeleteError) as err:
        await db.delete_view(new_view_name)
    assert err.value.error_code == 1203

    # Test delete missing view with ignore_missing set to True
    assert await db.delete_view(view_name, ignore_missing=True) is False


async def test_arangosearch_view_management(db, bad_db, cluster):
    # Test create arangosearch view
    view_name = generate_view_name()
    result = await db.create_arangosearch_view(
        view_name,
        {'consolidationIntervalMsec': 50000}
    )
    assert 'id' in result
    assert result['name'] == view_name
    assert result['type'].lower() == 'arangosearch'
    assert result['consolidation_interval_msec'] == 50000
    view_id = result['id']

    # Test create duplicate arangosearch view
    with assert_raises(ViewCreateError) as err:
        await db.create_arangosearch_view(
            view_name,
            {'consolidationIntervalMsec': 50000}
        )
    assert err.value.error_code == 1207

    result = await db.views()
    if not cluster:
        assert len(result) == 1
        view = result[0]
        assert view['id'] == view_id
        assert view['name'] == view_name
        assert view['type'] == 'arangosearch'

    # Test update arangosearch view
    view = await db.update_arangosearch_view(
        view_name,
        {'consolidationIntervalMsec': 70000}
    )
    assert view['id'] == view_id
    assert view['name'] == view_name
    assert view['type'].lower() == 'arangosearch'
    assert view['consolidation_interval_msec'] == 70000

    # Test update arangosearch view with bad database
    with assert_raises(ViewUpdateError) as err:
        await bad_db.update_arangosearch_view(
            view_name,
            {'consolidationIntervalMsec': 70000}
        )
    assert err.value.error_code in {11, 1228}

    # Test replace arangosearch view
    view = await db.replace_arangosearch_view(
        view_name,
        {'consolidationIntervalMsec': 40000}
    )
    assert view['id'] == view_id
    assert view['name'] == view_name
    assert view['type'] == 'arangosearch'
    assert view['consolidation_interval_msec'] == 40000

    # Test replace arangosearch with bad database
    with assert_raises(ViewReplaceError) as err:
        await bad_db.replace_arangosearch_view(
            view_name,
            {'consolidationIntervalMsec': 70000}
        )
    assert err.value.error_code in {11, 1228}

    # Test delete arangosearch view
    assert await db.delete_view(view_name, ignore_missing=False) is True
