"""
Transforms and generates ROS template.
"""
import os
import logging
from pathlib import Path

import typer

from rostran.core import exceptions
from rostran.core.format import (SourceTemplateFormat, TargetTemplateFormat, GeneratorFileFormat,
                                 convert_template_to_file_format)

app = typer.Typer(help=__doc__)
SOURCE_TEMPLATE_FORMAT_DEFAULT = typer.Option(
    SourceTemplateFormat.Auto, help='Source template format')
TARGET_TEMPLATE_FORMAT_DEFAULT = typer.Option(
    TargetTemplateFormat.Auto, help='Target template format')


@app.command()
def transform(
        source_path: str,
        source_format: SourceTemplateFormat = SOURCE_TEMPLATE_FORMAT_DEFAULT,
        target_path: str = typer.Argument(None),
        target_format: TargetTemplateFormat = TARGET_TEMPLATE_FORMAT_DEFAULT):
    """
    Transform AWS CloudFormation/Terraform/Excel template to ROS template.

    SOURCE represents AWS CloudFormation/Terraform/Excel template file path which will be transformed from.
    If file extension is ".json/.yml/.yaml", it will be automatically regarded as AWS CloudFormation template.
    If file extension is ".xlsx", it will be automatically regarded as Excel template.

    TARGET represents ROS template file path which will be transformed to. If not supplied, "template.yml" will be used.
    """
    # handle source template
    if not Path(source_path).exists():
        raise exceptions.TemplateNotExist(path=source_path)

    if source_format == SourceTemplateFormat.Auto:
        if source_path.endswith('.xlsx'):
            source_format = SourceTemplateFormat.Excel
        elif source_path.endswith('.tf'):
            source_format = SourceTemplateFormat.Terraform
        elif source_path.endswith(('.json', '.yaml', '.yml')):
            source_format = SourceTemplateFormat.CloudFormation
        else:
            raise exceptions.TemplateNotSupport(path=source_path)

    # handle target template
    if not target_path:
        if target_format in (TargetTemplateFormat.Auto, TargetTemplateFormat.Yaml):
            target_path = 'template.yml'
            target_format = TargetTemplateFormat.Yaml
        else:
            target_path = 'template.json'
    elif target_format == TargetTemplateFormat.Auto:
        if target_path.endswith(('.yaml', '.yml')):
            target_format = TargetTemplateFormat.Yaml
        elif target_path.endswith('.json'):
            target_format = TargetTemplateFormat.Json
        else:
            raise exceptions.TemplateNotSupport(path=target_path)

    path = Path(target_path)
    if path.exists():
        raise exceptions.TemplateAlreadyExist(path=target_path)
    if not path.parent.exists():
        raise exceptions.PathNotExist(path=path.parent)

    # initialize template
    source_file_format = convert_template_to_file_format(
        source_format, source_path)

    if source_format == SourceTemplateFormat.Excel:
        from ..providers import ExcelTemplate
        template = ExcelTemplate.initialize(source_path, source_file_format)
    elif source_format == SourceTemplateFormat.Terraform:
        from ..providers import TerraformTemplate
        template = TerraformTemplate.initialize(
            source_path, source_file_format)
    elif source_format == SourceTemplateFormat.CloudFormation:
        from ..providers import CloudFormationTemplate
        template = CloudFormationTemplate.initialize(
            source_path, source_file_format)
    else:
        raise exceptions.TemplateNotSupport(path=source_path)

    # transform template
    ros_templates = template.transform()
    if not isinstance(ros_templates, list):
        ros_templates.save(target_path, target_format)
    elif len(ros_templates) == 1:
        ros_templates[0].save(target_path, target_format)
    else:
        for i, ros_template in enumerate(ros_templates):
            name_parts = os.path.splitext(target_path)
            path = f'{name_parts[0]}-{i}{name_parts[1]}'
            ros_template.save(path, target_format)


@app.command()
def generate(resource_type: str, file_format: GeneratorFileFormat = GeneratorFileFormat.Excel):
    """
    Generate specific resource template file by given resource type.
    """
    typer.echo(
        f'Generate "{resource_type}" to ROS template (Format: {file_format})')


def main():
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    try:
        typer.main.get_command(app)(prog_name='rostran')
    except exceptions.RosTranWarning as e:
        typer.secho(f'{e}', fg=typer.colors.YELLOW)
        typer.Exit(0)
    except exceptions.RosTranException as e:
        typer.secho(f'{e}', fg=typer.colors.RED)
        typer.Exit(1)
    except Exception as e:
        typer.secho(f'{e}', fg=typer.colors.RED)


if __name__ == '__main__':
    main()
