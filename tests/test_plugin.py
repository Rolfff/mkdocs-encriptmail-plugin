import os
import shutil
import logging
import contextlib
import pathlib
from click.testing import CliRunner
from mkdocs.__main__ import build_command


@contextlib.contextmanager
def cd(path):
    """
    Credits
    https://stackoverflow.com/a/24469659/5525118

    Args:
        path (str): path or pathlib
    """
    old_path = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(old_path)


def build_docs_setup(testproject_path):
    """
    Runs the `mkdocs build` command
    
    Args:
        testproject_path (Path): Path to test project
    
    Returns:
        command: Object with results of command
    """
    with cd(testproject_path):
        return CliRunner().invoke(build_command)


def setup_clean_mkdocs_folder(mkdocs_yml_path, output_path):
    """
    Sets up a clean mkdocs directory
    
    outputpath/testproject
    ├── docs/
    └── mkdocs.yml
    
    Args:
        mkdocs_yml_path (Path): Path of mkdocs.yml file to use
        output_path (Path): Path of folder in which to create mkdocs project
        
    Returns:
        testproject_path (Path): Path to test project
    """
    output_path = str(output_path)
    testproject_path = os.path.join(output_path, "testproject")

    # Create empty 'testproject' folder
    if os.path.exists(testproject_path):
        logging.warning(
            """This command does not work on windows. 
        Refactor your test to use setup_clean_mkdocs_folder() only once"""
        )
        shutil.rmtree(testproject_path)

    # Copy mkdocs.yml file and our test 'docs/'
    shutil.copytree(
        os.path.join(os.path.dirname(mkdocs_yml_path), "docs"),
        os.path.join(testproject_path, "docs"),
    )
    shutil.copyfile(mkdocs_yml_path, os.path.join(testproject_path, "mkdocs.yml"))

    return testproject_path


def test_encriptMail_output(tmp_path):

    tmp_proj = setup_clean_mkdocs_folder("tests/fixtures/mkdocs.yml", tmp_path)

    result = build_docs_setup(tmp_proj)
    assert result.exit_code == 0, "'mkdocs build' command failed"

    index_file = os.path.join(tmp_proj, "site/index.html")
    assert os.path.exists(index_file), "%s does not exist" % index_file

    contents = pathlib.Path(index_file).read_text()
#    assert '<a href="javascript:linkTo_UnCryptMailto(%27ocknvq,vguvBvguv0vguv%27)">Email-Link</a>' in contents

#    assert '<a href="javascript:linkTo_UnCryptMailto(%27ocknvq,vguv4Bvguv0vguv%27)">test2(Q)test(P)test</a>' in contents

#    assert "test3@test.test" in contents


    #mailto:abcd@example.com
    assert "javascript:linkTo_UnCryptMailto(%27ocknvq,cdefBgzcorng0eqo%27)" in contents

    #mailto:abc@example.com
    assert "javascript:linkTo_UnCryptMailto(%27ocknvq,cdeBgzcorng0eqo%27)" in contents

    #mailto:abcd@example.co_m
    assert "javascript:linkTo_UnCryptMailto(%27ocknvq,cdefBgzcorng0eq_o%27)" in contents

    #mailto:ab-cd@exa-mple.com
    assert "javascript:linkTo_UnCryptMailto(%27ocknvq,cd/efBgzc/orng0eqo%27)" in contents

    assert "abcd(Q)example(P)com<" in contents
