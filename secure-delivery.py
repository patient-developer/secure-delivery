import os
import sys

import click

from app import create_app

COVERAGE = None
if os.getenv('FLASK_COVERAGE'):
    import coverage

    COVERAGE = coverage.coverage(branch=True, include='app/*')
    COVERAGE.start()

app = create_app(os.getenv('FLASK_CONFIG') or 'default')


@app.cli.command()
@click.option('--coverage/--no-coverage', default=False, help='Run tests under code coverage')
def test(coverage):
    """Run the unit tests"""
    if coverage and not os.getenv('FLASK_COVERAGE'):
        os.environ['FLASK_COVERAGE'] = '1'
        os.execvp(sys.executable, [sys.executable] + sys.argv)
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    if COVERAGE:
        COVERAGE.stop()
        COVERAGE.save()
        print('Coverage summary:')
        COVERAGE.report()
        base_dir = os.path.abspath(os.path.dirname(__file__))
        coverage_dir = os.path.join(base_dir, 'coverage')
        COVERAGE.html_report(directory=coverage_dir)
        print('HTML version: file://%s/index.html' % coverage_dir)
        COVERAGE.erase()
