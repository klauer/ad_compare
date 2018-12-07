from ophyd import (Device, Component as Cpt, DynamicDeviceComponent as DDC,
                   EpicsSignal, EpicsSignalRO)
from ophyd.areadetector.plugins import (
    PluginBase, Overlay, ColorConvPlugin, FilePlugin, HDF5Plugin, ImagePlugin,
    JPEGPlugin, MagickPlugin, NetCDFPlugin, NexusPlugin, OverlayPlugin,
    ProcessPlugin, ROIPlugin, StatsPlugin, TIFFPlugin, TransformPlugin)
from ophyd.areadetector import EpicsSignalWithRBV as SignalWithRBV, ad_group
from all import (
    AttrPlotPlugin_V31,
    AttributeNPlugin_V22,
    CircularBuffPlugin_V22,
    CircularBuffPlugin_V34,
    CodecPlugin_V34,
    FFTPlugin_V25,
    FilePlugin_V21,
    FilePlugin_V22,
    HDF5Plugin_V20,
    HDF5Plugin_V21,
    HDF5Plugin_V22,
    HDF5Plugin_V25,
    HDF5Plugin_V32,
    MagickPlugin_V31,
    NetCDFPlugin_V21,
    Overlay_V21,
    Overlay_V26,
    Overlay_V31,
    PosPluginPlugin_V25,
    ProcessPlugin_V33,
    PvaPlugin_V25,
    ROIPlugin_V26,
    ROIStatPlugin_V22,
    ROIStatPlugin_V23,
    ScatterPlugin_V31,
    ScatterPlugin_V32,
    StatsPlugin_V21,
    StatsPlugin_V22,
    StatsPlugin_V25,
    StatsPlugin_V26,
    StatsPlugin_V32,
    StatsPlugin_V33,
    TimeSeriesNPlugin_V25,
    TimeSeriesPlugin_V25,
    TransformPlugin_V21,
    )


class GatherPlugin_V31(PluginBase, version=(3, 1)):
    ...


class CommonPlugins(Device):
    ...




class CommonPlugins_V20(CommonPlugins, version=(2, 0)):
    cc1 = Cpt(ColorConvPlugin, "CC1:")
    cc2 = Cpt(ColorConvPlugin, "CC2:")
    hdf1 = Cpt(HDF5Plugin_V20, "HDF1:")
    jpeg1 = Cpt(JPEGPlugin, "JPEG1:")
    magick1 = Cpt(MagickPlugin, "Magick1:")
    nexus1 = Cpt(NexusPlugin, "Nexus1:")
    over1 = Cpt(Overlay, "Over1:")
    proc1 = Cpt(ProcessPlugin, "Proc1:")
    roi1 = Cpt(ROIPlugin, "ROI1:")
    roi2 = Cpt(ROIPlugin, "ROI2:")
    roi3 = Cpt(ROIPlugin, "ROI3:")
    roi4 = Cpt(ROIPlugin, "ROI4:")
    stats1 = Cpt(StatsPlugin, "Stats1:")
    stats2 = Cpt(StatsPlugin, "Stats2:")
    stats3 = Cpt(StatsPlugin, "Stats3:")
    stats4 = Cpt(StatsPlugin, "Stats4:")
    stats5 = Cpt(StatsPlugin, "Stats5:")
    tiff1 = Cpt(TIFFPlugin, "TIFF1:")
    trans1 = Cpt(TransformPlugin, "Trans1:")
    netcdf1 = Cpt(NetCDFPlugin, "netCDF1:")


class CommonPlugins_V21(CommonPlugins, version=(2, 1)):
    cc1 = Cpt(ColorConvPlugin, "CC1:")
    cc2 = Cpt(ColorConvPlugin, "CC2:")
    hdf1 = Cpt(HDF5Plugin_V20, "HDF1:")
    jpeg1 = Cpt(JPEGPlugin, "JPEG1:")
    magick1 = Cpt(MagickPlugin, "Magick1:")
    nexus1 = Cpt(NexusPlugin, "Nexus1:")
    over1 = Cpt(Overlay_V21, "Over1:")
    proc1 = Cpt(ProcessPlugin, "Proc1:")
    roi1 = Cpt(ROIPlugin, "ROI1:")
    roi2 = Cpt(ROIPlugin, "ROI2:")
    roi3 = Cpt(ROIPlugin, "ROI3:")
    roi4 = Cpt(ROIPlugin, "ROI4:")
    stats1 = Cpt(StatsPlugin_V21, "Stats1:")
    stats2 = Cpt(StatsPlugin_V21, "Stats2:")
    stats3 = Cpt(StatsPlugin_V21, "Stats3:")
    stats4 = Cpt(StatsPlugin_V21, "Stats4:")
    stats5 = Cpt(StatsPlugin_V21, "Stats5:")
    tiff1 = Cpt(TIFFPlugin, "TIFF1:")
    trans1 = Cpt(TransformPlugin_V21, "Trans1:")
    netcdf1 = Cpt(NetCDFPlugin_V21, "netCDF1:")


class CommonPlugins_V22(CommonPlugins, version=(2, 2)):
    attr1 = Cpt(AttributeNPlugin_V22, "Attr1:")
    cb1 = Cpt(CircularBuffPlugin_V22, "CB1:")
    cc1 = Cpt(ColorConvPlugin, "CC1:")
    cc2 = Cpt(ColorConvPlugin, "CC2:")
    hdf1 = Cpt(HDF5Plugin_V20, "HDF1:")
    jpeg1 = Cpt(JPEGPlugin, "JPEG1:")
    magick1 = Cpt(MagickPlugin, "Magick1:")
    nexus1 = Cpt(NexusPlugin, "Nexus1:")
    over1 = Cpt(Overlay_V21, "Over1:")
    proc1 = Cpt(ProcessPlugin, "Proc1:")
    roi1 = Cpt(ROIPlugin, "ROI1:")
    roi2 = Cpt(ROIPlugin, "ROI2:")
    roi3 = Cpt(ROIPlugin, "ROI3:")
    roi4 = Cpt(ROIPlugin, "ROI4:")
    roistat1 = Cpt(ROIStatPlugin_V22, "ROIStat1:")
    stats1 = Cpt(StatsPlugin_V22, "Stats1:")
    stats2 = Cpt(StatsPlugin_V22, "Stats2:")
    stats3 = Cpt(StatsPlugin_V22, "Stats3:")
    stats4 = Cpt(StatsPlugin_V22, "Stats4:")
    stats5 = Cpt(StatsPlugin_V22, "Stats5:")
    tiff1 = Cpt(TIFFPlugin, "TIFF1:")
    trans1 = Cpt(TransformPlugin_V21, "Trans1:")
    netcdf1 = Cpt(NetCDFPlugin, "netCDF1:")


class CommonPlugins_V23(CommonPlugins, version=(2, 3)):
    attr1 = Cpt(AttributeNPlugin_V22, "Attr1:")
    cb1 = Cpt(CircularBuffPlugin_V22, "CB1:")
    cc1 = Cpt(ColorConvPlugin, "CC1:")
    cc2 = Cpt(ColorConvPlugin, "CC2:")
    hdf1 = Cpt(HDF5Plugin_V20, "HDF1:")
    jpeg1 = Cpt(JPEGPlugin, "JPEG1:")
    magick1 = Cpt(MagickPlugin, "Magick1:")
    nexus1 = Cpt(NexusPlugin, "Nexus1:")
    over1 = Cpt(Overlay_V21, "Over1:")
    proc1 = Cpt(ProcessPlugin, "Proc1:")
    roi1 = Cpt(ROIPlugin, "ROI1:")
    roi2 = Cpt(ROIPlugin, "ROI2:")
    roi3 = Cpt(ROIPlugin, "ROI3:")
    roi4 = Cpt(ROIPlugin, "ROI4:")
    roistat1 = Cpt(ROIStatPlugin_V23, "ROIStat1:")
    stats1 = Cpt(StatsPlugin_V22, "Stats1:")
    stats2 = Cpt(StatsPlugin_V22, "Stats2:")
    stats3 = Cpt(StatsPlugin_V22, "Stats3:")
    stats4 = Cpt(StatsPlugin_V22, "Stats4:")
    stats5 = Cpt(StatsPlugin_V22, "Stats5:")
    tiff1 = Cpt(TIFFPlugin, "TIFF1:")
    trans1 = Cpt(TransformPlugin_V21, "Trans1:")
    netcdf1 = Cpt(NetCDFPlugin, "netCDF1:")


class CommonPlugins_V24(CommonPlugins, version=(2, 4)):
    attr1 = Cpt(AttributeNPlugin_V22, "Attr1:")
    cb1 = Cpt(CircularBuffPlugin_V22, "CB1:")
    cc1 = Cpt(ColorConvPlugin, "CC1:")
    cc2 = Cpt(ColorConvPlugin, "CC2:")
    hdf1 = Cpt(HDF5Plugin_V20, "HDF1:")
    jpeg1 = Cpt(JPEGPlugin, "JPEG1:")
    magick1 = Cpt(MagickPlugin, "Magick1:")
    nexus1 = Cpt(NexusPlugin, "Nexus1:")
    over1 = Cpt(Overlay_V21, "Over1:")
    proc1 = Cpt(ProcessPlugin, "Proc1:")
    roi1 = Cpt(ROIPlugin, "ROI1:")
    roi2 = Cpt(ROIPlugin, "ROI2:")
    roi3 = Cpt(ROIPlugin, "ROI3:")
    roi4 = Cpt(ROIPlugin, "ROI4:")
    roistat1 = Cpt(ROIStatPlugin_V23, "ROIStat1:")
    stats1 = Cpt(StatsPlugin_V22, "Stats1:")
    stats2 = Cpt(StatsPlugin_V22, "Stats2:")
    stats3 = Cpt(StatsPlugin_V22, "Stats3:")
    stats4 = Cpt(StatsPlugin_V22, "Stats4:")
    stats5 = Cpt(StatsPlugin_V22, "Stats5:")
    tiff1 = Cpt(TIFFPlugin, "TIFF1:")
    trans1 = Cpt(TransformPlugin_V21, "Trans1:")
    netcdf1 = Cpt(NetCDFPlugin, "netCDF1:")


class CommonPlugins_V25(CommonPlugins, version=(2, 5)):
    attr1 = Cpt(AttributeNPlugin_V22, "Attr1:")
    cb1 = Cpt(CircularBuffPlugin_V22, "CB1:")
    cc1 = Cpt(ColorConvPlugin, "CC1:")
    cc2 = Cpt(ColorConvPlugin, "CC2:")
    hdf1 = Cpt(HDF5Plugin_V20, "HDF1:")
    jpeg1 = Cpt(JPEGPlugin, "JPEG1:")
    magick1 = Cpt(MagickPlugin, "Magick1:")
    nexus1 = Cpt(NexusPlugin, "Nexus1:")
    over1 = Cpt(Overlay_V21, "Over1:")
    proc1 = Cpt(ProcessPlugin, "Proc1:")
    roi1 = Cpt(ROIPlugin, "ROI1:")
    roi2 = Cpt(ROIPlugin, "ROI2:")
    roi3 = Cpt(ROIPlugin, "ROI3:")
    roi4 = Cpt(ROIPlugin, "ROI4:")
    roistat1 = Cpt(ROIStatPlugin_V23, "ROIStat1:")
    stats1 = Cpt(StatsPlugin_V22, "Stats1:")
    stats2 = Cpt(StatsPlugin_V22, "Stats2:")
    stats3 = Cpt(StatsPlugin_V22, "Stats3:")
    stats4 = Cpt(StatsPlugin_V22, "Stats4:")
    stats5 = Cpt(StatsPlugin_V22, "Stats5:")
    tiff1 = Cpt(TIFFPlugin, "TIFF1:")
    trans1 = Cpt(TransformPlugin_V21, "Trans1:")
    netcdf1 = Cpt(NetCDFPlugin, "netCDF1:")


class CommonPlugins_V26(CommonPlugins, version=(2, 6)):
    attr1 = Cpt(AttributeNPlugin_V22, "Attr1:")
    cb1 = Cpt(CircularBuffPlugin_V22, "CB1:")
    cc1 = Cpt(ColorConvPlugin, "CC1:")
    cc2 = Cpt(ColorConvPlugin, "CC2:")
    hdf1 = Cpt(HDF5Plugin_V20, "HDF1:")
    jpeg1 = Cpt(JPEGPlugin, "JPEG1:")
    magick1 = Cpt(MagickPlugin, "Magick1:")
    nexus1 = Cpt(NexusPlugin, "Nexus1:")
    over1 = Cpt(Overlay_V21, "Over1:")
    proc1 = Cpt(ProcessPlugin, "Proc1:")
    roi1 = Cpt(ROIPlugin_V26, "ROI1:")
    roi2 = Cpt(ROIPlugin_V26, "ROI2:")
    roi3 = Cpt(ROIPlugin_V26, "ROI3:")
    roi4 = Cpt(ROIPlugin_V26, "ROI4:")
    roistat1 = Cpt(ROIStatPlugin_V23, "ROIStat1:")
    stats1 = Cpt(StatsPlugin_V22, "Stats1:")
    stats2 = Cpt(StatsPlugin_V22, "Stats2:")
    stats3 = Cpt(StatsPlugin_V22, "Stats3:")
    stats4 = Cpt(StatsPlugin_V22, "Stats4:")
    stats5 = Cpt(StatsPlugin_V22, "Stats5:")
    tiff1 = Cpt(TIFFPlugin, "TIFF1:")
    trans1 = Cpt(TransformPlugin_V21, "Trans1:")
    netcdf1 = Cpt(NetCDFPlugin, "netCDF1:")


class CommonPlugins_V31(CommonPlugins, version=(3, 1)):
    attr1 = Cpt(AttributeNPlugin_V22, "Attr1:")
    cb1 = Cpt(CircularBuffPlugin_V22, "CB1:")
    cc1 = Cpt(ColorConvPlugin, "CC1:")
    cc2 = Cpt(ColorConvPlugin, "CC2:")
    fft1 = Cpt(FFTPlugin_V25, "FFT1:")
    gather1 = Cpt(GatherPlugin_V31, "Gather1:")
    hdf1 = Cpt(HDF5Plugin_V20, "HDF1:")
    jpeg1 = Cpt(JPEGPlugin, "JPEG1:")
    nexus1 = Cpt(NexusPlugin, "Nexus1:")
    over1 = Cpt(Overlay_V21, "Over1:")
    proc1 = Cpt(ProcessPlugin, "Proc1:")
    roi1 = Cpt(ROIPlugin_V26, "ROI1:")
    roi2 = Cpt(ROIPlugin_V26, "ROI2:")
    roi3 = Cpt(ROIPlugin_V26, "ROI3:")
    roi4 = Cpt(ROIPlugin_V26, "ROI4:")
    roistat1 = Cpt(ROIStatPlugin_V23, "ROIStat1:")
    scatter1 = Cpt(ScatterPlugin_V31, "Scatter1:")
    stats1 = Cpt(StatsPlugin_V22, "Stats1:")
    stats2 = Cpt(StatsPlugin_V22, "Stats2:")
    stats3 = Cpt(StatsPlugin_V22, "Stats3:")
    stats4 = Cpt(StatsPlugin_V22, "Stats4:")
    stats5 = Cpt(StatsPlugin_V22, "Stats5:")
    tiff1 = Cpt(TIFFPlugin, "TIFF1:")
    trans1 = Cpt(TransformPlugin_V21, "Trans1:")
    netcdf1 = Cpt(NetCDFPlugin, "netCDF1:")


class CommonPlugins_V32(CommonPlugins, version=(3, 2)):
    attr1 = Cpt(AttributeNPlugin_V22, "Attr1:")
    cb1 = Cpt(CircularBuffPlugin_V22, "CB1:")
    cc1 = Cpt(ColorConvPlugin, "CC1:")
    cc2 = Cpt(ColorConvPlugin, "CC2:")
    fft1 = Cpt(FFTPlugin_V25, "FFT1:")
    gather1 = Cpt(GatherPlugin_V31, "Gather1:")
    hdf1 = Cpt(HDF5Plugin_V20, "HDF1:")
    jpeg1 = Cpt(JPEGPlugin, "JPEG1:")
    nexus1 = Cpt(NexusPlugin, "Nexus1:")
    over1 = Cpt(Overlay_V21, "Over1:")
    proc1 = Cpt(ProcessPlugin, "Proc1:")
    roi1 = Cpt(ROIPlugin_V26, "ROI1:")
    roi2 = Cpt(ROIPlugin_V26, "ROI2:")
    roi3 = Cpt(ROIPlugin_V26, "ROI3:")
    roi4 = Cpt(ROIPlugin_V26, "ROI4:")
    roistat1 = Cpt(ROIStatPlugin_V23, "ROIStat1:")
    scatter1 = Cpt(ScatterPlugin_V32, "Scatter1:")
    stats1 = Cpt(StatsPlugin_V22, "Stats1:")
    stats2 = Cpt(StatsPlugin_V22, "Stats2:")
    stats3 = Cpt(StatsPlugin_V22, "Stats3:")
    stats4 = Cpt(StatsPlugin_V22, "Stats4:")
    stats5 = Cpt(StatsPlugin_V22, "Stats5:")
    tiff1 = Cpt(TIFFPlugin, "TIFF1:")
    trans1 = Cpt(TransformPlugin_V21, "Trans1:")
    netcdf1 = Cpt(NetCDFPlugin, "netCDF1:")


class CommonPlugins_V33(CommonPlugins, version=(3, 3)):
    attr1 = Cpt(AttributeNPlugin_V22, "Attr1:")
    cb1 = Cpt(CircularBuffPlugin_V22, "CB1:")
    cc1 = Cpt(ColorConvPlugin, "CC1:")
    cc2 = Cpt(ColorConvPlugin, "CC2:")
    fft1 = Cpt(FFTPlugin_V25, "FFT1:")
    gather1 = Cpt(GatherPlugin_V31, "Gather1:")
    hdf1 = Cpt(HDF5Plugin_V20, "HDF1:")
    jpeg1 = Cpt(JPEGPlugin, "JPEG1:")
    nexus1 = Cpt(NexusPlugin, "Nexus1:")
    over1 = Cpt(Overlay_V21, "Over1:")
    proc1 = Cpt(ProcessPlugin_V33, "Proc1:")
    roi1 = Cpt(ROIPlugin_V26, "ROI1:")
    roi2 = Cpt(ROIPlugin_V26, "ROI2:")
    roi3 = Cpt(ROIPlugin_V26, "ROI3:")
    roi4 = Cpt(ROIPlugin_V26, "ROI4:")
    roistat1 = Cpt(ROIStatPlugin_V23, "ROIStat1:")
    scatter1 = Cpt(ScatterPlugin_V32, "Scatter1:")
    stats1 = Cpt(StatsPlugin_V22, "Stats1:")
    stats2 = Cpt(StatsPlugin_V22, "Stats2:")
    stats3 = Cpt(StatsPlugin_V22, "Stats3:")
    stats4 = Cpt(StatsPlugin_V22, "Stats4:")
    stats5 = Cpt(StatsPlugin_V22, "Stats5:")
    tiff1 = Cpt(TIFFPlugin, "TIFF1:")
    trans1 = Cpt(TransformPlugin_V21, "Trans1:")
    netcdf1 = Cpt(NetCDFPlugin, "netCDF1:")


class CommonPlugins_V331(CommonPlugins, version=(3, 3, 1)):
    attr1 = Cpt(AttributeNPlugin_V22, "Attr1:")
    cb1 = Cpt(CircularBuffPlugin_V22, "CB1:")
    cc1 = Cpt(ColorConvPlugin, "CC1:")
    cc2 = Cpt(ColorConvPlugin, "CC2:")
    fft1 = Cpt(FFTPlugin_V25, "FFT1:")
    gather1 = Cpt(GatherPlugin_V31, "Gather1:")
    hdf1 = Cpt(HDF5Plugin_V20, "HDF1:")
    jpeg1 = Cpt(JPEGPlugin, "JPEG1:")
    nexus1 = Cpt(NexusPlugin, "Nexus1:")
    over1 = Cpt(Overlay_V21, "Over1:")
    proc1 = Cpt(ProcessPlugin_V33, "Proc1:")
    roi1 = Cpt(ROIPlugin_V26, "ROI1:")
    roi2 = Cpt(ROIPlugin_V26, "ROI2:")
    roi3 = Cpt(ROIPlugin_V26, "ROI3:")
    roi4 = Cpt(ROIPlugin_V26, "ROI4:")
    roistat1 = Cpt(ROIStatPlugin_V23, "ROIStat1:")
    scatter1 = Cpt(ScatterPlugin_V32, "Scatter1:")
    stats1 = Cpt(StatsPlugin_V22, "Stats1:")
    stats2 = Cpt(StatsPlugin_V22, "Stats2:")
    stats3 = Cpt(StatsPlugin_V22, "Stats3:")
    stats4 = Cpt(StatsPlugin_V22, "Stats4:")
    stats5 = Cpt(StatsPlugin_V22, "Stats5:")
    tiff1 = Cpt(TIFFPlugin, "TIFF1:")
    trans1 = Cpt(TransformPlugin_V21, "Trans1:")
    netcdf1 = Cpt(NetCDFPlugin, "netCDF1:")


class CommonPlugins_V332(CommonPlugins, version=(3, 3, 2)):
    attr1 = Cpt(AttributeNPlugin_V22, "Attr1:")
    cb1 = Cpt(CircularBuffPlugin_V22, "CB1:")
    cc1 = Cpt(ColorConvPlugin, "CC1:")
    cc2 = Cpt(ColorConvPlugin, "CC2:")
    fft1 = Cpt(FFTPlugin_V25, "FFT1:")
    gather1 = Cpt(GatherPlugin_V31, "Gather1:")
    hdf1 = Cpt(HDF5Plugin_V20, "HDF1:")
    jpeg1 = Cpt(JPEGPlugin, "JPEG1:")
    nexus1 = Cpt(NexusPlugin, "Nexus1:")
    over1 = Cpt(Overlay_V21, "Over1:")
    proc1 = Cpt(ProcessPlugin_V33, "Proc1:")
    roi1 = Cpt(ROIPlugin_V26, "ROI1:")
    roi2 = Cpt(ROIPlugin_V26, "ROI2:")
    roi3 = Cpt(ROIPlugin_V26, "ROI3:")
    roi4 = Cpt(ROIPlugin_V26, "ROI4:")
    roistat1 = Cpt(ROIStatPlugin_V23, "ROIStat1:")
    scatter1 = Cpt(ScatterPlugin_V32, "Scatter1:")
    stats1 = Cpt(StatsPlugin_V22, "Stats1:")
    stats2 = Cpt(StatsPlugin_V22, "Stats2:")
    stats3 = Cpt(StatsPlugin_V22, "Stats3:")
    stats4 = Cpt(StatsPlugin_V22, "Stats4:")
    stats5 = Cpt(StatsPlugin_V22, "Stats5:")
    tiff1 = Cpt(TIFFPlugin, "TIFF1:")
    trans1 = Cpt(TransformPlugin_V21, "Trans1:")
    netcdf1 = Cpt(NetCDFPlugin, "netCDF1:")


class CommonPlugins_V34(CommonPlugins, version=(3, 4)):
    attr1 = Cpt(AttributeNPlugin_V22, "Attr1:")
    cb1 = Cpt(CircularBuffPlugin_V34, "CB1:")
    cc1 = Cpt(ColorConvPlugin, "CC1:")
    cc2 = Cpt(ColorConvPlugin, "CC2:")
    codec1 = Cpt(CodecPlugin_V34, "Codec1:")
    codec2 = Cpt(CodecPlugin_V34, "Codec2:")
    fft1 = Cpt(FFTPlugin_V25, "FFT1:")
    gather1 = Cpt(GatherPlugin_V31, "Gather1:")
    hdf1 = Cpt(HDF5Plugin_V20, "HDF1:")
    jpeg1 = Cpt(JPEGPlugin, "JPEG1:")
    nexus1 = Cpt(NexusPlugin, "Nexus1:")
    over1 = Cpt(Overlay_V21, "Over1:")
    proc1 = Cpt(ProcessPlugin_V33, "Proc1:")
    roi1 = Cpt(ROIPlugin_V26, "ROI1:")
    roi2 = Cpt(ROIPlugin_V26, "ROI2:")
    roi3 = Cpt(ROIPlugin_V26, "ROI3:")
    roi4 = Cpt(ROIPlugin_V26, "ROI4:")
    roistat1 = Cpt(ROIStatPlugin_V23, "ROIStat1:")
    scatter1 = Cpt(ScatterPlugin_V32, "Scatter1:")
    stats1 = Cpt(StatsPlugin_V22, "Stats1:")
    stats2 = Cpt(StatsPlugin_V22, "Stats2:")
    stats3 = Cpt(StatsPlugin_V22, "Stats3:")
    stats4 = Cpt(StatsPlugin_V22, "Stats4:")
    stats5 = Cpt(StatsPlugin_V22, "Stats5:")
    tiff1 = Cpt(TIFFPlugin, "TIFF1:")
    trans1 = Cpt(TransformPlugin_V21, "Trans1:")
    netcdf1 = Cpt(NetCDFPlugin, "netCDF1:")
