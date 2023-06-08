import os
import pathlib

import pandas as pd
from tqdm import tqdm
from vedo import Spline

import evoflow
from evoflow import Job, logger
from evoflow.Entities.Global import Global
from evoflow.pycatia.hybrid_shape_interfaces.hybrid_shape_curve_explicit import HybridShapeCurveExplicit
from evoflow.pycatia.mec_mod_interfaces.hybrid_shape import HybridShape


@evoflow.Step()
def hide_all():
    caa = Global().caa
    selection = caa.active_document.selection
    selection.clear()
    selection.search("type=*,all")
    selection.hide()
    selection.clear()


@evoflow.Step()
def export_splines(spline_names: list = None, resolution: int = None):
    """
    Export Splines ( Curve ) trong file CATIA đang mở
    :param resolution: độ phân giải của gieo điểm để export splines Ex: 1
    :param spline_names: Tên hiển thị trên cây thư mục. Ex: Curve.319 dùng để export
    :return:
    """

    caa = Global().caa
    document = caa.active_document
    selection = caa.active_document.selection
    selection.clear()
    hybrid_shape_factory = document.part().hybrid_shape_factory
    if spline_names is not None:
        z = [f"Name='{spline_name}'" for spline_name in spline_names]
        search_query = ' + '.join(z)
        search_query = f'({search_query}),all'
    else:
        # Search all curve
        search_query = "((((((FreeStyle.Curve + '2D Layout for 3D Design'.Curve) + Sketcher.Curve) + Drafting.Curve) + 'Part Design'.Curve) + 'Generative Shape Design'.Curve) + 'Functional Molded Part'.Curve),all"
    selection.search(search_query)
    selected_items = selection.items()
    logger.info(f"Found {len(selected_items)} Splines")
    spa_workbench = document.spa_workbench()

    spline_points = {}

    evoflow_part = caa.active_document.create_hybrid('evoflow')

    for spline in selected_items:
        spline = HybridShapeCurveExplicit(spline.com_object)
        spline_points[spline.get_path()] = []
        resolution = resolution or os.getenv('CURVE_RESOLUTION') or input(
            'Enter curve resolution to export (mm)-  Default = 10:') or 10
        resolution = int(resolution)

        points = spline.add_points_on_curve(distance=resolution, hybrid_shape_factory=hybrid_shape_factory)

        evoflow_part.append_hybrid_shapes(points)
        evoflow_part.update()
        spline.show(show_all_parent=True)
        for point_on_curve in tqdm(points, desc=f'Export Curve {spline.name}'):
            mesureable = point_on_curve.get_measurable(workbench=spa_workbench)
            x, y, z = mesureable.get_point()
            spline_points[spline.get_path()].append([x, y, z])
        spline.hide()

    splines = []
    for name, points in spline_points.items():
        try:
            spline = Spline(points)
        except:
            logger.info(f"Can't export spline: {name}, try to add more points")
            continue
        splines.append(spline)
        output_name = f"{os.getenv('DATA_PATH')}/{name}.vtk"
        output_dir = os.path.split(output_name)[0]
        pathlib.Path(output_dir).mkdir(exist_ok=True, parents=True)
        spline.write(output_name)
    evoflow_part.delete()
    caa.start_command('clear history')
    return {'splines': splines}


@evoflow.Step()
def export_surface_to_stl():
    mesh_path = os.getenv('DATA_PATH') or input('Enter mesh path: ') or '.'

    caa = Global().caa
    document_name = '.'.join(caa.active_document.name.split('.')[:-1])
    mesh_path = os.path.abspath(mesh_path)
    show_only_part_name = os.getenv('EXPORT_PART_NAME') or input('Enter RIB part name: ')
    selection = caa.active_document.selection
    selection.search(f"Name='{show_only_part_name}',all")
    visible_items = selection.items()
    wb = caa.active_document.spa_workbench()
    for item in visible_items:
        item.show(show_all_parent=True)

    selection.search(f"Name={show_only_part_name},all")
    selection.search("type=*,sel")
    rib_items = selection.items()
    progress_bar = tqdm(rib_items, desc='Export RIB to STL')
    for rib_item in progress_bar:
        try:
            shape = HybridShape(rib_item.com_object)
            shape.compute()
        except AttributeError as abe:
            continue

        progress_bar.set_description(f'Export {rib_item.name} to STL')
        measurable = shape.get_measurable(workbench=wb)
        try:
            area = measurable.area
        except:
            continue
        shape.show(show_all_parent=True)
        path = shape.get_path()
        file_name = f"{mesh_path}/{path}.stl"
        file_name = os.path.abspath(file_name)
        caa.active_document.export_data(file_name, file_type='stl', overwrite=True)
        rib_item.hide()
    logger.info(f'Found {selection.count} items in {show_only_part_name}')

    return {'mesh_path': mesh_path}


@evoflow.Step()
def catia_to_evoflow():
    start_step = hide_all()
    x = start_step.next(export_surface_to_stl())
    x = x.next(export_splines())

    job = Job(name='Export All data from CATIA', start_step=start_step)
    job.run()
    return job.params_pool


@evoflow.Step()
def get_die_direction():
    caa = Global().caa
    document = caa.active_document
    selection = document.selection
    selection.clear()
    evoflow_exported_path = os.getenv('DATA_PATH') or input('Enter exported path: ')
    die_direction_name = os.getenv('DIE_DIRECTION_NAME') or input('Enter Die direction name: ')
    selection.search(f"Name={die_direction_name},all")
    items = selection.items()
    x, y, z = None, None, None
    for die_vector in items:
        try:
            die_vector = HybridShape(die_vector.com_object)
            logger.info(f'Found die direction items: {die_vector.get_path()}')
            x, y, z = die_vector.get_measurable().get_direction()
            px, py, pz = die_vector.get_measurable().get_points_on_curve()[:3]
        except Exception as e:
            logger.error(e)

    logger.info(f"get diecrion: {x, y, z}")
    if x is None:
        raise Exception("Can't find die direction object")

    df = pd.DataFrame(
        data={'die_angle_x': [x], 'die_angle_y': [y], 'die_angle_z': [z], 'px': [px], 'py': [py], 'pz': [pz]})

    pathlib.Path(evoflow_exported_path).mkdir(exist_ok=True)
    df.to_excel(f'{evoflow_exported_path}/dieangle.xlsx', index=False)

    return {'die_angle_x': x, 'die_angle_y': y, 'die_angle_z': z, 'px': px, 'py': py, 'pz': pz}


if __name__ == '__main__':
    job = Job(
        start_step=export_splines(spline_names=['Curve.282'])
    )
    job.run()
