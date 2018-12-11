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

        code.append(f'class CommonPlugins_V{ver_string}(CommonPlugins, version={ver_tuple}, version_of=CommonPlugins):')
        for suffix in sorted(suffixes):
            clsname = suffix_to_class[suffix.rstrip('1234567890')]

            if hasattr(all_plugins, clsname):
                plugin_cls = getattr(all_plugins, clsname)
            else:
                available_names = [name for name in dir(all_plugins)
                                   if name.startswith(clsname)]
                print(clsname, available_names)
                try:
                    plugin_cls = getattr(all_plugins, available_names[0])
                except IndexError:
                    code.append('    # TODO no classes available? {} {}'.format(version, suffix))
                    continue

            all_versions = plugin_cls._device_versions_
            try:
                clsversion = max(ver for ver in all_versions
                                 if ver <= ver_tuple)
            except ValueError:
                if suffix not in ('Gather1', ):
                    code.append('    # TODO unavailable: {} {}'.format(version, suffix))
                    continue
                clsversion = ''.join(str(v) for v in ver_tuple)
            else:
                print('versions', all_versions, clsversion)
                clsversion = ''.join(str(v) for v in clsversion)

            if clsversion == '191':
                clsversion = ''
            else:
                clsversion = f'_V{clsversion}'

            if clsname.startswith('Overlay'):
                clsname = 'OverlayPlugin'
            elif clsname.startswith('AttributeNPlugin'):
                clsname = 'AttributePlugin'
            elif clsname.startswith('ROIStat'):
                clsname = 'ROIStatPlugin'

            if 'Stats' in clsname and ver_tuple >= (3, 3):
                args = ', configuration_attrs=[]'
            else:
                args = ''
            code.append(f'    {suffix.lower()} = Cpt({clsname}{clsversion}, "{suffix}:"{args})')

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


def main():
    with open('common_plugins.py', 'wt') as f:
        print(open('common_plugins_header.py', 'rt').read(), file=f)
        for version in versions[1:]:
            if version in ('R3-3-1', 'R3-3-2'):
                continue
            print()
            print()
            common_plugin_code = generate_common_plugins(version)
            print('', file=f)
            print('', file=f)
            print(common_plugin_code, file=f)
            if version in ('R3-3', 'R3-4'):
                vs = get_version_string(version)
                print(f'    proc1_tiff = Cpt(TIFFPlugin_V{vs}, "Proc1:TIFF:")', file=f)
                print(f'    stats1_ts = Cpt(TimeSeriesPlugin_V{vs}, "Stats1:TS:", configuration_attrs=[])', file=f)
                print(f'    stats2_ts = Cpt(TimeSeriesPlugin_V{vs}, "Stats2:TS:", configuration_attrs=[])', file=f)
                print(f'    stats3_ts = Cpt(TimeSeriesPlugin_V{vs}, "Stats3:TS:", configuration_attrs=[])', file=f)
                print(f'    stats4_ts = Cpt(TimeSeriesPlugin_V{vs}, "Stats4:TS:", configuration_attrs=[])', file=f)
                print(f'    stats5_ts = Cpt(TimeSeriesPlugin_V{vs}, "Stats5:TS:", configuration_attrs=[])', file=f)


main()

# AttrPlotPlugin_V31
# AttributeNPlugin_V22
# FilePlugin
# '': PosPluginPlugin_V25
# '': TimeSeriesNPlugin_V25
# '': TimeSeriesPlugin_V25
# '': TransformPlugin_V21
