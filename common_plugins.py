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



class CommonPlugins_V20(CommonPlugins, version=(2, 0), version_of=CommonPlugins):
    cc1 = Cpt(ColorConvPlugin_V20, "CC1:")
    cc2 = Cpt(ColorConvPlugin_V20, "CC2:")
    hdf1 = Cpt(HDF5Plugin_V20, "HDF1:")
    jpeg1 = Cpt(JPEGPlugin_V20, "JPEG1:")
    magick1 = Cpt(MagickPlugin_V20, "Magick1:")
    nexus1 = Cpt(NexusPlugin_V20, "Nexus1:")
    over1 = Cpt(OverlayPlugin, "Over1:")
    proc1 = Cpt(ProcessPlugin_V20, "Proc1:")
    roi1 = Cpt(ROIPlugin_V20, "ROI1:")
    roi2 = Cpt(ROIPlugin_V20, "ROI2:")
    roi3 = Cpt(ROIPlugin_V20, "ROI3:")
    roi4 = Cpt(ROIPlugin_V20, "ROI4:")
    stats1 = Cpt(StatsPlugin_V20, "Stats1:")
    stats2 = Cpt(StatsPlugin_V20, "Stats2:")
    stats3 = Cpt(StatsPlugin_V20, "Stats3:")
    stats4 = Cpt(StatsPlugin_V20, "Stats4:")
    stats5 = Cpt(StatsPlugin_V20, "Stats5:")
    tiff1 = Cpt(TIFFPlugin_V20, "TIFF1:")
    trans1 = Cpt(TransformPlugin_V20, "Trans1:")
    netcdf1 = Cpt(NetCDFPlugin_V20, "netCDF1:")


class CommonPlugins_V21(CommonPlugins, version=(2, 1), version_of=CommonPlugins):
    cc1 = Cpt(ColorConvPlugin_V20, "CC1:")
    cc2 = Cpt(ColorConvPlugin_V20, "CC2:")
    hdf1 = Cpt(HDF5Plugin_V21, "HDF1:")
    jpeg1 = Cpt(JPEGPlugin_V21, "JPEG1:")
    magick1 = Cpt(MagickPlugin_V21, "Magick1:")
    nexus1 = Cpt(NexusPlugin_V21, "Nexus1:")
    over1 = Cpt(OverlayPlugin_V21, "Over1:")
    proc1 = Cpt(ProcessPlugin_V20, "Proc1:")
    roi1 = Cpt(ROIPlugin_V20, "ROI1:")
    roi2 = Cpt(ROIPlugin_V20, "ROI2:")
    roi3 = Cpt(ROIPlugin_V20, "ROI3:")
    roi4 = Cpt(ROIPlugin_V20, "ROI4:")
    stats1 = Cpt(StatsPlugin_V20, "Stats1:")
    stats2 = Cpt(StatsPlugin_V20, "Stats2:")
    stats3 = Cpt(StatsPlugin_V20, "Stats3:")
    stats4 = Cpt(StatsPlugin_V20, "Stats4:")
    stats5 = Cpt(StatsPlugin_V20, "Stats5:")
    tiff1 = Cpt(TIFFPlugin_V21, "TIFF1:")
    trans1 = Cpt(TransformPlugin_V21, "Trans1:")
    netcdf1 = Cpt(NetCDFPlugin_V21, "netCDF1:")


class CommonPlugins_V22(CommonPlugins, version=(2, 2), version_of=CommonPlugins):
    attr1 = Cpt(AttributePlugin_V22, "Attr1:")
    cb1 = Cpt(CircularBuffPlugin_V22, "CB1:")
    cc1 = Cpt(ColorConvPlugin_V22, "CC1:")
    cc2 = Cpt(ColorConvPlugin_V22, "CC2:")
    hdf1 = Cpt(HDF5Plugin_V22, "HDF1:")
    jpeg1 = Cpt(JPEGPlugin_V22, "JPEG1:")
    magick1 = Cpt(MagickPlugin_V22, "Magick1:")
    nexus1 = Cpt(NexusPlugin_V22, "Nexus1:")
    over1 = Cpt(OverlayPlugin_V21, "Over1:")
    proc1 = Cpt(ProcessPlugin_V22, "Proc1:")
    roi1 = Cpt(ROIPlugin_V22, "ROI1:")
    roi2 = Cpt(ROIPlugin_V22, "ROI2:")
    roi3 = Cpt(ROIPlugin_V22, "ROI3:")
    roi4 = Cpt(ROIPlugin_V22, "ROI4:")
    roistat1 = Cpt(ROIStatPlugin_V22, "ROIStat1:")
    stats1 = Cpt(StatsPlugin_V22, "Stats1:")
    stats2 = Cpt(StatsPlugin_V22, "Stats2:")
    stats3 = Cpt(StatsPlugin_V22, "Stats3:")
    stats4 = Cpt(StatsPlugin_V22, "Stats4:")
    stats5 = Cpt(StatsPlugin_V22, "Stats5:")
    tiff1 = Cpt(TIFFPlugin_V22, "TIFF1:")
    trans1 = Cpt(TransformPlugin_V22, "Trans1:")
    netcdf1 = Cpt(NetCDFPlugin_V22, "netCDF1:")


class CommonPlugins_V23(CommonPlugins, version=(2, 3), version_of=CommonPlugins):
    attr1 = Cpt(AttributePlugin_V22, "Attr1:")
    cb1 = Cpt(CircularBuffPlugin_V22, "CB1:")
    cc1 = Cpt(ColorConvPlugin_V22, "CC1:")
    cc2 = Cpt(ColorConvPlugin_V22, "CC2:")
    hdf1 = Cpt(HDF5Plugin_V22, "HDF1:")
    jpeg1 = Cpt(JPEGPlugin_V22, "JPEG1:")
    magick1 = Cpt(MagickPlugin_V22, "Magick1:")
    nexus1 = Cpt(NexusPlugin_V22, "Nexus1:")
    over1 = Cpt(OverlayPlugin_V21, "Over1:")
    proc1 = Cpt(ProcessPlugin_V22, "Proc1:")
    roi1 = Cpt(ROIPlugin_V22, "ROI1:")
    roi2 = Cpt(ROIPlugin_V22, "ROI2:")
    roi3 = Cpt(ROIPlugin_V22, "ROI3:")
    roi4 = Cpt(ROIPlugin_V22, "ROI4:")
    roistat1 = Cpt(ROIStatPlugin_V23, "ROIStat1:")
    stats1 = Cpt(StatsPlugin_V22, "Stats1:")
    stats2 = Cpt(StatsPlugin_V22, "Stats2:")
    stats3 = Cpt(StatsPlugin_V22, "Stats3:")
    stats4 = Cpt(StatsPlugin_V22, "Stats4:")
    stats5 = Cpt(StatsPlugin_V22, "Stats5:")
    tiff1 = Cpt(TIFFPlugin_V22, "TIFF1:")
    trans1 = Cpt(TransformPlugin_V22, "Trans1:")
    netcdf1 = Cpt(NetCDFPlugin_V22, "netCDF1:")


class CommonPlugins_V24(CommonPlugins, version=(2, 4), version_of=CommonPlugins):
    attr1 = Cpt(AttributePlugin_V22, "Attr1:")
    cb1 = Cpt(CircularBuffPlugin_V22, "CB1:")
    cc1 = Cpt(ColorConvPlugin_V22, "CC1:")
    cc2 = Cpt(ColorConvPlugin_V22, "CC2:")
    hdf1 = Cpt(HDF5Plugin_V22, "HDF1:")
    jpeg1 = Cpt(JPEGPlugin_V22, "JPEG1:")
    magick1 = Cpt(MagickPlugin_V22, "Magick1:")
    nexus1 = Cpt(NexusPlugin_V22, "Nexus1:")
    over1 = Cpt(OverlayPlugin_V21, "Over1:")
    proc1 = Cpt(ProcessPlugin_V22, "Proc1:")
    roi1 = Cpt(ROIPlugin_V22, "ROI1:")
    roi2 = Cpt(ROIPlugin_V22, "ROI2:")
    roi3 = Cpt(ROIPlugin_V22, "ROI3:")
    roi4 = Cpt(ROIPlugin_V22, "ROI4:")
    roistat1 = Cpt(ROIStatPlugin_V23, "ROIStat1:")
    stats1 = Cpt(StatsPlugin_V22, "Stats1:")
    stats2 = Cpt(StatsPlugin_V22, "Stats2:")
    stats3 = Cpt(StatsPlugin_V22, "Stats3:")
    stats4 = Cpt(StatsPlugin_V22, "Stats4:")
    stats5 = Cpt(StatsPlugin_V22, "Stats5:")
    tiff1 = Cpt(TIFFPlugin_V22, "TIFF1:")
    trans1 = Cpt(TransformPlugin_V22, "Trans1:")
    netcdf1 = Cpt(NetCDFPlugin_V22, "netCDF1:")


class CommonPlugins_V25(CommonPlugins, version=(2, 5), version_of=CommonPlugins):
    attr1 = Cpt(AttributePlugin_V22, "Attr1:")
    cb1 = Cpt(CircularBuffPlugin_V22, "CB1:")
    cc1 = Cpt(ColorConvPlugin_V22, "CC1:")
    cc2 = Cpt(ColorConvPlugin_V22, "CC2:")
    hdf1 = Cpt(HDF5Plugin_V25, "HDF1:")
    jpeg1 = Cpt(JPEGPlugin_V22, "JPEG1:")
    magick1 = Cpt(MagickPlugin_V22, "Magick1:")
    nexus1 = Cpt(NexusPlugin_V22, "Nexus1:")
    over1 = Cpt(OverlayPlugin_V21, "Over1:")
    proc1 = Cpt(ProcessPlugin_V22, "Proc1:")
    roi1 = Cpt(ROIPlugin_V22, "ROI1:")
    roi2 = Cpt(ROIPlugin_V22, "ROI2:")
    roi3 = Cpt(ROIPlugin_V22, "ROI3:")
    roi4 = Cpt(ROIPlugin_V22, "ROI4:")
    roistat1 = Cpt(ROIStatPlugin_V23, "ROIStat1:")
    stats1 = Cpt(StatsPlugin_V25, "Stats1:")
    stats2 = Cpt(StatsPlugin_V25, "Stats2:")
    stats3 = Cpt(StatsPlugin_V25, "Stats3:")
    stats4 = Cpt(StatsPlugin_V25, "Stats4:")
    stats5 = Cpt(StatsPlugin_V25, "Stats5:")
    tiff1 = Cpt(TIFFPlugin_V22, "TIFF1:")
    trans1 = Cpt(TransformPlugin_V22, "Trans1:")
    netcdf1 = Cpt(NetCDFPlugin_V22, "netCDF1:")


class CommonPlugins_V26(CommonPlugins, version=(2, 6), version_of=CommonPlugins):
    attr1 = Cpt(AttributePlugin_V22, "Attr1:")
    cb1 = Cpt(CircularBuffPlugin_V26, "CB1:")
    cc1 = Cpt(ColorConvPlugin_V26, "CC1:")
    cc2 = Cpt(ColorConvPlugin_V26, "CC2:")
    hdf1 = Cpt(HDF5Plugin_V26, "HDF1:")
    jpeg1 = Cpt(JPEGPlugin_V26, "JPEG1:")
    magick1 = Cpt(MagickPlugin_V26, "Magick1:")
    nexus1 = Cpt(NexusPlugin_V26, "Nexus1:")
    over1 = Cpt(OverlayPlugin_V26, "Over1:")
    proc1 = Cpt(ProcessPlugin_V26, "Proc1:")
    roi1 = Cpt(ROIPlugin_V26, "ROI1:")
    roi2 = Cpt(ROIPlugin_V26, "ROI2:")
    roi3 = Cpt(ROIPlugin_V26, "ROI3:")
    roi4 = Cpt(ROIPlugin_V26, "ROI4:")
    roistat1 = Cpt(ROIStatPlugin_V26, "ROIStat1:")
    stats1 = Cpt(StatsPlugin_V26, "Stats1:")
    stats2 = Cpt(StatsPlugin_V26, "Stats2:")
    stats3 = Cpt(StatsPlugin_V26, "Stats3:")
    stats4 = Cpt(StatsPlugin_V26, "Stats4:")
    stats5 = Cpt(StatsPlugin_V26, "Stats5:")
    tiff1 = Cpt(TIFFPlugin_V26, "TIFF1:")
    trans1 = Cpt(TransformPlugin_V26, "Trans1:")
    netcdf1 = Cpt(NetCDFPlugin_V26, "netCDF1:")


class CommonPlugins_V31(CommonPlugins, version=(3, 1), version_of=CommonPlugins):
    attr1 = Cpt(AttributePlugin_V22, "Attr1:")
    cb1 = Cpt(CircularBuffPlugin_V31, "CB1:")
    cc1 = Cpt(ColorConvPlugin_V31, "CC1:")
    cc2 = Cpt(ColorConvPlugin_V31, "CC2:")
    fft1 = Cpt(FFTPlugin_V31, "FFT1:")
    gather1 = Cpt(GatherPlugin_V31, "Gather1:")
    hdf1 = Cpt(HDF5Plugin_V31, "HDF1:")
    jpeg1 = Cpt(JPEGPlugin_V31, "JPEG1:")
    nexus1 = Cpt(NexusPlugin_V31, "Nexus1:")
    over1 = Cpt(OverlayPlugin_V31, "Over1:")
    proc1 = Cpt(ProcessPlugin_V31, "Proc1:")
    roi1 = Cpt(ROIPlugin_V31, "ROI1:")
    roi2 = Cpt(ROIPlugin_V31, "ROI2:")
    roi3 = Cpt(ROIPlugin_V31, "ROI3:")
    roi4 = Cpt(ROIPlugin_V31, "ROI4:")
    roistat1 = Cpt(ROIStatPlugin_V31, "ROIStat1:")
    scatter1 = Cpt(ScatterPlugin_V31, "Scatter1:")
    stats1 = Cpt(StatsPlugin_V31, "Stats1:")
    stats2 = Cpt(StatsPlugin_V31, "Stats2:")
    stats3 = Cpt(StatsPlugin_V31, "Stats3:")
    stats4 = Cpt(StatsPlugin_V31, "Stats4:")
    stats5 = Cpt(StatsPlugin_V31, "Stats5:")
    tiff1 = Cpt(TIFFPlugin_V31, "TIFF1:")
    trans1 = Cpt(TransformPlugin_V31, "Trans1:")
    netcdf1 = Cpt(NetCDFPlugin_V31, "netCDF1:")


class CommonPlugins_V32(CommonPlugins, version=(3, 2), version_of=CommonPlugins):
    attr1 = Cpt(AttributePlugin_V22, "Attr1:")
    cb1 = Cpt(CircularBuffPlugin_V31, "CB1:")
    cc1 = Cpt(ColorConvPlugin_V31, "CC1:")
    cc2 = Cpt(ColorConvPlugin_V31, "CC2:")
    fft1 = Cpt(FFTPlugin_V31, "FFT1:")
    gather1 = Cpt(GatherPlugin_V31, "Gather1:")
    hdf1 = Cpt(HDF5Plugin_V32, "HDF1:")
    jpeg1 = Cpt(JPEGPlugin_V31, "JPEG1:")
    nexus1 = Cpt(NexusPlugin_V31, "Nexus1:")
    over1 = Cpt(OverlayPlugin_V31, "Over1:")
    proc1 = Cpt(ProcessPlugin_V31, "Proc1:")
    roi1 = Cpt(ROIPlugin_V31, "ROI1:")
    roi2 = Cpt(ROIPlugin_V31, "ROI2:")
    roi3 = Cpt(ROIPlugin_V31, "ROI3:")
    roi4 = Cpt(ROIPlugin_V31, "ROI4:")
    roistat1 = Cpt(ROIStatPlugin_V31, "ROIStat1:")
    scatter1 = Cpt(ScatterPlugin_V32, "Scatter1:")
    stats1 = Cpt(StatsPlugin_V32, "Stats1:")
    stats2 = Cpt(StatsPlugin_V32, "Stats2:")
    stats3 = Cpt(StatsPlugin_V32, "Stats3:")
    stats4 = Cpt(StatsPlugin_V32, "Stats4:")
    stats5 = Cpt(StatsPlugin_V32, "Stats5:")
    tiff1 = Cpt(TIFFPlugin_V31, "TIFF1:")
    trans1 = Cpt(TransformPlugin_V31, "Trans1:")
    netcdf1 = Cpt(NetCDFPlugin_V31, "netCDF1:")


class CommonPlugins_V33(CommonPlugins, version=(3, 3), version_of=CommonPlugins):
    attr1 = Cpt(AttributePlugin_V22, "Attr1:")
    cb1 = Cpt(CircularBuffPlugin_V33, "CB1:")
    cc1 = Cpt(ColorConvPlugin_V33, "CC1:")
    cc2 = Cpt(ColorConvPlugin_V33, "CC2:")
    fft1 = Cpt(FFTPlugin_V33, "FFT1:")
    gather1 = Cpt(GatherPlugin_V31, "Gather1:")
    hdf1 = Cpt(HDF5Plugin_V33, "HDF1:")
    jpeg1 = Cpt(JPEGPlugin_V33, "JPEG1:")
    nexus1 = Cpt(NexusPlugin_V33, "Nexus1:")
    over1 = Cpt(OverlayPlugin_V31, "Over1:")
    proc1 = Cpt(ProcessPlugin_V33, "Proc1:")
    roi1 = Cpt(ROIPlugin_V33, "ROI1:")
    roi2 = Cpt(ROIPlugin_V33, "ROI2:")
    roi3 = Cpt(ROIPlugin_V33, "ROI3:")
    roi4 = Cpt(ROIPlugin_V33, "ROI4:")
    roistat1 = Cpt(ROIStatPlugin_V33, "ROIStat1:")
    scatter1 = Cpt(ScatterPlugin_V33, "Scatter1:")
    stats1 = Cpt(StatsPlugin_V33, "Stats1:", configuration_attrs=[])
    stats2 = Cpt(StatsPlugin_V33, "Stats2:", configuration_attrs=[])
    stats3 = Cpt(StatsPlugin_V33, "Stats3:", configuration_attrs=[])
    stats4 = Cpt(StatsPlugin_V33, "Stats4:", configuration_attrs=[])
    stats5 = Cpt(StatsPlugin_V33, "Stats5:", configuration_attrs=[])
    tiff1 = Cpt(TIFFPlugin_V33, "TIFF1:")
    trans1 = Cpt(TransformPlugin_V33, "Trans1:")
    netcdf1 = Cpt(NetCDFPlugin_V33, "netCDF1:")
    proc1_tiff = Cpt(TIFFPlugin_V33, "Proc1:TIFF:")
    stats1_ts = Cpt(TimeSeriesPlugin_V33, "Stats1:TS:", configuration_attrs=[])
    stats2_ts = Cpt(TimeSeriesPlugin_V33, "Stats2:TS:", configuration_attrs=[])
    stats3_ts = Cpt(TimeSeriesPlugin_V33, "Stats3:TS:", configuration_attrs=[])
    stats4_ts = Cpt(TimeSeriesPlugin_V33, "Stats4:TS:", configuration_attrs=[])
    stats5_ts = Cpt(TimeSeriesPlugin_V33, "Stats5:TS:", configuration_attrs=[])


class CommonPlugins_V34(CommonPlugins, version=(3, 4), version_of=CommonPlugins):
    attr1 = Cpt(AttributePlugin_V22, "Attr1:")
    cb1 = Cpt(CircularBuffPlugin_V34, "CB1:")
    cc1 = Cpt(ColorConvPlugin_V34, "CC1:")
    cc2 = Cpt(ColorConvPlugin_V34, "CC2:")
    codec1 = Cpt(CodecPlugin_V34, "Codec1:")
    codec2 = Cpt(CodecPlugin_V34, "Codec2:")
    fft1 = Cpt(FFTPlugin_V34, "FFT1:")
    gather1 = Cpt(GatherPlugin_V31, "Gather1:")
    hdf1 = Cpt(HDF5Plugin_V34, "HDF1:")
    jpeg1 = Cpt(JPEGPlugin_V34, "JPEG1:")
    nexus1 = Cpt(NexusPlugin_V34, "Nexus1:")
    over1 = Cpt(OverlayPlugin_V31, "Over1:")
    proc1 = Cpt(ProcessPlugin_V34, "Proc1:")
    roi1 = Cpt(ROIPlugin_V34, "ROI1:")
    roi2 = Cpt(ROIPlugin_V34, "ROI2:")
    roi3 = Cpt(ROIPlugin_V34, "ROI3:")
    roi4 = Cpt(ROIPlugin_V34, "ROI4:")
    roistat1 = Cpt(ROIStatPlugin_V34, "ROIStat1:")
    scatter1 = Cpt(ScatterPlugin_V34, "Scatter1:")
    stats1 = Cpt(StatsPlugin_V34, "Stats1:", configuration_attrs=[])
    stats2 = Cpt(StatsPlugin_V34, "Stats2:", configuration_attrs=[])
    stats3 = Cpt(StatsPlugin_V34, "Stats3:", configuration_attrs=[])
    stats4 = Cpt(StatsPlugin_V34, "Stats4:", configuration_attrs=[])
    stats5 = Cpt(StatsPlugin_V34, "Stats5:", configuration_attrs=[])
    tiff1 = Cpt(TIFFPlugin_V34, "TIFF1:")
    trans1 = Cpt(TransformPlugin_V34, "Trans1:")
    netcdf1 = Cpt(NetCDFPlugin_V34, "netCDF1:")
    proc1_tiff = Cpt(TIFFPlugin_V34, "Proc1:TIFF:")
    stats1_ts = Cpt(TimeSeriesPlugin_V34, "Stats1:TS:", configuration_attrs=[])
    stats2_ts = Cpt(TimeSeriesPlugin_V34, "Stats2:TS:", configuration_attrs=[])
    stats3_ts = Cpt(TimeSeriesPlugin_V34, "Stats3:TS:", configuration_attrs=[])
    stats4_ts = Cpt(TimeSeriesPlugin_V34, "Stats4:TS:", configuration_attrs=[])
    stats5_ts = Cpt(TimeSeriesPlugin_V34, "Stats5:TS:", configuration_attrs=[])
