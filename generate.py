import re
import inspect
import collections

from ophyd.areadetector import plugins
from ophyd.areadetector.util import (StubInfo, EpicsSignalWithRBV)
from compare import compare

# for R1-9-1 if existing class, verify that all PVs are there and that's it


mbbi_value_to_string = {'ZRVL': 'ZRST',
                        'ONVL': 'ONST',
                        'TWVL': 'TWST',
                        'THVL': 'THST',
                        'FRVL': 'FRST',
                        'FVVL': 'FVST',
                        'SXVL': 'SXST',
                        'SVVL': 'SVST',
                        'EIVL': 'EIST',
                        'NIVL': 'NIST',
                        'TEVL': 'TEST',
                        'ELVL': 'ELST',
                        'TVVL': 'TVST',
                        'TTVL': 'TTST',
                        'FTVL': 'FTST',
                        'FFVL': 'FFST',
                        }

def _suffixes_from_device(devcls):
    '''Get all suffixes from a device, given its class'''
    for attr, cpt in devcls._sig_attrs.items():
        if hasattr(cpt, 'defn'):
            items = [(cls, suffix)
                     for cls, suffix, kwargs in cpt.defn.values()]
        elif hasattr(cpt, 'suffix'):
            items = [(cpt.cls, cpt.suffix)]
        else:
            items = []

        for cls, suffix in items:
            yield attr, suffix, cls
            if issubclass(cls, EpicsSignalWithRBV):
                yield attr, '{}_RBV'.format(suffix), cls


def check_if_exists(cls, pv):
    for attr, attr_pv, cls in _suffixes_from_device(cls):
        if pv == attr_pv:
            return attr, attr_pv, cls


def get_prop_name(existing_class, pv):
    '''Get a property name from the camel-case AreaDetector PV name'''
    if existing_class is not None:
        exists = check_if_exists(existing_class, pv)
        if exists:
            return exists[0]

    # If it's all capital letters and underscores, then just convert
    # to lower-case and that's it
    m = re.match('^[A-Z0-9_]+$', pv)
    if m:
        return pv.lower()

    # If the name starts with a bunch of capital letters, use
    # all but the last one as one word
    # e.g., TESTOne -> test_one
    m = re.match('^([A-Z0-9]+)', pv)
    if m:
        start_caps = m.groups()[0]
        pv = pv[len(start_caps):]
        pv = ''.join([start_caps[:-1].lower(), '_', start_caps[-1].lower(),
                      pv])

    if pv.endswith('_RBV'):
        pv = pv[:-len('_RBV')]

    # Get all groups of caps or lower-case
    # e.g., AAAbbbCCC -> 'AAA', 'bbb, 'CCC'
    split = re.findall('([a-z0-9:]+|[:A-Z0-9]+)', pv)
    ret = []

    # Put them all back together, removing single-letter splits
    for s in split:
        if ret and len(ret[-1]) == 1:
            ret[-1] += s
        else:
            ret.append(s)

    ret =  '_'.join(ret).lower()
    # TODO fixes
    end_fixes = {
        'v_al': '_val',
    }

    for from_, to in end_fixes.items():
        ret = ret.replace(from_, to)

    return ret


def group_with_rbv(records, existing_class):
    info = {}
    for record in records:
        if record.endswith('_RBV'):
            without_rbv = record[:-4]
        else:
            without_rbv = record

        with_rbv = f'{without_rbv}_RBV'

        if without_rbv in records and with_rbv in records:
            info[without_rbv] = 'with_rbv'
        elif without_rbv in records:
            info[without_rbv] = 'no_rbv'
        else:
            info[with_rbv] = 'only_rbv'

    potential_groups = {
        'X': 'YZN',
        'Y': 'ZN',
        '0': '123456789',
        '1': '234567890',
        '2': '34567890',
        '3': '4567890',
        '4': '567890',
        '5': '67890',
        '6': '7890',
    }
    for record, rbv_info in list(info.items()):
        for first, others in potential_groups.items():
            if record not in info:
                # already grouped
                break
            if first in record:
                list_name = list(record)
                idx = list_name.index(first)
                if list_name.count(first) > 1:
                    continue

                group = [record]
                for other in others:
                    list_name[idx] = other
                    other_name = ''.join(list_name)
                    if other_name in info:
                        if info[record] != info[other_name]:
                            # not the same rbv type, skip grouping
                            break
                        group.append(other_name)
                else:
                    if len(group) == 1:
                        continue
                    list_name.pop(idx)
                    without_name = ''.join(list_name)
                    for item in group:
                        info.pop(item)
                    prop_name = get_prop_name(existing_class, without_name)
                    if without_name.endswith('_RBV'):
                        without_name = without_name[:-len('_RBV')]
                    info[(prop_name, ) + tuple(group)] = rbv_info
                    # TODO: position_ylink -> position_link.y
                    # BUSTED

    return list(info.items())


def get_class_name(existing_class, version):
    if existing_class in (plugins.PluginBase, plugins.FilePlugin):
        existing_name = 'Todo'
    else:
        existing_name = existing_class.__name__

    if version == 'R1-9-1':
        return existing_name

    version = version.replace('-', '').lstrip('R')
    return f'{existing_name}_V{version}'


def find_per_version_records(existing_class, fn, renames):
    df = compare(fn)
    records = list(sorted(df.index))
    versions = df.columns

    per_version_records = {version: {}
                           for version in versions
                           }

    HierarchyInfo = collections.namedtuple('HierarchyInfo', 'record info rbv')

    for record, rbv_info in group_with_rbv(records, existing_class):
        last_info = None
        for version in versions:
            if isinstance(record, tuple):
                group_name, *group_records = record
                group_name = renames.get(group_name, group_name)
                rinfo = df.at[group_records[0], version]
                existing_in_base = [check_if_exists(existing_class, rec)
                                    for rec in group_records]
                if any(existing_in_base):
                    class_types = [item[-1] for item in existing_in_base
                                   if item is not None]
                    if all(existing_in_base) and len(set(class_types)) == 1:
                        print('ok', group_name, group_records,
                              set(class_types))
                    else:
                        print('our groups:', group_records)
                        print('what is in base class')
                        for i, item in enumerate(existing_in_base):
                            print('\t', i, item)
                        print('class types:', class_types)
                        raise ValueError(f'match some not all')

                prop_name = get_prop_name(existing_class, group_name)
                prop_name = renames.get(prop_name, prop_name)

                if rinfo == 'NO':
                    if last_info is None:
                        # does not exist yet
                        hier_info = None
                    elif last_info.info == 'NO':
                        # last one was also NO - ignore
                        hier_info = None
                    elif 'REMOVED' in last_info.info:
                        # removed in last version, no need to propagate
                        hier_info = None
                    else:
                        # newly removed
                        hier_info = HierarchyInfo(
                            record,
                            f'{prop_name} = None  # REMOVED {record}',
                            rbv_info)
                elif rinfo == '-' or rinfo.startswith('added'):
                    hier_info = None
                    # hier_info = HierarchyInfo(
                    #     record,
                    #     f'# {prop_name} ({record}) from parent',
                    #     rbv_info
                    # )
                elif last_info and last_info.rbv != rbv_info:
                    hier_info = HierarchyInfo(
                        record,
                        f'# !! {record} RBV changed',
                        rbv_info)
                else:
                    hier_info = HierarchyInfo(record, rinfo, rbv_info)
            else:
                rinfo = df.at[record, version]
                prop_name = get_prop_name(existing_class, record)
                if rinfo == 'NO':
                    if last_info is None:
                        # does not exist yet
                        hier_info = None
                    elif last_info.info == 'NO':
                        # last one was also NO - ignore
                        hier_info = None
                    elif 'REMOVED' in last_info.info:
                        # removed in last version, no need to propagate
                        hier_info = None
                    else:
                        # newly removed
                        hier_info = HierarchyInfo(
                            record,
                            f'{prop_name} = None  # REMOVED {record}',
                            rbv_info)
                elif rinfo == '-' or rinfo.startswith('added'):
                    hier_info = None
                    # hier_info = HierarchyInfo(
                    #     record,
                    #     f'# {prop_name} ({record}) from parent',
                    #     rbv_info
                    # )
                elif last_info and last_info.rbv != rbv_info:
                    hier_info = HierarchyInfo(
                        record,
                        f'# !! {record} RBV changed',
                        rbv_info)
                else:
                    hier_info = HierarchyInfo(record, rinfo, rbv_info)

            if hier_info is not None:
                per_version_records[version][hier_info.record] = hier_info
                last_info = hier_info

    for version, records in per_version_records.items():
        if all(r.info.startswith('#') for r in records.values()):
            # print(version, 'is identical')
            continue

        print()
        class_name = get_class_name(existing_class, version)
        for name, item in records.items():
            print(version, class_name, item.record, item.rbv,
                  item.info.replace('\n', '|')[:])
    return per_version_records


def split_back(rinfo):
    lines = rinfo.split('\n')
    ret = {}
    for line in lines:
        line = line.strip()
        if line in ('-', 'NO'):
            continue
        key, value = line.split(' ', 1)
        ret[key] = value
    return ret


def run(existing_class, fn, renames, output_f):
    class_map = {
        'only_rbv': 'EpicsSignalRO',
        'no_rbv': 'EpicsSignal',
        'with_rbv': 'SignalWithRBV',
    }

    per_version_records = find_per_version_records(existing_class, fn, renames)
    if existing_class is not None:
        parent_class = existing_class.__name__
    else:
        parent_class = 'PluginBase'
    print(f'from ophyd import (Component as Cpt, DynamicDeviceComponent as DDC)', file=output_f)
    print(f'from ophyd import (EpicsSignal, EpicsSignalRO)', file=output_f)
    print(f'from ophyd.areadetector.plugins import {parent_class}', file=output_f)
    print(f'from ophyd.areadetector.base import (EpicsSignalWithRBV as SignalWithRBV, ad_group)', file=output_f)

    for version, records in per_version_records.items():
        if all(r.info.startswith('#') for r in records.values()):
            # print(version, 'is identical')
            continue

        added = set()
        print(file=output_f)
        print(file=output_f)

        class_name = get_class_name(existing_class, version)
        print(f'class {class_name}({parent_class}):', file=output_f)
        string_info = ''

        for name, item in records.items():
            cls = class_map[item.rbv]
            if isinstance(item.record, tuple):
                prop_name, *records = item.record
                exists = check_if_exists(existing_class, records[0])
                if exists:
                    # first PV of group is DDC in existing class - use that
                    # name
                    prop_name = exists[0]

                if '# REMOVED ' in item.info:
                    if prop_name not in added:
                        print(f'    {prop_name} = None  # REMOVED DDC', file=output_f)
                    continue

                added.add(prop_name)
                print(f'''\
    {prop_name} = DDC(
        ad_group(
            {cls},
            [''', file=output_f)
                props = dict((rec, get_prop_name(None, rec))
                             for rec in records)
                for i, (rec, prop_name) in enumerate(props.items()):
                    print(f'''\
             ({prop_name!r}, {rec!r}),''',
                          file=output_f)

                print(f'''\
            ]),
            doc="{name[0]}",
            default_read_attrs={list(props.values())!r},
            )''', file=output_f)
                continue

            prop_name = get_prop_name(existing_class, item.record)
            prop_name = renames.get(prop_name, prop_name)

            if '# REMOVED ' in item.info:
                if prop_name not in added:
                    # don't remove something we just added...
                    print(f'    {prop_name} = None  # REMOVED',
                          file=output_f)
                continue

            added.add(prop_name)
            cpt_class = 'Cpt'
            record = item.record
            dinfo = split_back(item.info)
            if 'RTYP' in dinfo:
                rtyp = dinfo['RTYP']
                if rtyp in ('stringin', 'stringout'):
                    string_info = ', string=True'
                elif rtyp in ('bi', 'bo'):
                    try:
                        options = '0={ZNAM!r} 1={ONAM!r}'.format(**dinfo)
                    except KeyError:
                        options = ''
                    string_info = f', string=True, doc="{options}"'
                elif rtyp in ('mbbi', 'mbbo'):
                    options = ['{}={!r}'.format(dinfo.get(v), dinfo.get(s))
                               for v, s in mbbi_value_to_string.items()
                               if v in dinfo and s in dinfo]
                    options = ' '.join(options)
                    string_info = f', string=True, \n            doc="{options}"'

            print(f'    {prop_name} = {cpt_class}({cls}, {record!r}{string_info})',
                  file=output_f)

        parent_class = class_name



base_renames = {'type': 'types'}
with open('test.py', 'wt') as f:
    # run(plugins.ROIPlugin, 'NDROI.template', base_renames, output_f=f)
    # run(plugins.Overlay, 'NDOverlayN.template', base_renames, output_f=f)
    # run(plugins.ImagePlugin, 'NDStdArrays.template', base_renames, output_f=f)
    # rec = run(plugins.StatsPlugin, 'NDStats.template', base_renames, output_f=f)
    # run(plugins.ColorConvPlugin, 'NDColorConvert.template', base_renames, output_f=f)
    # run(plugins.ProcessPlugin, 'NDProcess.template', base_renames, output_f=f)
    # run(plugins.Overlay, 'NDOverlayN.template', base_renames, output_f=f)
    # run(plugins.OverlayPlugin, 'NDOverlay.template', base_renames, output_f=f)
    # run(plugins.ROIPlugin, 'NDROI.template', base_renames, output_f=f)
    # run(plugins.TransformPlugin, 'NDTransform.template', base_renames, output_f=f)
    # run(plugins.FilePlugin, 'NDFile.template', base_renames, output_f=f)
    # run(plugins.NetCDFPlugin, 'NDFileNetCDF.template', base_renames, output_f=f)
    # run(plugins.TIFFPlugin, 'NDFileTIFF.template', base_renames, output_f=f)
    # run(plugins.JPEGPlugin, 'NDFileJPEG.template', base_renames, output_f=f)
    # run(plugins.NexusPlugin, 'NDFileNexus.template', base_renames, output_f=f)
    # run(plugins.HDF5Plugin, 'NDFileHDF5.template', base_renames, output_f=f)
    # run(plugins.MagickPlugin, 'NDFileMagick.template', base_renames, output_f=f)
    # run(plugins.PluginBase, 'NDPva.template', base_renames, output_f=f)
    # run(plugins.PluginBase, 'NDFFT.template', base_renames, output_f=f)
    # run(plugins.PluginBase, 'NDScatter.template', base_renames, output_f=f)
    # run(plugins.PluginBase, 'NDPosPlugin.template', base_renames, output_f=f)
    # run(plugins.PluginBase, 'NDCircularBuff.template', base_renames, output_f=f)
    # run(plugins.PluginBase, 'NDAttributeN.template', base_renames, output_f=f)
    # run(plugins.PluginBase, 'NDAttrPlot.template', base_renames, output_f=f)
    # run(plugins.PluginBase, 'NDTimeSeriesN.template', base_renames, output_f=f)
    # run(plugins.PluginBase, 'NDTimeSeries.template', base_renames, output_f=f)

    # failures:
    # run(plugins.PluginBase, 'NDAttrPlotAttr.template', base_renames, output_f=f)
    # run(plugins.PluginBase, 'NDAttrPlotData.template', base_renames, output_f=f)
    # run(plugins.PluginBase, 'NDGatherN.template', base_renames, output_f=f)

    # nothing:
    # run(plugins.PluginBase, 'NDGather.template', base_renames, output_f=f)
