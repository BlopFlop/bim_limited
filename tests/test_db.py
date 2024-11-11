try:
    from src.core.config import BASE_DIR
except (NameError, ImportError) as error:
    raise AssertionError(
        "При импорте BASE_DIR из модуля "
        "`src.core.config` возникло исключение:\n"
        f"{type(error).__name__}: {error}."
    )


def test_check_migration_file_exist():
    """Check exists migration files."""
    app_dirs = [d.name for d in BASE_DIR.iterdir()]
    assert (
        "alembic" in app_dirs
    ), "В корневой директории не обнаружена папка `alembic`."
    alembic_dir = BASE_DIR / "alembic"
    version_dir = [d.name for d in alembic_dir.iterdir()]
    assert (
        "versions" in version_dir
    ), "В папке `alembic` не обнаружена папка `versions`"
    versions_dir = alembic_dir / "versions"
    files_in_version_dir = [
        f.name
        for f in versions_dir.iterdir()
        if f.is_file() and f.name != "__init__.py"
    ]
    assert (
        len(files_in_version_dir) > 0
    ), "В папке `alembic.versions` не обнаружены файлы миграций"
