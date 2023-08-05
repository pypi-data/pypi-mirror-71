from __future__ import absolute_import, unicode_literals
import pytest
from aioarangodb.exceptions import (
    AQLCacheClearError,
    AQLCacheConfigureError,
    AQLCacheEntriesError,
    AQLCachePropertiesError,
    AQLFunctionCreateError,
    AQLFunctionDeleteError,
    AQLFunctionListError,
    AQLQueryClearError,
    AQLQueryExecuteError,
    AQLQueryExplainError,
    AQLQueryListError,
    AQLQueryTrackingGetError,
    AQLQueryTrackingSetError,
    AQLQueryKillError,
    AQLQueryValidateError
)
from aioarangodb.tests.helpers import assert_raises, extract
pytestmark = pytest.mark.asyncio


async def test_aql_attributes(db, username):
    assert db.context in ['default', 'async', 'batch', 'transaction']
    assert db.username == username
    assert db.db_name == db.name
    assert repr(db.aql) == '<AQL in {}>'.format(db.name)
    assert repr(db.aql.cache) == '<AQLQueryCache in {}>'.format(db.name)


async def test_aql_query_management(db, bad_db, col, docs):
    plan_fields = [
        'estimatedNrItems',
        'estimatedCost',
        'rules',
        'variables',
        'collections',
    ]
    # Test explain invalid query
    with assert_raises(AQLQueryExplainError) as err:
        await db.aql.explain('INVALID QUERY')
    assert err.value.error_code == 1501

    # Test explain valid query with all_plans set to False
    plan = await db.aql.explain(
        'FOR d IN {} RETURN d'.format(col.name),
        all_plans=False,
        opt_rules=['-all', '+use-index-range']
    )
    assert all(field in plan for field in plan_fields)

    # Test explain valid query with all_plans set to True
    plans = await db.aql.explain(
        'FOR d IN {} RETURN d'.format(col.name),
        all_plans=True,
        opt_rules=['-all', '+use-index-range'],
        max_plans=10
    )
    for plan in plans:
        assert all(field in plan for field in plan_fields)
    assert len(plans) < 10

    # Test validate invalid query
    with assert_raises(AQLQueryValidateError) as err:
        await db.aql.validate('INVALID QUERY')
    assert err.value.error_code == 1501

    # Test validate valid query
    result = await db.aql.validate('FOR d IN {} RETURN d'.format(col.name))
    assert 'ast' in result
    assert 'bind_vars' in result
    assert 'collections' in result
    assert 'parsed' in result

    # Test execute invalid AQL query
    with assert_raises(AQLQueryExecuteError) as err:
        await db.aql.execute('INVALID QUERY')
    assert err.value.error_code == 1501

    # Test execute valid query
    await db.collection(col.name).import_bulk(docs)
    cursor = await db.aql.execute(
        '''
        FOR d IN {col}
            UPDATE {{_key: d._key, _val: @val }} IN {col}
            RETURN NEW
        '''.format(col=col.name),
        count=True,
        # batch_size=1,
        ttl=10,
        bind_vars={'val': 42},
        full_count=True,
        max_plans=1000,
        optimizer_rules=['+all'],
        cache=True,
        memory_limit=1000000,
        fail_on_warning=False,
        profile=True,
        max_transaction_size=100000,
        max_warning_count=10,
        intermediate_commit_count=1,
        intermediate_commit_size=1000,
        satellite_sync_wait=False,
        write_collections=[col.name],
        read_collections=[col.name],
        stream=False,
        skip_inaccessible_cols=True,
        max_runtime=0.0
    )
    assert cursor.id is None
    assert cursor.type == 'cursor'
    assert cursor.batch() is not None
    assert cursor.has_more() is False
    assert cursor.count() == await col.count()
    assert cursor.cached() is False
    assert cursor.statistics() is not None
    assert cursor.profile() is not None
    assert cursor.warnings() == []
    assert await extract('_key', cursor) == await extract('_key', docs)
    assert await cursor.close(ignore_missing=True) is None

    # Test get tracking properties with bad database
    with assert_raises(AQLQueryTrackingGetError) as err:
        await bad_db.aql.tracking()
    assert err.value.error_code in {11, 1228}

    # Test get tracking properties
    tracking = await db.aql.tracking()
    assert isinstance(tracking['enabled'], bool)
    assert isinstance(tracking['max_query_string_length'], int)
    assert isinstance(tracking['max_slow_queries'], int)
    assert isinstance(tracking['slow_query_threshold'], int)
    assert isinstance(tracking['track_bind_vars'], bool)
    assert isinstance(tracking['track_slow_queries'], bool)

    # Test set tracking properties with bad database
    with assert_raises(AQLQueryTrackingSetError) as err:
        await bad_db.aql.set_tracking(enabled=not tracking['enabled'])
    assert err.value.error_code in {11, 1228}
    assert (await db.aql.tracking())['enabled'] == tracking['enabled']

    # Test set tracking properties
    new_tracking = await db.aql.set_tracking(
        enabled=not tracking['enabled'],
        max_query_string_length=4000,
        max_slow_queries=60,
        slow_query_threshold=15,
        track_bind_vars=not tracking['track_bind_vars'],
        track_slow_queries=not tracking['track_slow_queries']
    )
    assert new_tracking['enabled'] != tracking['enabled']
    assert new_tracking['max_query_string_length'] == 4000
    assert new_tracking['max_slow_queries'] == 60
    assert new_tracking['slow_query_threshold'] == 15
    assert new_tracking['track_bind_vars'] != tracking['track_bind_vars']
    assert new_tracking['track_slow_queries'] != tracking['track_slow_queries']

    # Make sure to revert the properties
    new_tracking = await db.aql.set_tracking(
        enabled=True,
        track_bind_vars=True,
        track_slow_queries=True
    )
    assert new_tracking['enabled'] is True
    assert new_tracking['track_bind_vars'] is True
    assert new_tracking['track_slow_queries'] is True

    # Kick off some long lasting queries in the background
    await db.begin_async_execution().aql.execute('RETURN SLEEP(100)')
    await db.begin_async_execution().aql.execute('RETURN SLEEP(50)')

    # Test list queries
    queries = await db.aql.queries()
    for query in queries:
        assert 'id' in query
        assert 'query' in query
        assert 'started' in query
        assert 'state' in query
        assert 'bind_vars' in query
        assert 'runtime' in query
    assert len(queries) == 2

    # Test list queries with bad database
    with assert_raises(AQLQueryListError) as err:
        await bad_db.aql.queries()
    assert err.value.error_code in {11, 1228}

    # Test kill queries
    query_id_1, query_id_2 = await extract('id', queries)
    assert await db.aql.kill(query_id_1) is True

    while len(queries) > 1:
        queries = await db.aql.queries()
    assert query_id_1 not in await extract('id', queries)

    assert await db.aql.kill(query_id_2) is True
    while len(queries) > 0:
        queries = await db.aql.queries()
    assert query_id_2 not in await extract('id', queries)

    # Test kill missing queries
    with assert_raises(AQLQueryKillError) as err:
        await db.aql.kill(query_id_1)
    assert err.value.error_code == 1591
    with assert_raises(AQLQueryKillError) as err:
        await db.aql.kill(query_id_2)
    assert err.value.error_code == 1591

    # Test list slow queries
    assert await db.aql.slow_queries() == []

    # Test list slow queries with bad database
    with assert_raises(AQLQueryListError) as err:
        await bad_db.aql.slow_queries()
    assert err.value.error_code in {11, 1228}

    # Test clear slow queries
    assert await db.aql.clear_slow_queries() is True

    # Test clear slow queries with bad database
    with assert_raises(AQLQueryClearError) as err:
        await bad_db.aql.clear_slow_queries()
    assert err.value.error_code in {11, 1228}


async def test_aql_function_management(db, bad_db):
    fn_group = 'functions::temperature'
    fn_name_1 = 'functions::temperature::celsius_to_fahrenheit'
    fn_body_1 = 'function (celsius) { return celsius * 1.8 + 32; }'
    fn_name_2 = 'functions::temperature::fahrenheit_to_celsius'
    fn_body_2 = 'function (fahrenheit) { return (fahrenheit - 32) / 1.8; }'
    bad_fn_name = 'functions::temperature::should_not_exist'
    bad_fn_body = 'function (celsius) { invalid syntax }'

    # Test list AQL functions
    assert await db.aql.functions() == []

    # Test list AQL functions with bad database
    with assert_raises(AQLFunctionListError) as err:
        await bad_db.aql.functions()
    assert err.value.error_code in {11, 1228}

    # Test create invalid AQL function
    with assert_raises(AQLFunctionCreateError) as err:
        await db.aql.create_function(bad_fn_name, bad_fn_body)
    assert err.value.error_code == 1581

    # Test create AQL function one
    assert await db.aql.create_function(fn_name_1, fn_body_1) == {'is_new': True}
    functions = await db.aql.functions()
    assert len(functions) == 1
    assert functions[0]['name'] == fn_name_1
    assert functions[0]['code'] == fn_body_1
    assert 'is_deterministic' in functions[0]

    # Test create AQL function one again (idempotency)
    assert await db.aql.create_function(fn_name_1, fn_body_1) == {'is_new': False}
    functions = await db.aql.functions()
    assert len(functions) == 1
    assert functions[0]['name'] == fn_name_1
    assert functions[0]['code'] == fn_body_1
    assert 'is_deterministic' in functions[0]

    # Test create AQL function two
    assert await db.aql.create_function(fn_name_2, fn_body_2) == {'is_new': True}
    functions = sorted(await db.aql.functions(), key=lambda x: x['name'])
    assert len(functions) == 2
    assert functions[0]['name'] == fn_name_1
    assert functions[0]['code'] == fn_body_1
    assert functions[1]['name'] == fn_name_2
    assert functions[1]['code'] == fn_body_2
    assert 'is_deterministic' in functions[0]
    assert 'is_deterministic' in functions[1]

    # Test delete AQL function one
    assert await db.aql.delete_function(fn_name_1) == {'deleted': 1}
    functions = await db.aql.functions()
    assert len(functions) == 1
    assert functions[0]['name'] == fn_name_2
    assert functions[0]['code'] == fn_body_2

    # Test delete missing AQL function
    with assert_raises(AQLFunctionDeleteError) as err:
        await db.aql.delete_function(fn_name_1)
    assert err.value.error_code == 1582
    assert await db.aql.delete_function(fn_name_1, ignore_missing=True) is False
    functions = await db.aql.functions()
    assert len(functions) == 1
    assert functions[0]['name'] == fn_name_2
    assert functions[0]['code'] == fn_body_2

    # Test delete AQL function group
    assert await db.aql.delete_function(fn_group, group=True) == {'deleted': 1}
    assert await db.aql.functions() == []


async def test_aql_cache_management(db, bad_db):
    # Test get AQL cache properties
    properties = await db.aql.cache.properties()
    assert 'mode' in properties
    assert 'max_results' in properties
    assert 'max_results_size' in properties
    assert 'max_entry_size' in properties
    assert 'include_system' in properties

    # Test get AQL cache properties with bad database
    with assert_raises(AQLCachePropertiesError):
        await bad_db.aql.cache.properties()

    # Test get AQL cache configure properties
    properties = await db.aql.cache.configure(
        mode='on',
        max_results=100,
        max_results_size=10000,
        max_entry_size=10000,
        include_system=True
    )
    assert properties['mode'] == 'on'
    assert properties['max_results'] == 100
    assert properties['max_results_size'] == 10000
    assert properties['max_entry_size'] == 10000
    assert properties['include_system'] is True

    properties = await db.aql.cache.properties()
    assert properties['mode'] == 'on'
    assert properties['max_results'] == 100
    assert properties['max_results_size'] == 10000
    assert properties['max_entry_size'] == 10000
    assert properties['include_system'] is True

    # Test get AQL cache configure properties with bad database
    with assert_raises(AQLCacheConfigureError):
        await bad_db.aql.cache.configure(mode='on')

    # Test get AQL cache entries
    result = await db.aql.cache.entries()
    assert isinstance(result, list)

    # Test get AQL cache entries with bad database
    with assert_raises(AQLCacheEntriesError) as err:
        await bad_db.aql.cache.entries()
    assert err.value.error_code in {11, 1228}

    # Test get AQL cache clear
    result = await db.aql.cache.clear()
    assert isinstance(result, bool)

    # Test get AQL cache clear with bad database
    with assert_raises(AQLCacheClearError) as err:
        await bad_db.aql.cache.clear()
    assert err.value.error_code in {11, 1228}
