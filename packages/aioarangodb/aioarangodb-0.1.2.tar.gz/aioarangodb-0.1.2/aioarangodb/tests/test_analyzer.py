from __future__ import absolute_import, unicode_literals
import pytest

from aioarangodb.exceptions import (
    AnalyzerCreateError,
    AnalyzerDeleteError,
    AnalyzerGetError,
    AnalyzerListError
)
from aioarangodb.tests.helpers import assert_raises, generate_analyzer_name


@pytest.mark.asyncio
async def test_analyzer_management(db, bad_db, cluster):
    analyzer_name = generate_analyzer_name()
    full_analyzer_name = db.name + '::' + analyzer_name
    bad_analyzer_name = generate_analyzer_name()

    # Test create analyzer
    result = await db.create_analyzer(analyzer_name, 'identity', {})
    assert result['name'] == full_analyzer_name
    assert result['type'] == 'identity'
    assert result['properties'] == {}
    assert result['features'] == []

    # Test create duplicate with bad database
    with assert_raises(AnalyzerCreateError) as err:
        await bad_db.create_analyzer(analyzer_name, 'identity', {}, [])
    assert err.value.error_code in {11, 1228}

    # Test get analyzer
    result = await db.analyzer(analyzer_name)
    assert result['name'] == full_analyzer_name
    assert result['type'] == 'identity'
    assert result['properties'] == {}
    assert result['features'] == []

    # Test get missing analyzer
    with assert_raises(AnalyzerGetError) as err:
        await db.analyzer(bad_analyzer_name)
    assert err.value.error_code in {1202}

    # Test list analyzers
    result = await db.analyzers()
    assert full_analyzer_name in [a['name'] for a in result]

    # Test list analyzers with bad database
    with assert_raises(AnalyzerListError) as err:
        await bad_db.analyzers()
    assert err.value.error_code in {11, 1228}

    # Test delete analyzer
    assert await db.delete_analyzer(analyzer_name, force=True) is True
    assert full_analyzer_name not in [a['name'] for a in await db.analyzers()]

    # Test delete missing analyzer
    with assert_raises(AnalyzerDeleteError) as err:
        await db.delete_analyzer(analyzer_name)
    assert err.value.error_code in {1202}

    # Test delete missing analyzer with ignore_missing set to True
    assert await db.delete_analyzer(analyzer_name, ignore_missing=True) is False
