import os
import sys
import git
import io
import re
import pathlib

import importlib
import collections
import textwrap

from ophyd.areadetector import plugins
from ophyd.areadetector.util import EpicsSignalWithRBV
from ophyd.areadetector.cam import CamBase
from compare import compare_dbtext
from generate import (mbbi_value_to_string, _suffixes_from_device,
                      check_if_exists, get_prop_name as _get_prop_name,
                      group_with_rbv, get_version_tuple, get_version_string,
                      get_hierarchy_info, split_back)


_fixes = {
    'pl_c': 'plc_',
    'maca_ddress': 'mac_address',
    'i_nterrupt': 'interrupt',
    'al_c': 'alc_',
    'alc_b_est': 'alc_best',
    'eb_': 'e_',
    'em_icc': 'emi_cc',
    'adcs_peed': 'adc_speed',
    'ad_crange': 'adc_range',
}


def fix_prop_name(name):
    for from_, to in _fixes.items():
        name = name.replace(from_, to)

    if name.startswith('q') and len(name) > 2:
        # qimagingcammmmm
        if name[2] == '_':
            name = ''.join((name[0], '_', name[1], name[3:]))
    return name


def get_prop_name(cls, rec):
    return fix_prop_name(_get_prop_name(cls, rec))


def get_class_name(existing_class, version, fn):
    if existing_class in (CamBase, ):
        if isinstance(fn, tuple):
            fn = fn[0]
        fn = os.path.split(fn)[-1]
        if fn.startswith('AD'):
            existing_name = fn[2:]
        else:
            existing_name = fn
        existing_name = existing_name.replace('.template', 'Cam')
    else:
        existing_name = existing_class.__name__

    if version == 'R1-9-1':
        return existing_name

    version = get_version_string(version)
    return f'{existing_name}_V{version}'


def find_per_version_records(existing_class, trees, fn, renames):
    skip_versions = ()

    tag_to_dbtext = {}
    for tag, tree in trees.items():
        if 'beta' in tag or 'dls_' in tag or 'pre' in tag:
            continue

        if not isinstance(fn, tuple):
            fn = (fn, )

        db_text = []
        blobs = [blob for blob in tree.traverse()
                 if blob.name in fn]

        print([blob.name for blob in tree.traverse()])

        print(tag, blobs)
        for blob in blobs:
            with io.BytesIO() as f:
                blob.stream_data(f)
                buf = bytearray(f.getbuffer())

            db_text.append(buf.decode('utf-8'))

        db_text = '\n'.join(db_text)
        tag_to_dbtext[tag] = db_text
        print(tag, db_text)

    df = compare_dbtext(tag_to_dbtext)
    records = list(sorted(df.index))
    versions = df.columns

    per_version_records = {version: {}
                           for version in versions
                           if version in df
                           and version not in skip_versions
                           }

    for record, rbv_info in group_with_rbv(records, existing_class):
        last_info = None
        for version in versions:
            if version in skip_versions:
                continue

            hier_info = get_hierarchy_info(df, existing_class, version,
                                           last_info, record, rbv_info,
                                           renames=renames)

            if hier_info is not None:
                per_version_records[version][hier_info.record] = hier_info
                last_info = hier_info

    for version, records in per_version_records.items():
        if all(r.info.startswith('#') for r in records.values()):
            # print(version, 'is identical')
            continue

        print()
        class_name = get_class_name(existing_class, version, fn)
        for name, item in records.items():
            print(version, class_name, item.record, item.rbv,
                  item.info.replace('\n', '|')[:])
    return per_version_records


def run(existing_class, repo_root, fn, renames, output_file, include_header=True):
    class_map = {
        'only_rbv': 'EpicsSignalRO',
        'no_rbv': 'EpicsSignal',
        'with_rbv': 'SignalWithRBV',
    }

    ddc_groups = {
        'EpicsSignal': 'DDC_EpicsSignal',
        'EpicsSignalRO': 'DDC_EpicsSignalRO',
        'SignalWithRBV': 'DDC_SignalWithRBV',
    }

    repo = git.Repo(repo_root)
    print('Repo root', repo_root, repo)
    print('tags', list(repo.tags))

    def deref(tag):
        if hasattr(tag, 'object'):
            return deref(tag.object)
        return tag

    if not len(repo.tags):
        trees = {'R0-0': repo.tree()}
    else:
        trees = {tag.name: deref(tag).tree for tag in repo.tags}

    print(repo_root, fn, len(trees), trees)

    per_version_records = find_per_version_records(existing_class, trees, fn,
                                                   renames)
    if existing_class is not None:
        parent_class = existing_class.__name__
    else:
        parent_class = 'TODO'

    if include_header:
        print(open('header-cam.py', 'rt').read(), file=output_file)

    print(f'# --- {fn} ---', file=output_file)

    first_class = None

    for version, records in per_version_records.items():
        version_tuple = get_version_tuple(version)

        if version == 'R1-9-1':
            f = sys.stdout
        else:
            f = output_file

        class_name = get_class_name(existing_class, version, fn)

        f.flush()
        # terrible, terrible magic
        generated_module = importlib.reload(importlib.import_module('all_cams'))
        mixin = ''

        if first_class is None:
            if parent_class == 'CamBase':
                first_class = class_name
            else:
                first_class = existing_class.__name__

        bases = [getattr(generated_module, parent_class)
                 if hasattr(generated_module, parent_class)
                 else getattr(plugins, parent_class)]

        print(bases)
        if mixin:
            bases.append(getattr(generated_module, mixin))
            mixin = f', {mixin}'

        added = set()
        removed = set()

        print(file=f)
        print(file=f)

        generated_class = type('GeneratedCls', tuple(bases), {})

        if parent_class.startswith('CamBase'):
            version_of = ''
        else:
            version_of = f', version_of={first_class}'

        if all(r.info.startswith('#') for r in records.values()):
            if mixin:
                print(f'class {class_name}({parent_class}{mixin}, version={version_tuple}{version_of}):',
                      file=f)
                print('    ...', file=f)
                parent_class = class_name
            continue

        print(f'class {class_name}({parent_class}{mixin}, version={version_tuple}{version_of}):',
              file=f)

        string_info = ''
        for name, item in records.items():
            cls = class_map[item.rbv]
            if isinstance(item.record, tuple):
                prop_name, *records = item.record
                exists = check_if_exists(generated_class, records[0])
                if exists:
                    # first PV of group is DDC in existing class - use that
                    # name
                    prop_name = exists[0]

                group = ddc_groups[cls]
                props = dict((rec, get_prop_name(None, rec))
                             for rec in records)
                prop_name = fix_prop_name(prop_name)

                if '# REMOVED ' in item.info:
                    if (prop_name not in added and
                            getattr(generated_class, prop_name, None) is not None):
                        print(f'    {prop_name} = None  # REMOVED DDC', file=f)
                        removed.add(prop_name)
                    continue

                elif getattr(generated_class, prop_name, None) is not None:
                    existing_cpt = getattr(generated_class, prop_name)
                    if hasattr(existing_cpt, 'defn') and len(props) == len(existing_cpt.defn):
                        continue
                    else:
                        print('    # Overriding {}={}'
                              ''.format(prop_name, getattr(existing_cpt, 'defn', None)),
                              file=f)

                if prop_name in added:
                    prop_name = prop_name + '_TODO'

                added.add(prop_name)
                print(f'    {prop_name} = {group}(', end='', file=f)
                for i, (rec, prop_name) in enumerate(props.items()):
                    print(f'({prop_name!r}, {rec!r}),', end='', file=f)

                print(f'doc="{prop_name}")', file=f)
                continue

            prop_name = get_prop_name(generated_class, item.record)

            if '# REMOVED ' in item.info:
                if (prop_name not in added and
                        getattr(generated_class, prop_name, None) is not None):
                    # don't remove something we just added...
                    print(f'    {prop_name} = None  # REMOVED',
                          file=f)
                    removed.add(prop_name)
                continue

            cpt_class = 'Cpt'
            record = item.record
            dinfo = split_back(item.info)
            if 'RTYP' in dinfo:
                rtyp = dinfo['RTYP']
                def quote_if_necessary(s):
                    if ' ' in s:
                        return repr(s)
                    return s

                if rtyp in ('stringin', 'stringout'):
                    string_info = ', string=True'
                elif rtyp in ('bi', 'bo'):
                    try:
                        options = '0={} 1={}'.format(quote_if_necessary(dinfo['ZNAM']),
                                                     quote_if_necessary(dinfo['ONAM']))
                    except KeyError:
                        options = ''
                    options = options.replace('"', "'")
                    string_info = f', string=True'
                    if options:
                        string_info += f', doc="{options}"'
                elif rtyp in ('mbbi', 'mbbo'):
                    options = ['{}={}'.format(dinfo.get(v), quote_if_necessary(dinfo.get(s)))
                               for v, s in mbbi_value_to_string.items()
                               if v in dinfo and s in dinfo]
                    options = ' '.join(options)
                    options = options.replace('"', "'")
                    string_info = f', string=True'
                    if options:
                        string_info += f', doc="{options}"'
                else:
                    string_info = ''

            if hasattr(generated_class, prop_name):
                cpt = getattr(generated_class, prop_name)
                if not hasattr(cpt, 'cls'):
                    beginning = '# hmm - conflict: '
                else:
                    beginning = '# hmm: '
            else:
                beginning = ''
                if prop_name in added:
                    prop_name = prop_name + '_TODO'

                added.add(prop_name)
                if '$(' in record:
                    record = record.replace('$(N)', '$(index)')
                    record = record.replace('$(', '{self.')
                    record = record.replace(')', '}')
                    record = '{self.prefix}' + record
                    cpt_class = 'FCpt'

            print(f'    {beginning}{prop_name} = {cpt_class}({cls}, {record!r}{string_info})',
                  file=f)

        if not added and not removed:
            print('    ...', file=f)

        if class_name == 'GatherNPlugin_V31':
            print('    def __init__(self, *args, index, **kwargs):', file=f)
            print('        self.index = index', file=f)
            print('        super().__init__(*args, **kwargs)', file=f)

        parent_class = class_name


base_renames = {'type': 'types',
                'name': 'name_',
                'trigger': 'trigger_',
                'position': 'position_',
                'l_evel': '_level',
                'tsn_sec': 'ts_nsec',
                'tss_ec': 'ts_sec',
                'attr_name': 'attribute_name',
                'flush_on_soft_trg': 'flush_on_soft_trigger',
                'nd_array_address_n': 'gather_array_address',
                'nd_array_port_n': 'gather_array_port',
                'maca_ddress': 'mac_address',
                'pl_c': 'plc_',
                }

ad_path = pathlib.Path('/Users/klauer/Repos/areaDetector')
to_run = [
    (CamBase, ad_path / 'ADAndor', 'andorCCD.template', base_renames),
    (CamBase, ad_path / 'ADDexela', 'Dexela.template', base_renames),
    (CamBase, ad_path / 'ADMerlin', ('merlin.template', 'medipix.template'), base_renames),
    (CamBase, ad_path / 'ADAndor3', 'andor3.template', base_renames),
    (CamBase, ad_path / 'ADAndor3', 'ase.template', base_renames),
    (CamBase, ad_path / 'ADAndor3', 'andor3.template', base_renames),
    (CamBase, ad_path / 'ADmarCCD', 'marCCD.template', base_renames),
    (CamBase, ad_path / 'ADQImaging', 'qimaging.template', base_renames),
    (CamBase, ad_path / 'ADPICam', 'PICam.template', base_renames),
    (CamBase, ad_path / 'aravisGigE', 'Prosilica_GC.template', base_renames),
    (CamBase, ad_path / 'aravisGigE', 'PGR_Flea3.template', base_renames),
    (CamBase, ad_path / 'aravisGigE', 'PSL_SCMOS.template', base_renames),
    (CamBase, ad_path / 'aravisGigE', 'PSL_FDI3.template', base_renames),
    (CamBase, ad_path / 'aravisGigE', 'PGR_BlackflyS_13Y3M.template', base_renames),
    (CamBase, ad_path / 'aravisGigE', 'PGR_Blackfly_20E4C.template', base_renames),
    (CamBase, ad_path / 'aravisGigE', 'PGR_GS3_U3_23S6M.template', base_renames),
    (CamBase, ad_path / 'aravisGigE', 'FLIR_ORX_10G_51S5M.template', base_renames),
    (CamBase, ad_path / 'aravisGigE', 'aravisCamera.template', base_renames),
    (CamBase, ad_path / 'ADProsilica', 'prosilica.template', base_renames),
    (CamBase, ad_path / 'ADLightField', 'LightField.template', base_renames),
    (CamBase, ad_path / 'ADLightField', 'LightField.template', base_renames),
    (CamBase, ad_path / 'ADPvCam', 'pvCam.template', base_renames),
    (CamBase, ad_path / 'ADADSC', 'adsc.template', base_renames),
    (CamBase, ad_path / 'ADEiger', 'eiger.template', base_renames),
    (CamBase, ad_path / 'ADMythen', 'mythen.template', base_renames),
    (CamBase, ad_path / 'ADRoper', 'roper.template', base_renames),
    (CamBase, ad_path / 'ADLambda', 'ase.template', base_renames),
    (CamBase, ad_path / 'ADLambda', 'ADLambda.template', base_renames),
    (CamBase, ad_path / 'ADFastCCD', 'FastCCD.template', base_renames),
    (CamBase, ad_path / 'ADPilatus', 'pilatus.template', base_renames),
    (CamBase, ad_path / 'ADmar345', 'mar345.template', base_renames),
    (CamBase, ad_path / 'ADPSL', 'ase.template', base_renames),
    (CamBase, ad_path / 'ADPSL', 'PSL.template', base_renames),
    (CamBase, ad_path / 'ADFireWireWin', 'firewireDCAM.template', base_renames),
    (CamBase, ad_path / 'ADBruker', 'BIS.template', base_renames),
    (CamBase, ad_path / 'ADPixirad', 'pixirad.template', base_renames),
    (CamBase, ad_path / 'ADPixirad', 'ase.template', base_renames),
    (CamBase, ad_path / 'ADPixirad', 'pixirad.template', base_renames),
    (CamBase, ad_path / 'ADPhotonII', 'PhotonII.template', base_renames),
    (CamBase, ad_path / 'NDDriverStdArrays', 'NDDriverStdArrays.template', base_renames),
    (CamBase, ad_path / 'ADPerkinElmer', 'PerkinElmer.template', base_renames),
    (CamBase, ad_path / 'ADPointGrey', 'pointGrey.template', base_renames),
]

if __name__ == '__main__':
    with open('all_cams.py', 'wt') as f:
        for idx, (base_cls, repo_root, template_fn, renames) in enumerate(to_run):
            run(base_cls, repo_root, template_fn, base_renames, output_file=f,
                include_header=(idx == 0))
