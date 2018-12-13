from ophyd import (Device, Component as Cpt, DynamicDeviceComponent as DDC,
                   EpicsSignal, EpicsSignalRO)
from ophyd.device import create_device_from_components
from ophyd.areadetector import (ADBase, EpicsSignalWithRBV as SignalWithRBV, ad_group)
import all_plugins


class PluginVersions(Device):
    ...


def _select_version(cls, version):
    all_versions = cls._class_info_['versions']
    matched_version = max(ver for ver in all_versions if ver <= version)
    return all_versions[matched_version]


def _get_bases(cls, version):
    mixin_cls = _select_version(cls, version)
    base_cls = _select_version(all_plugins.PluginBase, version)
    if issubclass(mixin_cls, base_cls):
        return (mixin_cls, )

    return (mixin_cls, base_cls)


def _generate_overlay_plugin(clsname, version):
    cpt_cls = _select_version(all_plugins.Overlay, version)
    bases = _get_bases(all_plugins.OverlayPlugin, version)

    return create_device_from_components(
        name=clsname,
        base_class=bases + (CommonOverlayPlugin, ),
        overlay_1=Cpt(cpt_cls, '1:'),
        overlay_2=Cpt(cpt_cls, '2:'),
        overlay_3=Cpt(cpt_cls, '3:'),
        overlay_4=Cpt(cpt_cls, '4:'),
        overlay_5=Cpt(cpt_cls, '5:'),
        overlay_6=Cpt(cpt_cls, '6:'),
        overlay_7=Cpt(cpt_cls, '7:'),
        overlay_8=Cpt(cpt_cls, '8:'),
    )


def _generate_attribute_plugin(clsname, version):
    if version < (2, 2):
        return None
    cpt_cls = _select_version(all_plugins.AttributeNPlugin, version)
    bases = _get_bases(all_plugins.AttributePlugin, version)

    return create_device_from_components(
        name=clsname,
        base_class=bases + (CommonAttributePlugin, ),
        attr_1=Cpt(cpt_cls, '1:'),
        attr_2=Cpt(cpt_cls, '2:'),
        attr_3=Cpt(cpt_cls, '3:'),
        attr_4=Cpt(cpt_cls, '4:'),
        attr_5=Cpt(cpt_cls, '5:'),
        attr_6=Cpt(cpt_cls, '6:'),
        attr_7=Cpt(cpt_cls, '7:'),
        attr_8=Cpt(cpt_cls, '8:'),
    )


def _generate_roistat_plugin(clsname, version):
    if version < (2, 2):
        return None

    cpt_cls = _select_version(all_plugins.ROIStatNPlugin, version)
    bases = _get_bases(all_plugins.ROIStatPlugin, version)

    return create_device_from_components(
        name=clsname,
        base_class=bases + (CommonROIStatPlugin, ),
        roistat_1=Cpt(cpt_cls, '1:'),
        roistat_2=Cpt(cpt_cls, '2:'),
        roistat_3=Cpt(cpt_cls, '3:'),
        roistat_4=Cpt(cpt_cls, '4:'),
        roistat_5=Cpt(cpt_cls, '5:'),
        roistat_6=Cpt(cpt_cls, '6:'),
        roistat_7=Cpt(cpt_cls, '7:'),
        roistat_8=Cpt(cpt_cls, '8:'),
    )


def _generate_gather_plugin(clsname, version):
    if version < (3, 1):
        return None

    cpt_cls = _select_version(all_plugins.GatherNPlugin, version)
    bases = _get_bases(all_plugins.GatherPlugin, version)

    return create_device_from_components(
        name=clsname,
        base_class=bases + (CommonGatherPlugin, ),
        gather_1=Cpt(cpt_cls, '', index=1),
        gather_2=Cpt(cpt_cls, '', index=2),
        gather_3=Cpt(cpt_cls, '', index=3),
        gather_4=Cpt(cpt_cls, '', index=4),
        gather_5=Cpt(cpt_cls, '', index=5),
        gather_6=Cpt(cpt_cls, '', index=6),
        gather_7=Cpt(cpt_cls, '', index=7),
        gather_8=Cpt(cpt_cls, '', index=8),
    )


class CommonOverlayPlugin(Device):
    ...


class CommonAttributePlugin(Device):
    ...


class CommonROIStatPlugin(Device):
    ...


class CommonGatherPlugin(Device):
    ...


class PluginVersions_V191(PluginVersions, version=(1, 9, 1), version_of=PluginVersions):
    ColorConvPlugin = all_plugins.ColorConvPlugin
    CommonOverlayPlugin = CommonOverlayPlugin
    HDF5Plugin = all_plugins.HDF5Plugin
    JPEGPlugin = all_plugins.JPEGPlugin
    MagickPlugin = all_plugins.MagickPlugin
    NetCDFPlugin = all_plugins.NetCDFPlugin
    NexusPlugin = all_plugins.NexusPlugin
    ProcessPlugin = all_plugins.ProcessPlugin
    ROIPlugin = all_plugins.ROIPlugin
    StatsPlugin = all_plugins.StatsPlugin
    TIFFPlugin = all_plugins.TIFFPlugin
    TransformPlugin = all_plugins.TransformPlugin


class PluginVersions_V20(PluginVersions, version=(2, 0), version_of=PluginVersions):
    ColorConvPlugin = all_plugins.ColorConvPlugin_V20
    CommonOverlayPlugin = _generate_overlay_plugin('CommonOverlayPlugin_V20', (2, 0))
    HDF5Plugin = all_plugins.HDF5Plugin_V20
    JPEGPlugin = all_plugins.JPEGPlugin_V20
    MagickPlugin = all_plugins.MagickPlugin_V20
    NetCDFPlugin = all_plugins.NetCDFPlugin_V20
    NexusPlugin = all_plugins.NexusPlugin_V20
    ProcessPlugin = all_plugins.ProcessPlugin_V20
    ROIPlugin = all_plugins.ROIPlugin_V20
    StatsPlugin = all_plugins.StatsPlugin_V20
    TIFFPlugin = all_plugins.TIFFPlugin_V20
    TransformPlugin = all_plugins.TransformPlugin_V20


class PluginVersions_V21(PluginVersions, version=(2, 1), version_of=PluginVersions):
    ColorConvPlugin = all_plugins.ColorConvPlugin_V20
    CommonOverlayPlugin = _generate_overlay_plugin('CommonOverlayPlugin_V21', (2, 1))
    HDF5Plugin = all_plugins.HDF5Plugin_V21
    JPEGPlugin = all_plugins.JPEGPlugin_V21
    MagickPlugin = all_plugins.MagickPlugin_V21
    NetCDFPlugin = all_plugins.NetCDFPlugin_V21
    NexusPlugin = all_plugins.NexusPlugin_V21
    ProcessPlugin = all_plugins.ProcessPlugin_V20
    ROIPlugin = all_plugins.ROIPlugin_V20
    StatsPlugin = all_plugins.StatsPlugin_V20
    TIFFPlugin = all_plugins.TIFFPlugin_V21
    TransformPlugin = all_plugins.TransformPlugin_V21


class PluginVersions_V22(PluginVersions, version=(2, 2), version_of=PluginVersions):
    CircularBuffPlugin = all_plugins.CircularBuffPlugin_V22
    ColorConvPlugin = all_plugins.ColorConvPlugin_V22
    CommonAttributePlugin = _generate_attribute_plugin('CommonAttributePlugin_V22', (2, 2))
    CommonOverlayPlugin = _generate_overlay_plugin('CommonOverlayPlugin_V22', (2, 2))
    CommonROIStatPlugin = _generate_roistat_plugin('CommonROIStatPlugin_V22', (2, 2))
    HDF5Plugin = all_plugins.HDF5Plugin_V22
    JPEGPlugin = all_plugins.JPEGPlugin_V22
    MagickPlugin = all_plugins.MagickPlugin_V22
    NetCDFPlugin = all_plugins.NetCDFPlugin_V22
    NexusPlugin = all_plugins.NexusPlugin_V22
    ProcessPlugin = all_plugins.ProcessPlugin_V22
    ROIPlugin = all_plugins.ROIPlugin_V22
    StatsPlugin = all_plugins.StatsPlugin_V22
    TIFFPlugin = all_plugins.TIFFPlugin_V22
    TransformPlugin = all_plugins.TransformPlugin_V22


class PluginVersions_V23(PluginVersions, version=(2, 3), version_of=PluginVersions):
    CircularBuffPlugin = all_plugins.CircularBuffPlugin_V22
    ColorConvPlugin = all_plugins.ColorConvPlugin_V22
    CommonAttributePlugin = _generate_attribute_plugin('CommonAttributePlugin_V23', (2, 3))
    CommonOverlayPlugin = _generate_overlay_plugin('CommonOverlayPlugin_V23', (2, 3))
    CommonROIStatPlugin = _generate_roistat_plugin('CommonROIStatPlugin_V23', (2, 3))
    HDF5Plugin = all_plugins.HDF5Plugin_V22
    JPEGPlugin = all_plugins.JPEGPlugin_V22
    MagickPlugin = all_plugins.MagickPlugin_V22
    NetCDFPlugin = all_plugins.NetCDFPlugin_V22
    NexusPlugin = all_plugins.NexusPlugin_V22
    ProcessPlugin = all_plugins.ProcessPlugin_V22
    ROIPlugin = all_plugins.ROIPlugin_V22
    StatsPlugin = all_plugins.StatsPlugin_V22
    TIFFPlugin = all_plugins.TIFFPlugin_V22
    TransformPlugin = all_plugins.TransformPlugin_V22


class PluginVersions_V24(PluginVersions, version=(2, 4), version_of=PluginVersions):
    CircularBuffPlugin = all_plugins.CircularBuffPlugin_V22
    ColorConvPlugin = all_plugins.ColorConvPlugin_V22
    CommonAttributePlugin = _generate_attribute_plugin('CommonAttributePlugin_V24', (2, 4))
    CommonOverlayPlugin = _generate_overlay_plugin('CommonOverlayPlugin_V24', (2, 4))
    CommonROIStatPlugin = _generate_roistat_plugin('CommonROIStatPlugin_V24', (2, 4))
    HDF5Plugin = all_plugins.HDF5Plugin_V22
    JPEGPlugin = all_plugins.JPEGPlugin_V22
    MagickPlugin = all_plugins.MagickPlugin_V22
    NetCDFPlugin = all_plugins.NetCDFPlugin_V22
    NexusPlugin = all_plugins.NexusPlugin_V22
    ProcessPlugin = all_plugins.ProcessPlugin_V22
    ROIPlugin = all_plugins.ROIPlugin_V22
    StatsPlugin = all_plugins.StatsPlugin_V22
    TIFFPlugin = all_plugins.TIFFPlugin_V22
    TransformPlugin = all_plugins.TransformPlugin_V22


class PluginVersions_V25(PluginVersions, version=(2, 5), version_of=PluginVersions):
    CircularBuffPlugin = all_plugins.CircularBuffPlugin_V22
    ColorConvPlugin = all_plugins.ColorConvPlugin_V22
    CommonAttributePlugin = _generate_attribute_plugin('CommonAttributePlugin_V25', (2, 5))
    CommonOverlayPlugin = _generate_overlay_plugin('CommonOverlayPlugin_V25', (2, 5))
    CommonROIStatPlugin = _generate_roistat_plugin('CommonROIStatPlugin_V25', (2, 5))
    HDF5Plugin = all_plugins.HDF5Plugin_V25
    JPEGPlugin = all_plugins.JPEGPlugin_V22
    MagickPlugin = all_plugins.MagickPlugin_V22
    NetCDFPlugin = all_plugins.NetCDFPlugin_V22
    NexusPlugin = all_plugins.NexusPlugin_V22
    ProcessPlugin = all_plugins.ProcessPlugin_V22
    ROIPlugin = all_plugins.ROIPlugin_V22
    StatsPlugin = all_plugins.StatsPlugin_V25
    TIFFPlugin = all_plugins.TIFFPlugin_V22
    TransformPlugin = all_plugins.TransformPlugin_V22


class PluginVersions_V26(PluginVersions, version=(2, 6), version_of=PluginVersions):
    CircularBuffPlugin = all_plugins.CircularBuffPlugin_V26
    ColorConvPlugin = all_plugins.ColorConvPlugin_V26
    CommonAttributePlugin = _generate_attribute_plugin('CommonAttributePlugin_V26', (2, 6))
    CommonOverlayPlugin = _generate_overlay_plugin('CommonOverlayPlugin_V26', (2, 6))
    CommonROIStatPlugin = _generate_roistat_plugin('CommonROIStatPlugin_V26', (2, 6))
    HDF5Plugin = all_plugins.HDF5Plugin_V26
    JPEGPlugin = all_plugins.JPEGPlugin_V26
    MagickPlugin = all_plugins.MagickPlugin_V26
    NetCDFPlugin = all_plugins.NetCDFPlugin_V26
    NexusPlugin = all_plugins.NexusPlugin_V26
    ProcessPlugin = all_plugins.ProcessPlugin_V26
    ROIPlugin = all_plugins.ROIPlugin_V26
    StatsPlugin = all_plugins.StatsPlugin_V26
    TIFFPlugin = all_plugins.TIFFPlugin_V26
    TransformPlugin = all_plugins.TransformPlugin_V26


class PluginVersions_V31(PluginVersions, version=(3, 1), version_of=PluginVersions):
    CircularBuffPlugin = all_plugins.CircularBuffPlugin_V31
    ColorConvPlugin = all_plugins.ColorConvPlugin_V31
    CommonAttributePlugin = _generate_attribute_plugin('CommonAttributePlugin_V31', (3, 1))
    CommonGatherPlugin = _generate_gather_plugin('CommonGatherPlugin_V31', (3, 1))
    CommonOverlayPlugin = _generate_overlay_plugin('CommonOverlayPlugin_V31', (3, 1))
    CommonROIStatPlugin = _generate_roistat_plugin('CommonROIStatPlugin_V31', (3, 1))
    FFTPlugin = all_plugins.FFTPlugin_V31
    HDF5Plugin = all_plugins.HDF5Plugin_V31
    JPEGPlugin = all_plugins.JPEGPlugin_V31
    NetCDFPlugin = all_plugins.NetCDFPlugin_V31
    NexusPlugin = all_plugins.NexusPlugin_V31
    ProcessPlugin = all_plugins.ProcessPlugin_V31
    ROIPlugin = all_plugins.ROIPlugin_V31
    ScatterPlugin = all_plugins.ScatterPlugin_V31
    StatsPlugin = all_plugins.StatsPlugin_V31
    TIFFPlugin = all_plugins.TIFFPlugin_V31
    TransformPlugin = all_plugins.TransformPlugin_V31


class PluginVersions_V32(PluginVersions, version=(3, 2), version_of=PluginVersions):
    CircularBuffPlugin = all_plugins.CircularBuffPlugin_V31
    ColorConvPlugin = all_plugins.ColorConvPlugin_V31
    CommonAttributePlugin = _generate_attribute_plugin('CommonAttributePlugin_V32', (3, 2))
    CommonGatherPlugin = _generate_gather_plugin('CommonGatherPlugin_V32', (3, 2))
    CommonOverlayPlugin = _generate_overlay_plugin('CommonOverlayPlugin_V32', (3, 2))
    CommonROIStatPlugin = _generate_roistat_plugin('CommonROIStatPlugin_V32', (3, 2))
    FFTPlugin = all_plugins.FFTPlugin_V31
    HDF5Plugin = all_plugins.HDF5Plugin_V32
    JPEGPlugin = all_plugins.JPEGPlugin_V31
    NetCDFPlugin = all_plugins.NetCDFPlugin_V31
    NexusPlugin = all_plugins.NexusPlugin_V31
    ProcessPlugin = all_plugins.ProcessPlugin_V31
    ROIPlugin = all_plugins.ROIPlugin_V31
    ScatterPlugin = all_plugins.ScatterPlugin_V32
    StatsPlugin = all_plugins.StatsPlugin_V32
    TIFFPlugin = all_plugins.TIFFPlugin_V31
    TransformPlugin = all_plugins.TransformPlugin_V31


class PluginVersions_V33(PluginVersions, version=(3, 3), version_of=PluginVersions):
    CircularBuffPlugin = all_plugins.CircularBuffPlugin_V33
    ColorConvPlugin = all_plugins.ColorConvPlugin_V33
    CommonAttributePlugin = _generate_attribute_plugin('CommonAttributePlugin_V33', (3, 3))
    CommonGatherPlugin = _generate_gather_plugin('CommonGatherPlugin_V33', (3, 3))
    CommonOverlayPlugin = _generate_overlay_plugin('CommonOverlayPlugin_V33', (3, 3))
    CommonROIStatPlugin = _generate_roistat_plugin('CommonROIStatPlugin_V33', (3, 3))
    FFTPlugin = all_plugins.FFTPlugin_V33
    HDF5Plugin = all_plugins.HDF5Plugin_V33
    JPEGPlugin = all_plugins.JPEGPlugin_V33
    NetCDFPlugin = all_plugins.NetCDFPlugin_V33
    NexusPlugin = all_plugins.NexusPlugin_V33
    ProcessPlugin = all_plugins.ProcessPlugin_V33
    ROIPlugin = all_plugins.ROIPlugin_V33
    ScatterPlugin = all_plugins.ScatterPlugin_V33
    StatsPlugin = all_plugins.StatsPlugin_V33
    TIFFPlugin = all_plugins.TIFFPlugin_V33
    TimeSeriesPlugin = all_plugins.TimeSeriesPlugin_V33
    TransformPlugin = all_plugins.TransformPlugin_V33


class PluginVersions_V34(PluginVersions, version=(3, 4), version_of=PluginVersions):
    CircularBuffPlugin = all_plugins.CircularBuffPlugin_V34
    CodecPlugin = all_plugins.CodecPlugin_V34
    ColorConvPlugin = all_plugins.ColorConvPlugin_V34
    CommonAttributePlugin = _generate_attribute_plugin('CommonAttributePlugin_V34', (3, 4))
    CommonGatherPlugin = _generate_gather_plugin('CommonGatherPlugin_V34', (3, 4))
    CommonOverlayPlugin = _generate_overlay_plugin('CommonOverlayPlugin_V34', (3, 4))
    CommonROIStatPlugin = _generate_roistat_plugin('CommonROIStatPlugin_V34', (3, 4))
    FFTPlugin = all_plugins.FFTPlugin_V34
    HDF5Plugin = all_plugins.HDF5Plugin_V34
    JPEGPlugin = all_plugins.JPEGPlugin_V34
    NetCDFPlugin = all_plugins.NetCDFPlugin_V34
    NexusPlugin = all_plugins.NexusPlugin_V34
    ProcessPlugin = all_plugins.ProcessPlugin_V34
    ROIPlugin = all_plugins.ROIPlugin_V34
    ScatterPlugin = all_plugins.ScatterPlugin_V34
    StatsPlugin = all_plugins.StatsPlugin_V34
    TIFFPlugin = all_plugins.TIFFPlugin_V34
    TimeSeriesPlugin = all_plugins.TimeSeriesPlugin_V34
    TransformPlugin = all_plugins.TransformPlugin_V34


class CommonPlugins(Device):
    ...


class CommonPlugins_V20(CommonPlugins, version=(2, 0), version_of=CommonPlugins):
    plugins = PluginVersions_V20

    cc1 = Cpt(plugins.ColorConvPlugin, "CC1:")
    cc2 = Cpt(plugins.ColorConvPlugin, "CC2:")
    hdf1 = Cpt(plugins.HDF5Plugin, "HDF1:")
    jpeg1 = Cpt(plugins.JPEGPlugin, "JPEG1:")
    magick1 = Cpt(plugins.MagickPlugin, "Magick1:")
    nexus1 = Cpt(plugins.NexusPlugin, "Nexus1:")
    over1 = Cpt(plugins.CommonOverlayPlugin, "Over1:")
    proc1 = Cpt(plugins.ProcessPlugin, "Proc1:")
    roi1 = Cpt(plugins.ROIPlugin, "ROI1:")
    roi2 = Cpt(plugins.ROIPlugin, "ROI2:")
    roi3 = Cpt(plugins.ROIPlugin, "ROI3:")
    roi4 = Cpt(plugins.ROIPlugin, "ROI4:")
    stats1 = Cpt(plugins.StatsPlugin, "Stats1:")
    stats2 = Cpt(plugins.StatsPlugin, "Stats2:")
    stats3 = Cpt(plugins.StatsPlugin, "Stats3:")
    stats4 = Cpt(plugins.StatsPlugin, "Stats4:")
    stats5 = Cpt(plugins.StatsPlugin, "Stats5:")
    tiff1 = Cpt(plugins.TIFFPlugin, "TIFF1:")
    trans1 = Cpt(plugins.TransformPlugin, "Trans1:")
    netcdf1 = Cpt(plugins.NetCDFPlugin, "netCDF1:")


class CommonPlugins_V21(CommonPlugins, version=(2, 1), version_of=CommonPlugins):
    plugins = PluginVersions_V21

    cc1 = Cpt(plugins.ColorConvPlugin, "CC1:")
    cc2 = Cpt(plugins.ColorConvPlugin, "CC2:")
    hdf1 = Cpt(plugins.HDF5Plugin, "HDF1:")
    jpeg1 = Cpt(plugins.JPEGPlugin, "JPEG1:")
    magick1 = Cpt(plugins.MagickPlugin, "Magick1:")
    nexus1 = Cpt(plugins.NexusPlugin, "Nexus1:")
    over1 = Cpt(plugins.CommonOverlayPlugin, "Over1:")
    proc1 = Cpt(plugins.ProcessPlugin, "Proc1:")
    roi1 = Cpt(plugins.ROIPlugin, "ROI1:")
    roi2 = Cpt(plugins.ROIPlugin, "ROI2:")
    roi3 = Cpt(plugins.ROIPlugin, "ROI3:")
    roi4 = Cpt(plugins.ROIPlugin, "ROI4:")
    stats1 = Cpt(plugins.StatsPlugin, "Stats1:")
    stats2 = Cpt(plugins.StatsPlugin, "Stats2:")
    stats3 = Cpt(plugins.StatsPlugin, "Stats3:")
    stats4 = Cpt(plugins.StatsPlugin, "Stats4:")
    stats5 = Cpt(plugins.StatsPlugin, "Stats5:")
    tiff1 = Cpt(plugins.TIFFPlugin, "TIFF1:")
    trans1 = Cpt(plugins.TransformPlugin, "Trans1:")
    netcdf1 = Cpt(plugins.NetCDFPlugin, "netCDF1:")


class CommonPlugins_V22(CommonPlugins, version=(2, 2), version_of=CommonPlugins):
    plugins = PluginVersions_V22

    attr1 = Cpt(plugins.CommonAttributePlugin, "Attr1:")
    cb1 = Cpt(plugins.CircularBuffPlugin, "CB1:")
    cc1 = Cpt(plugins.ColorConvPlugin, "CC1:")
    cc2 = Cpt(plugins.ColorConvPlugin, "CC2:")
    hdf1 = Cpt(plugins.HDF5Plugin, "HDF1:")
    jpeg1 = Cpt(plugins.JPEGPlugin, "JPEG1:")
    magick1 = Cpt(plugins.MagickPlugin, "Magick1:")
    nexus1 = Cpt(plugins.NexusPlugin, "Nexus1:")
    over1 = Cpt(plugins.CommonOverlayPlugin, "Over1:")
    proc1 = Cpt(plugins.ProcessPlugin, "Proc1:")
    roi1 = Cpt(plugins.ROIPlugin, "ROI1:")
    roi2 = Cpt(plugins.ROIPlugin, "ROI2:")
    roi3 = Cpt(plugins.ROIPlugin, "ROI3:")
    roi4 = Cpt(plugins.ROIPlugin, "ROI4:")
    roistat1 = Cpt(plugins.CommonROIStatPlugin, "ROIStat1:")
    stats1 = Cpt(plugins.StatsPlugin, "Stats1:")
    stats2 = Cpt(plugins.StatsPlugin, "Stats2:")
    stats3 = Cpt(plugins.StatsPlugin, "Stats3:")
    stats4 = Cpt(plugins.StatsPlugin, "Stats4:")
    stats5 = Cpt(plugins.StatsPlugin, "Stats5:")
    tiff1 = Cpt(plugins.TIFFPlugin, "TIFF1:")
    trans1 = Cpt(plugins.TransformPlugin, "Trans1:")
    netcdf1 = Cpt(plugins.NetCDFPlugin, "netCDF1:")


class CommonPlugins_V23(CommonPlugins, version=(2, 3), version_of=CommonPlugins):
    plugins = PluginVersions_V23

    attr1 = Cpt(plugins.CommonAttributePlugin, "Attr1:")
    cb1 = Cpt(plugins.CircularBuffPlugin, "CB1:")
    cc1 = Cpt(plugins.ColorConvPlugin, "CC1:")
    cc2 = Cpt(plugins.ColorConvPlugin, "CC2:")
    hdf1 = Cpt(plugins.HDF5Plugin, "HDF1:")
    jpeg1 = Cpt(plugins.JPEGPlugin, "JPEG1:")
    magick1 = Cpt(plugins.MagickPlugin, "Magick1:")
    nexus1 = Cpt(plugins.NexusPlugin, "Nexus1:")
    over1 = Cpt(plugins.CommonOverlayPlugin, "Over1:")
    proc1 = Cpt(plugins.ProcessPlugin, "Proc1:")
    roi1 = Cpt(plugins.ROIPlugin, "ROI1:")
    roi2 = Cpt(plugins.ROIPlugin, "ROI2:")
    roi3 = Cpt(plugins.ROIPlugin, "ROI3:")
    roi4 = Cpt(plugins.ROIPlugin, "ROI4:")
    roistat1 = Cpt(plugins.CommonROIStatPlugin, "ROIStat1:")
    stats1 = Cpt(plugins.StatsPlugin, "Stats1:")
    stats2 = Cpt(plugins.StatsPlugin, "Stats2:")
    stats3 = Cpt(plugins.StatsPlugin, "Stats3:")
    stats4 = Cpt(plugins.StatsPlugin, "Stats4:")
    stats5 = Cpt(plugins.StatsPlugin, "Stats5:")
    tiff1 = Cpt(plugins.TIFFPlugin, "TIFF1:")
    trans1 = Cpt(plugins.TransformPlugin, "Trans1:")
    netcdf1 = Cpt(plugins.NetCDFPlugin, "netCDF1:")


class CommonPlugins_V24(CommonPlugins, version=(2, 4), version_of=CommonPlugins):
    plugins = PluginVersions_V24

    attr1 = Cpt(plugins.CommonAttributePlugin, "Attr1:")
    cb1 = Cpt(plugins.CircularBuffPlugin, "CB1:")
    cc1 = Cpt(plugins.ColorConvPlugin, "CC1:")
    cc2 = Cpt(plugins.ColorConvPlugin, "CC2:")
    hdf1 = Cpt(plugins.HDF5Plugin, "HDF1:")
    jpeg1 = Cpt(plugins.JPEGPlugin, "JPEG1:")
    magick1 = Cpt(plugins.MagickPlugin, "Magick1:")
    nexus1 = Cpt(plugins.NexusPlugin, "Nexus1:")
    over1 = Cpt(plugins.CommonOverlayPlugin, "Over1:")
    proc1 = Cpt(plugins.ProcessPlugin, "Proc1:")
    roi1 = Cpt(plugins.ROIPlugin, "ROI1:")
    roi2 = Cpt(plugins.ROIPlugin, "ROI2:")
    roi3 = Cpt(plugins.ROIPlugin, "ROI3:")
    roi4 = Cpt(plugins.ROIPlugin, "ROI4:")
    roistat1 = Cpt(plugins.CommonROIStatPlugin, "ROIStat1:")
    stats1 = Cpt(plugins.StatsPlugin, "Stats1:")
    stats2 = Cpt(plugins.StatsPlugin, "Stats2:")
    stats3 = Cpt(plugins.StatsPlugin, "Stats3:")
    stats4 = Cpt(plugins.StatsPlugin, "Stats4:")
    stats5 = Cpt(plugins.StatsPlugin, "Stats5:")
    tiff1 = Cpt(plugins.TIFFPlugin, "TIFF1:")
    trans1 = Cpt(plugins.TransformPlugin, "Trans1:")
    netcdf1 = Cpt(plugins.NetCDFPlugin, "netCDF1:")


class CommonPlugins_V25(CommonPlugins, version=(2, 5), version_of=CommonPlugins):
    plugins = PluginVersions_V25

    attr1 = Cpt(plugins.CommonAttributePlugin, "Attr1:")
    cb1 = Cpt(plugins.CircularBuffPlugin, "CB1:")
    cc1 = Cpt(plugins.ColorConvPlugin, "CC1:")
    cc2 = Cpt(plugins.ColorConvPlugin, "CC2:")
    hdf1 = Cpt(plugins.HDF5Plugin, "HDF1:")
    jpeg1 = Cpt(plugins.JPEGPlugin, "JPEG1:")
    magick1 = Cpt(plugins.MagickPlugin, "Magick1:")
    nexus1 = Cpt(plugins.NexusPlugin, "Nexus1:")
    over1 = Cpt(plugins.CommonOverlayPlugin, "Over1:")
    proc1 = Cpt(plugins.ProcessPlugin, "Proc1:")
    roi1 = Cpt(plugins.ROIPlugin, "ROI1:")
    roi2 = Cpt(plugins.ROIPlugin, "ROI2:")
    roi3 = Cpt(plugins.ROIPlugin, "ROI3:")
    roi4 = Cpt(plugins.ROIPlugin, "ROI4:")
    roistat1 = Cpt(plugins.CommonROIStatPlugin, "ROIStat1:")
    stats1 = Cpt(plugins.StatsPlugin, "Stats1:")
    stats2 = Cpt(plugins.StatsPlugin, "Stats2:")
    stats3 = Cpt(plugins.StatsPlugin, "Stats3:")
    stats4 = Cpt(plugins.StatsPlugin, "Stats4:")
    stats5 = Cpt(plugins.StatsPlugin, "Stats5:")
    tiff1 = Cpt(plugins.TIFFPlugin, "TIFF1:")
    trans1 = Cpt(plugins.TransformPlugin, "Trans1:")
    netcdf1 = Cpt(plugins.NetCDFPlugin, "netCDF1:")


class CommonPlugins_V26(CommonPlugins, version=(2, 6), version_of=CommonPlugins):
    plugins = PluginVersions_V26

    attr1 = Cpt(plugins.CommonAttributePlugin, "Attr1:")
    cb1 = Cpt(plugins.CircularBuffPlugin, "CB1:")
    cc1 = Cpt(plugins.ColorConvPlugin, "CC1:")
    cc2 = Cpt(plugins.ColorConvPlugin, "CC2:")
    hdf1 = Cpt(plugins.HDF5Plugin, "HDF1:")
    jpeg1 = Cpt(plugins.JPEGPlugin, "JPEG1:")
    magick1 = Cpt(plugins.MagickPlugin, "Magick1:")
    nexus1 = Cpt(plugins.NexusPlugin, "Nexus1:")
    over1 = Cpt(plugins.CommonOverlayPlugin, "Over1:")
    proc1 = Cpt(plugins.ProcessPlugin, "Proc1:")
    roi1 = Cpt(plugins.ROIPlugin, "ROI1:")
    roi2 = Cpt(plugins.ROIPlugin, "ROI2:")
    roi3 = Cpt(plugins.ROIPlugin, "ROI3:")
    roi4 = Cpt(plugins.ROIPlugin, "ROI4:")
    roistat1 = Cpt(plugins.CommonROIStatPlugin, "ROIStat1:")
    stats1 = Cpt(plugins.StatsPlugin, "Stats1:")
    stats2 = Cpt(plugins.StatsPlugin, "Stats2:")
    stats3 = Cpt(plugins.StatsPlugin, "Stats3:")
    stats4 = Cpt(plugins.StatsPlugin, "Stats4:")
    stats5 = Cpt(plugins.StatsPlugin, "Stats5:")
    tiff1 = Cpt(plugins.TIFFPlugin, "TIFF1:")
    trans1 = Cpt(plugins.TransformPlugin, "Trans1:")
    netcdf1 = Cpt(plugins.NetCDFPlugin, "netCDF1:")


class CommonPlugins_V31(CommonPlugins, version=(3, 1), version_of=CommonPlugins):
    plugins = PluginVersions_V31

    attr1 = Cpt(plugins.CommonAttributePlugin, "Attr1:")
    cb1 = Cpt(plugins.CircularBuffPlugin, "CB1:")
    cc1 = Cpt(plugins.ColorConvPlugin, "CC1:")
    cc2 = Cpt(plugins.ColorConvPlugin, "CC2:")
    fft1 = Cpt(plugins.FFTPlugin, "FFT1:")
    gather1 = Cpt(plugins.CommonGatherPlugin, "Gather1:")
    hdf1 = Cpt(plugins.HDF5Plugin, "HDF1:")
    jpeg1 = Cpt(plugins.JPEGPlugin, "JPEG1:")
    nexus1 = Cpt(plugins.NexusPlugin, "Nexus1:")
    over1 = Cpt(plugins.CommonOverlayPlugin, "Over1:")
    proc1 = Cpt(plugins.ProcessPlugin, "Proc1:")
    roi1 = Cpt(plugins.ROIPlugin, "ROI1:")
    roi2 = Cpt(plugins.ROIPlugin, "ROI2:")
    roi3 = Cpt(plugins.ROIPlugin, "ROI3:")
    roi4 = Cpt(plugins.ROIPlugin, "ROI4:")
    roistat1 = Cpt(plugins.CommonROIStatPlugin, "ROIStat1:")
    scatter1 = Cpt(plugins.ScatterPlugin, "Scatter1:")
    stats1 = Cpt(plugins.StatsPlugin, "Stats1:")
    stats2 = Cpt(plugins.StatsPlugin, "Stats2:")
    stats3 = Cpt(plugins.StatsPlugin, "Stats3:")
    stats4 = Cpt(plugins.StatsPlugin, "Stats4:")
    stats5 = Cpt(plugins.StatsPlugin, "Stats5:")
    tiff1 = Cpt(plugins.TIFFPlugin, "TIFF1:")
    trans1 = Cpt(plugins.TransformPlugin, "Trans1:")
    netcdf1 = Cpt(plugins.NetCDFPlugin, "netCDF1:")


class CommonPlugins_V32(CommonPlugins, version=(3, 2), version_of=CommonPlugins):
    plugins = PluginVersions_V32

    attr1 = Cpt(plugins.CommonAttributePlugin, "Attr1:")
    cb1 = Cpt(plugins.CircularBuffPlugin, "CB1:")
    cc1 = Cpt(plugins.ColorConvPlugin, "CC1:")
    cc2 = Cpt(plugins.ColorConvPlugin, "CC2:")
    fft1 = Cpt(plugins.FFTPlugin, "FFT1:")
    gather1 = Cpt(plugins.CommonGatherPlugin, "Gather1:")
    hdf1 = Cpt(plugins.HDF5Plugin, "HDF1:")
    jpeg1 = Cpt(plugins.JPEGPlugin, "JPEG1:")
    nexus1 = Cpt(plugins.NexusPlugin, "Nexus1:")
    over1 = Cpt(plugins.CommonOverlayPlugin, "Over1:")
    proc1 = Cpt(plugins.ProcessPlugin, "Proc1:")
    roi1 = Cpt(plugins.ROIPlugin, "ROI1:")
    roi2 = Cpt(plugins.ROIPlugin, "ROI2:")
    roi3 = Cpt(plugins.ROIPlugin, "ROI3:")
    roi4 = Cpt(plugins.ROIPlugin, "ROI4:")
    roistat1 = Cpt(plugins.CommonROIStatPlugin, "ROIStat1:")
    scatter1 = Cpt(plugins.ScatterPlugin, "Scatter1:")
    stats1 = Cpt(plugins.StatsPlugin, "Stats1:")
    stats2 = Cpt(plugins.StatsPlugin, "Stats2:")
    stats3 = Cpt(plugins.StatsPlugin, "Stats3:")
    stats4 = Cpt(plugins.StatsPlugin, "Stats4:")
    stats5 = Cpt(plugins.StatsPlugin, "Stats5:")
    tiff1 = Cpt(plugins.TIFFPlugin, "TIFF1:")
    trans1 = Cpt(plugins.TransformPlugin, "Trans1:")
    netcdf1 = Cpt(plugins.NetCDFPlugin, "netCDF1:")


class CommonPlugins_V33(CommonPlugins, version=(3, 3), version_of=CommonPlugins):
    plugins = PluginVersions_V33

    attr1 = Cpt(plugins.CommonAttributePlugin, "Attr1:")
    cb1 = Cpt(plugins.CircularBuffPlugin, "CB1:")
    cc1 = Cpt(plugins.ColorConvPlugin, "CC1:")
    cc2 = Cpt(plugins.ColorConvPlugin, "CC2:")
    fft1 = Cpt(plugins.FFTPlugin, "FFT1:")
    gather1 = Cpt(plugins.CommonGatherPlugin, "Gather1:")
    hdf1 = Cpt(plugins.HDF5Plugin, "HDF1:")
    jpeg1 = Cpt(plugins.JPEGPlugin, "JPEG1:")
    netcdf1 = Cpt(plugins.NetCDFPlugin, "netCDF1:")
    nexus1 = Cpt(plugins.NexusPlugin, "Nexus1:")
    over1 = Cpt(plugins.CommonOverlayPlugin, "Over1:")
    proc1 = Cpt(plugins.ProcessPlugin, "Proc1:")
    proc1_tiff = Cpt(plugins.TIFFPlugin, "Proc1:TIFF:")
    roi1 = Cpt(plugins.ROIPlugin, "ROI1:")
    roi2 = Cpt(plugins.ROIPlugin, "ROI2:")
    roi3 = Cpt(plugins.ROIPlugin, "ROI3:")
    roi4 = Cpt(plugins.ROIPlugin, "ROI4:")
    roistat1 = Cpt(plugins.CommonROIStatPlugin, "ROIStat1:")
    scatter1 = Cpt(plugins.ScatterPlugin, "Scatter1:")
    stats1 = Cpt(plugins.StatsPlugin, "Stats1:")
    stats1_ts = Cpt(plugins.TimeSeriesPlugin, "Stats1:TS:")
    stats2 = Cpt(plugins.StatsPlugin, "Stats2:")
    stats2_ts = Cpt(plugins.TimeSeriesPlugin, "Stats2:TS:")
    stats3 = Cpt(plugins.StatsPlugin, "Stats3:")
    stats3_ts = Cpt(plugins.TimeSeriesPlugin, "Stats3:TS:")
    stats4 = Cpt(plugins.StatsPlugin, "Stats4:")
    stats4_ts = Cpt(plugins.TimeSeriesPlugin, "Stats4:TS:")
    stats5 = Cpt(plugins.StatsPlugin, "Stats5:")
    stats5_ts = Cpt(plugins.TimeSeriesPlugin, "Stats5:TS:")
    tiff1 = Cpt(plugins.TIFFPlugin, "TIFF1:")
    trans1 = Cpt(plugins.TransformPlugin, "Trans1:")


class CommonPlugins_V34(CommonPlugins, version=(3, 4), version_of=CommonPlugins):
    plugins = PluginVersions_V34

    attr1 = Cpt(plugins.CommonAttributePlugin, "Attr1:")
    cb1 = Cpt(plugins.CircularBuffPlugin, "CB1:")
    cc1 = Cpt(plugins.ColorConvPlugin, "CC1:")
    cc2 = Cpt(plugins.ColorConvPlugin, "CC2:")
    codec1 = Cpt(plugins.CodecPlugin, "Codec1:")
    codec2 = Cpt(plugins.CodecPlugin, "Codec2:")
    fft1 = Cpt(plugins.FFTPlugin, "FFT1:")
    gather1 = Cpt(plugins.CommonGatherPlugin, "Gather1:")
    hdf1 = Cpt(plugins.HDF5Plugin, "HDF1:")
    jpeg1 = Cpt(plugins.JPEGPlugin, "JPEG1:")
    netcdf1 = Cpt(plugins.NetCDFPlugin, "netCDF1:")
    nexus1 = Cpt(plugins.NexusPlugin, "Nexus1:")
    over1 = Cpt(plugins.CommonOverlayPlugin, "Over1:")
    proc1 = Cpt(plugins.ProcessPlugin, "Proc1:")
    proc1_tiff = Cpt(plugins.TIFFPlugin, "Proc1:TIFF:")
    roi1 = Cpt(plugins.ROIPlugin, "ROI1:")
    roi2 = Cpt(plugins.ROIPlugin, "ROI2:")
    roi3 = Cpt(plugins.ROIPlugin, "ROI3:")
    roi4 = Cpt(plugins.ROIPlugin, "ROI4:")
    roistat1 = Cpt(plugins.CommonROIStatPlugin, "ROIStat1:")
    scatter1 = Cpt(plugins.ScatterPlugin, "Scatter1:")
    stats1 = Cpt(plugins.StatsPlugin, "Stats1:")
    stats1_ts = Cpt(plugins.TimeSeriesPlugin, "Stats1:TS:")
    stats2 = Cpt(plugins.StatsPlugin, "Stats2:")
    stats2_ts = Cpt(plugins.TimeSeriesPlugin, "Stats2:TS:")
    stats3 = Cpt(plugins.StatsPlugin, "Stats3:")
    stats3_ts = Cpt(plugins.TimeSeriesPlugin, "Stats3:TS:")
    stats4 = Cpt(plugins.StatsPlugin, "Stats4:")
    stats4_ts = Cpt(plugins.TimeSeriesPlugin, "Stats4:TS:")
    stats5 = Cpt(plugins.StatsPlugin, "Stats5:")
    stats5_ts = Cpt(plugins.TimeSeriesPlugin, "Stats5:TS:")
    tiff1 = Cpt(plugins.TIFFPlugin, "TIFF1:")
    trans1 = Cpt(plugins.TransformPlugin, "Trans1:")
