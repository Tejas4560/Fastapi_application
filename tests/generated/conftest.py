"""
pytest configuration for AI-generated tests.
Framework-specific setup with minimal dependencies.
"""

import os
import sys
import pytest
import warnings

# Suppress deprecation warnings during testing
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=PendingDeprecationWarning)

# Set testing environment
os.environ.setdefault("TESTING", "true")
os.environ.setdefault("LOG_LEVEL", "ERROR")

# Add target project to Python path
TARGET_ROOT = os.environ.get("TARGET_ROOT", "/home/runner/work/Fastapi_application/Fastapi_application/pipeline/target_repo")
if TARGET_ROOT and TARGET_ROOT not in sys.path:
    sys.path.insert(0, TARGET_ROOT)

# Also add current directory
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


# ============== FASTAPI-SPECIFIC CONFIGURATION ==============

import asyncio

# Try to import the FastAPI app
_fastapi_app = None
try:
    for module_name in ['main', 'app', 'api', 'server', 'application']:
        try:
            mod = __import__(module_name)
            if hasattr(mod, 'app'):
                _fastapi_app = mod.app
                break
            elif hasattr(mod, 'create_app'):
                _fastapi_app = mod.create_app()
                break
        except ImportError:
            continue
except Exception:
    pass


@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def app():
    """FastAPI application fixture."""
    if _fastapi_app is None:
        pytest.skip("No FastAPI app found")
    return _fastapi_app


@pytest.fixture
def client(app):
    """FastAPI TestClient fixture."""
    try:
        from fastapi.testclient import TestClient
        return TestClient(app)
    except ImportError:
        from starlette.testclient import TestClient
        return TestClient(app)


@pytest.fixture
def async_client(app):
    """Async client for FastAPI."""
    try:
        from httpx import AsyncClient
        return AsyncClient(app=app, base_url="http://test")
    except ImportError:
        pytest.skip("httpx not installed for async testing")


@pytest.fixture
def sample_data():
    """Sample test data for FastAPI apps."""
    return {
        "title": "Test Item",
        "description": "Test Description",
        "name": "Test Name",
        "email": "test@example.com",
        "username": "testuser",
        "password": "testpass123",
        "is_active": True,
    }


@pytest.fixture
def auth_headers():
    """Authorization headers for API testing."""
    return {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": "Bearer test-token",
    }


@pytest.fixture
def mock_db():
    """Mock database for testing without real DB."""
    return {}


@pytest.fixture
def override_dependencies(app):
    """
    Override FastAPI dependencies for testing.

    Usage:
        def test_with_mock_db(client, override_dependencies):
            # Dependencies are overridden for this test
            pass

    To override specific dependencies:
        app.dependency_overrides[get_db] = lambda: mock_db
    """
    original_overrides = app.dependency_overrides.copy()
    yield app.dependency_overrides
    # Restore original dependencies after test
    app.dependency_overrides.clear()
    app.dependency_overrides.update(original_overrides)


@pytest.fixture(autouse=True)
def reset_dependency_overrides(app):
    """Auto-reset dependency overrides after each test."""
    yield
    app.dependency_overrides.clear()


# UNIVERSAL fixtures for any project structure
import sys
import os
import pathlib  # needed for _setup_detected_frameworks()

# Add project root to Python path for universal imports
PROJECT_ROOT = r"/home/runner/work/Fastapi_application/Fastapi_application/pipeline/target_repo"
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

@pytest.fixture(scope="session", autouse=True)
def universal_coverage_setup():
    """UNIVERSAL setup for maximum coverage with real code execution."""
    # Set coverage optimization environment
    os.environ['COVERAGE_OPTIMIZATION'] = 'universal'
    os.environ['REAL_IMPORTS_ONLY'] = 'true'
    os.environ['TESTING_MAX_COVERAGE'] = 'true'
    
    # Universal framework auto-detection
    _setup_detected_frameworks()
    
    yield
    
    # Cleanup
    os.environ.pop('COVERAGE_OPTIMIZATION', None)
    os.environ.pop('REAL_IMPORTS_ONLY', None)

def _setup_detected_frameworks():
    """Auto-detect and setup frameworks for any project structure."""
    # Try to detect and import common project modules
    project_modules = ['app', 'main', 'application', 'server', 'api', 'backend', 'core', 'project']
    
    # Also try to detect project-specific modules from the structure
    try:
        # Look for Python files in project root to detect main modules
        for py_file in pathlib.Path(PROJECT_ROOT).glob("*.py"):
            module_name = py_file.stem
            if module_name not in project_modules and not module_name.startswith('_'):
                project_modules.append(module_name)
    except Exception:
        pass
    
    for module_name in project_modules:
        try:
            __import__(module_name)
            print(f"Detected and imported: {module_name}")
        except ImportError:
            continue

@pytest.fixture
def universal_sample_data():
    """UNIVERSAL sample data for comprehensive testing."""
    return {
        'user': {
            'username': 'testuser_universal',
            'email': 'universal_test@example.com',
            'password': 'UniversalPassword123!',
        },
        'api_payloads': {
            'create_user': {
                'user': {
                    'username': 'api_test_user',
                    'email': 'api_test@example.com',
                    'password': 'ApiTestPass123!',
                }
            },
            'login': {
                'user': {
                    'email': 'api_test@example.com',
                    'password': 'ApiTestPass123!',
                }
            },
        },
        'edge_cases': {
            'empty_string': '',
            'none_value': None,
            'zero': 0,
            'negative': -1,
            'large_number': 999999999999,
            'special_chars': r'!@#$%^&*()_+-=[]{}|;:,.<>?/\~`',
            'unicode': '测试数据 🚀 émojis ñoños café ☕',
            'long_string': 'x' * 1000,
            'whitespace': '   ',
        }
    }

# UNIVERSAL test utilities
class UniversalTestUtils:
    """Universal utilities for achieving maximum coverage."""
    
    @staticmethod
    def setup_universal_imports():
        """Setup universal imports for any project structure."""
        print("UNIVERSAL: Setting up imports for any project structure")
    
    @staticmethod
    def generate_comprehensive_test_cases(target_name, target_type):
        """Generate comprehensive test cases for any target."""
        base_cases = [
            f"test_{target_name}_basic_functionality",
            f"test_{target_name}_edge_cases", 
            f"test_{target_name}_error_conditions",
            f"test_{target_name}_validation",
        ]
        
        if target_type in ['model', 'class']:
            base_cases.extend([
                f"test_{target_name}_creation",
                f"test_{target_name}_methods",
                f"test_{target_name}_properties",
            ])
        
        if target_type in ['api', 'route']:
            base_cases.extend([
                f"test_{target_name}_get",
                f"test_{target_name}_post", 
                f"test_{target_name}_put",
                f"test_{target_name}_delete",
            ])
        
        return base_cases
