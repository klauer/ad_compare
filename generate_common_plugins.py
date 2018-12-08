import os
import pathlib
import pandas as pd
import git
from recordwhat.parsers.db_parsimonious import dbWalker, db_grammar
from recordwhat.parsers.st_cmd import load_records
from compare import versions, preprocess
from generate import get_version_string, get_version_tuple
import ophyd.areadetector.plugins
import all_plugins


def generate_pvlists():
    boot_path = lambda version: pathlib.Path(version) / 'iocBoot'
    potential_filenames = ['EXAMPLE_commonPlugins.cmd', 'commonPlugins.cmd']
    filenames = {version: boot_path(version) / fn
                 for version in versions
                 for fn in potential_filenames
                 if os.path.exists(boot_path(version) / fn)
                 }

    for version, fn in filenames.items():
        ad_root = fn.parent.parent.absolute()
        print()
        print(version, fn, f'(ad root {ad_root!r})')
        records = load_records(
            fn, start_path=ad_root / 'ADApp' / 'Db',
            fallback_db_paths=[ad_root / 'ADApp' / 'Db'],
            macros=dict(AREA_DETECTOR=ad_root,
                        P='prefix:', R='',
                        PREFIX='PREFIX:',
                        PORT='_PORT_',
                        XSIZE='_XSIZE_',
                        YSIZE='_YSIZE_',
                        XCENT='_XCENT_',
                        YCENT='_YCENT_',
                        XWIDTH='_XWIDTH_',
                        YWIDTH='_YWIDTH_',
                        NCHANS='1',
                        SSCAN='ignore',
                        ASYN='ignore',
                        CALC='ignore',
                        AUTOSAVE='ignore',
                        ALIVE='ignore',
                        DEVIOCSTATS='ignore',
                        ADCORE=ad_root,
                        ),
            preprocessor=preprocess,
            ignore_nonexisting=True)

        pvnames = list(records.keys())
        with open(pathlib.Path('pvlists') / f'{version}.txt', 'wt') as f:
            print('\n'.join(pv for pv in pvnames if '.' not in pv), file=f)

        with open(pathlib.Path('pvlists') / f'{version}_full.txt', 'wt') as f:
            for pvname, info in records.items():
                print(f'{pvname} {info}', file=f)


def generate_common_plugins(version):
    def get_suffix(record):
        record = record[len('prefix:'):]
        record = record[:record.index(':')]
        return record

    code = []
    with open(pathlib.Path('pvlists') / f'{version}.txt') as f:
        records = [record.strip() for record in f.readlines()]
        suffixes = {get_suffix(record) for record in records}

        ver_string = get_version_string(version)
        ver_tuple = get_version_tuple(version)

        code.append(f'class CommonPlugins_V{ver_string}(CommonPlugins, version={ver_tuple}):')
        for suffix in sorted(suffixes):
            clsname = suffix_to_class[suffix.rstrip('1234567890')]

            if hasattr(all_plugins, clsname):
                plugin_cls = getattr(all_plugins, clsname)
            else:
                available_names = [name for name in dir(all_plugins)
                                   if name.startswith(clsname)]
                print(clsname, available_names)
                plugin_cls = getattr(all_plugins, available_names[0])

            all_versions = plugin_cls._device_versions_
            clsversion = max(ver for ver in all_versions
                             if ver <= ver_tuple)
            print('versions', all_versions, clsversion)
            clsversion = ''.join(str(v) for v in clsversion)
            if clsversion == '191':
                clsversion = ''
            else:
                clsversion = f'_V{clsversion}'

            if clsname.startswith('Overlay'):
                if ver_tuple>= (3, 1):
                    clsname, clsversion = 'OverlayPlugin', '_V31'
                elif ver_tuple>= (2, 6):
                    clsname, clsversion = 'OverlayPlugin', '_V26'
                elif ver_tuple>= (2, 1):
                    clsname, clsversion = 'OverlayPlugin', '_V21'
                elif ver_tuple>= (2, 0):
                    clsname, clsversion = 'OverlayPlugin', '_V20'
                else:
                    clsname, clsversion = 'OverlayPlugin', ''

            code.append(f'    {suffix.lower()} = Cpt({clsname}{clsversion}, "{suffix}:")')

    return '\n'.join(code)


def check_coverage(cls):
    ...


suffix_to_class = {
    'Attr': 'AttributeNPlugin',
    'CB': 'CircularBuffPlugin',
    'Codec': 'CodecPlugin',
    'CC': 'ColorConvPlugin',
    'FFT': 'FFTPlugin',
    'HDF': 'HDF5Plugin',
    'Gather': 'GatherPlugin',
    'Image': 'ImagePlugin',
    'JPEG': 'JPEGPlugin',
    'Magick': 'MagickPlugin',
    'netCDF': 'NetCDFPlugin',
    'Nexus': 'NexusPlugin',
    'Over': 'Overlay',
    'Proc': 'ProcessPlugin',
    'Pva': 'PvaPlugin',
    'ROI': 'ROIPlugin',
    'ROIStat': 'ROIStatPlugin',
    'Scatter': 'ScatterPlugin',
    'Stats': 'StatsPlugin',
    'TIFF': 'TIFFPlugin',
    'Trans': 'TransformPlugin',
    }


with open('common_plugins.py', 'wt') as f:
    print('''\
from ophyd import (Device, Component as Cpt, DynamicDeviceComponent as DDC,
                   EpicsSignal, EpicsSignalRO)
from ophyd.areadetector.plugins import (
    PluginBase, Overlay, ColorConvPlugin, FilePlugin, HDF5Plugin, ImagePlugin,
    JPEGPlugin, MagickPlugin, NetCDFPlugin, NexusPlugin, OverlayPlugin,
    ProcessPlugin, ROIPlugin, StatsPlugin, TIFFPlugin, TransformPlugin)
from ophyd.areadetector import (ADBase, EpicsSignalWithRBV as SignalWithRBV, ad_group)
from all_plugins import *


class OverlayPlugin_V20(OverlayPlugin, PluginBase_V20, version=(2, 0)):
    overlay_1 = Cpt(Overlay, '1:')
    overlay_2 = Cpt(Overlay, '2:')
    overlay_3 = Cpt(Overlay, '3:')
    overlay_4 = Cpt(Overlay, '4:')
    overlay_5 = Cpt(Overlay, '5:')
    overlay_6 = Cpt(Overlay, '6:')
    overlay_7 = Cpt(Overlay, '7:')
    overlay_8 = Cpt(Overlay, '8:')


class OverlayPlugin_V21(OverlayPlugin, version=(2, 1)):
    overlay_1 = Cpt(Overlay_V21, '1:')
    overlay_2 = Cpt(Overlay_V21, '2:')
    overlay_3 = Cpt(Overlay_V21, '3:')
    overlay_4 = Cpt(Overlay_V21, '4:')
    overlay_5 = Cpt(Overlay_V21, '5:')
    overlay_6 = Cpt(Overlay_V21, '6:')
    overlay_7 = Cpt(Overlay_V21, '7:')
    overlay_8 = Cpt(Overlay_V21, '8:')


class OverlayPlugin_V26(OverlayPlugin, version=(2, 1)):
    overlay_1 = Cpt(Overlay_V26, '1:')
    overlay_2 = Cpt(Overlay_V26, '2:')
    overlay_3 = Cpt(Overlay_V26, '3:')
    overlay_4 = Cpt(Overlay_V26, '4:')
    overlay_5 = Cpt(Overlay_V26, '5:')
    overlay_6 = Cpt(Overlay_V26, '6:')
    overlay_7 = Cpt(Overlay_V26, '7:')
    overlay_8 = Cpt(Overlay_V26, '8:')


class OverlayPlugin_V31(OverlayPlugin, version=(3, 1)):
    overlay_1 = Cpt(Overlay_V31, '1:')
    overlay_2 = Cpt(Overlay_V31, '2:')
    overlay_3 = Cpt(Overlay_V31, '3:')
    overlay_4 = Cpt(Overlay_V31, '4:')
    overlay_5 = Cpt(Overlay_V31, '5:')
    overlay_6 = Cpt(Overlay_V31, '6:')
    overlay_7 = Cpt(Overlay_V31, '7:')
    overlay_8 = Cpt(Overlay_V31, '8:')


class CommonPlugins(ADBase):
    ...

''', file=f)
    for version in versions[1:]:
        print()
        print()
        print(version)
        common_plugin_code = generate_common_plugins(version)
        print('', file=f)
        print('', file=f)
        print(common_plugin_code, file=f)


# AttrPlotPlugin_V31
# AttributeNPlugin_V22
# FilePlugin
# '': PosPluginPlugin_V25
# '': TimeSeriesNPlugin_V25
# '': TimeSeriesPlugin_V25
# '': TransformPlugin_V21
