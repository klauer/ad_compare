from ophyd import (Device, Component as Cpt, DynamicDeviceComponent as DDC,
                   EpicsSignal, EpicsSignalRO)
from ophyd.areadetector.plugins import (
    PluginBase, Overlay, ColorConvPlugin, FilePlugin, HDF5Plugin, ImagePlugin,
    JPEGPlugin, MagickPlugin, NetCDFPlugin, NexusPlugin, OverlayPlugin,
    ProcessPlugin, ROIPlugin, StatsPlugin, TIFFPlugin, TransformPlugin)
from ophyd.areadetector import (ADBase, EpicsSignalWithRBV as SignalWithRBV, ad_group)
from all_plugins import *

available_versions = [(2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6),
                      (3, 1), (3, 2), (3, 3), (3, 4),
                      ]

def _select_version(cls, version):
    all_versions = cls._device_versions_
    try:
        matched_version = max(ver for ver in all_versions if ver <= version)
    except ValueError:
        print('Failed to find version of', cls.__name__, 'for version', version,
              'all versions:', all_versions)
        raise

    return all_versions[matched_version]


def _generate_overlay_plugin(clsname, version):
    cpt_cls = _select_version(Overlay, version)
    base_cls = _select_version(OverlayPlugin, version)
    class _OverlayPlugin(base_cls, version=version, version_of=OverlayPlugin):
        overlay_1 = Cpt(cpt_cls, '1:')
        overlay_2 = Cpt(cpt_cls, '2:')
        overlay_3 = Cpt(cpt_cls, '3:')
        overlay_4 = Cpt(cpt_cls, '4:')
        overlay_5 = Cpt(cpt_cls, '5:')
        overlay_6 = Cpt(cpt_cls, '6:')
        overlay_7 = Cpt(cpt_cls, '7:')
        overlay_8 = Cpt(cpt_cls, '8:')
    return _OverlayPlugin


def _generate_attribute_plugin(clsname, version):
    if version < (2, 2):
        return None
    cpt_cls = _select_version(AttributeNPlugin, version)
    base_cls = _select_version(AttributePlugin, version)

    class _AttributePlugin(base_cls, version=version, version_of=AttributePlugin):
        attr_1 = Cpt(cpt_cls, '1:')
        attr_2 = Cpt(cpt_cls, '2:')
        attr_3 = Cpt(cpt_cls, '3:')
        attr_4 = Cpt(cpt_cls, '4:')
        attr_5 = Cpt(cpt_cls, '5:')
        attr_6 = Cpt(cpt_cls, '6:')
        attr_7 = Cpt(cpt_cls, '7:')
        attr_8 = Cpt(cpt_cls, '8:')

    return _AttributePlugin


def _generate_roistat_plugin(clsname, version):
    if version < (2, 2):
        return None

    cpt_cls = _select_version(ROIStatNPlugin, version)
    base_cls = _select_version(ROIStatPlugin, version)

    class _ROIStatPlugin(base_cls, version=version, version_of=ROIStatPlugin):
        roistat_1 = Cpt(cpt_cls, '1:')
        roistat_2 = Cpt(cpt_cls, '2:')
        roistat_3 = Cpt(cpt_cls, '3:')
        roistat_4 = Cpt(cpt_cls, '4:')
        roistat_5 = Cpt(cpt_cls, '5:')
        roistat_6 = Cpt(cpt_cls, '6:')
        roistat_7 = Cpt(cpt_cls, '7:')
        roistat_8 = Cpt(cpt_cls, '8:')

    return _ROIStatPlugin


def _generate_gather_plugin(clsname, version):
    if version < (3, 1):
        return None

    cpt_cls = _select_version(GatherNPlugin, version)
    base_cls = _select_version(GatherPlugin, version)

    class _GatherPlugin(base_cls, version=version, version_of=GatherNPlugin):
        gather_1 = Cpt(cpt_cls, '', index=1)
        gather_2 = Cpt(cpt_cls, '', index=2)
        gather_3 = Cpt(cpt_cls, '', index=3)
        gather_4 = Cpt(cpt_cls, '', index=4)
        gather_5 = Cpt(cpt_cls, '', index=5)
        gather_6 = Cpt(cpt_cls, '', index=6)
        gather_7 = Cpt(cpt_cls, '', index=7)
        gather_8 = Cpt(cpt_cls, '', index=8)

    return _GatherPlugin


for version in available_versions:
    version_str = ''.join(str(v) for v in version)
    clsname = 'AttributePlugin_V{}'.format(version_str)
    globals()[clsname] = _generate_attribute_plugin(clsname, version)

    clsname = 'OverlayPlugin_V{}'.format(version_str)
    globals()[clsname] = _generate_overlay_plugin(clsname, version)

    clsname = 'ROIStatPlugin_V{}'.format(version_str)
    globals()[clsname] = _generate_roistat_plugin(clsname, version)

    clsname = 'GatherPlugin_V{}'.format(version_str)
    globals()[clsname] = _generate_gather_plugin(clsname, version)


class CommonPlugins(ADBase):
    ...
