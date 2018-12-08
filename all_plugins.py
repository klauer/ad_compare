# --- NDColorConvert.template ---
from ophyd import (
    Component as Cpt,
    DynamicDeviceComponent as DDC,
    EpicsSignal,
    EpicsSignalRO,
)
from ophyd.areadetector.plugins import (
    PluginBase,
    Overlay,
    ColorConvPlugin,
    FilePlugin,
    HDF5Plugin,
    ImagePlugin,
    JPEGPlugin,
    MagickPlugin,
    NetCDFPlugin,
    NexusPlugin,
    OverlayPlugin,
    ProcessPlugin,
    ROIPlugin,
    StatsPlugin,
    TIFFPlugin,
    TransformPlugin,
)
from ophyd.areadetector import EpicsSignalWithRBV as SignalWithRBV, ad_group


def DDC_EpicsSignal(*items, **kw):
    return DDC(ad_group(EpicsSignal, items), **kw)


def DDC_EpicsSignalRO(*items, **kw):
    return DDC(ad_group(EpicsSignalRO, items), **kw)


def DDC_SignalWithRBV(*items, **kw):
    return DDC(ad_group(SignalWithRBV, items), **kw)


class PluginBase_V20(PluginBase):
    epics_ts_sec = Cpt(SignalWithRBV, "EpicsTSSec")
    epics_ts_nsec = Cpt(SignalWithRBV, "EpicsTSNsec")


class FilePlugin_V20(FilePlugin, PluginBase_V20):
    ...


class FilePlugin_V21(FilePlugin_V20):
    lazy_open = Cpt(SignalWithRBV, "LazyOpen", string=True, doc="0='No' 1='Yes'")


class FilePlugin_V22(FilePlugin_V21):
    create_directory = Cpt(SignalWithRBV, "CreateDirectory")
    file_number = Cpt(SignalWithRBV, "FileNumber")
    file_number_sync = None  # REMOVED
    file_number_write = None  # REMOVED
    temp_suffix = Cpt(SignalWithRBV, "TempSuffix", string=True)


class GatherPlugin_V31(PluginBase_V20, version=(3, 1)):
    ...


# --- NDFileHDF5.template ---


class HDF5Plugin_V20(HDF5Plugin, FilePlugin_V20, version=(2, 0)):
    data_bits_offset = Cpt(SignalWithRBV, "DataBitsOffset")
    io_speed = Cpt(EpicsSignal, "IOSpeed")
    num_data_bits = Cpt(SignalWithRBV, "NumDataBits")
    num_frames_flush = Cpt(SignalWithRBV, "NumFramesFlush")
    run_time = Cpt(EpicsSignal, "RunTime")
    szip_num_pixels = Cpt(SignalWithRBV, "SZipNumPixels")
    store_attr = Cpt(SignalWithRBV, "StoreAttr", string=True, doc="0='No' 1='Yes'")
    store_perform = Cpt(
        SignalWithRBV, "StorePerform", string=True, doc="0='No' 1='Yes'"
    )
    zlevel = Cpt(SignalWithRBV, "ZLevel", string=True, doc="0='No' 1='Yes'")
    extra_dim_name = DDC_EpicsSignalRO(
        ("extra_dim_name_x", "ExtraDimNameX_RBV"),
        ("extra_dim_name_y", "ExtraDimNameY_RBV"),
        ("extra_dim_name_n", "ExtraDimNameN_RBV"),
        doc="extra_dim_name",
        default_read_attrs=["extra_dim_name_x", "extra_dim_name_y", "extra_dim_name_n"],
    )


class HDF5Plugin_V21(HDF5Plugin_V20, FilePlugin_V21, version=(2, 1)):
    xml_error_msg = Cpt(EpicsSignalRO, "XMLErrorMsg_RBV")
    xml_file_name = Cpt(SignalWithRBV, "XMLFileName")
    xml_valid = Cpt(EpicsSignalRO, "XMLValid_RBV", string=True, doc="0='No' 1='Yes'")


class HDF5Plugin_V22(HDF5Plugin_V21, FilePlugin_V22, version=(2, 2)):
    nd_attribute_chunk = Cpt(SignalWithRBV, "NDAttributeChunk")


class HDF5Plugin_V25(HDF5Plugin_V22, version=(2, 5)):
    dim_att_datasets = Cpt(
        SignalWithRBV, "DimAttDatasets", string=True, doc="0='No' 1='Yes'"
    )
    fill_value = Cpt(SignalWithRBV, "FillValue", string=True, doc="0='No' 1='Yes'")
    position_mode = Cpt(
        SignalWithRBV, "PositionMode", string=True, doc="0='Off' 1='On'"
    )
    swmr_active = Cpt(
        EpicsSignalRO, "SWMRActive_RBV", string=True, doc="0='Off' 1='Active'"
    )
    swmr_cb_counter = Cpt(
        EpicsSignalRO, "SWMRCbCounter_RBV", string=True, doc="0='Off' 1='Active'"
    )
    swmr_mode = Cpt(SignalWithRBV, "SWMRMode", string=True, doc="0='Off' 1='On'")
    swmr_supported = Cpt(
        EpicsSignalRO,
        "SWMRSupported_RBV",
        string=True,
        doc="0='Not Supported' 1='Supported'",
    )
    extra_dim_chunk = DDC_SignalWithRBV(
        ("extra_dim_chunk3", "ExtraDimChunk3"),
        ("extra_dim_chunk4", "ExtraDimChunk4"),
        ("extra_dim_chunk5", "ExtraDimChunk5"),
        ("extra_dim_chunk6", "ExtraDimChunk6"),
        ("extra_dim_chunk7", "ExtraDimChunk7"),
        ("extra_dim_chunk8", "ExtraDimChunk8"),
        ("extra_dim_chunk9", "ExtraDimChunk9"),
        doc="extra_dim_chunk",
        default_read_attrs=[
            "extra_dim_chunk3",
            "extra_dim_chunk4",
            "extra_dim_chunk5",
            "extra_dim_chunk6",
            "extra_dim_chunk7",
            "extra_dim_chunk8",
            "extra_dim_chunk9",
        ],
    )
    extra_dim_chunk = DDC_SignalWithRBV(
        ("extra_dim_chunk_x", "ExtraDimChunkX"),
        ("extra_dim_chunk_y", "ExtraDimChunkY"),
        doc="extra_dim_chunk",
        default_read_attrs=["extra_dim_chunk_x", "extra_dim_chunk_y"],
    )
    extra_dim_name = DDC_EpicsSignalRO(
        ("extra_dim_name3", "ExtraDimName3_RBV"),
        ("extra_dim_name4", "ExtraDimName4_RBV"),
        ("extra_dim_name5", "ExtraDimName5_RBV"),
        ("extra_dim_name6", "ExtraDimName6_RBV"),
        ("extra_dim_name7", "ExtraDimName7_RBV"),
        ("extra_dim_name8", "ExtraDimName8_RBV"),
        ("extra_dim_name9", "ExtraDimName9_RBV"),
        doc="extra_dim_name",
        default_read_attrs=[
            "extra_dim_name3",
            "extra_dim_name4",
            "extra_dim_name5",
            "extra_dim_name6",
            "extra_dim_name7",
            "extra_dim_name8",
            "extra_dim_name9",
        ],
    )
    extra_dim_size = DDC_SignalWithRBV(
        ("extra_dim_size3", "ExtraDimSize3"),
        ("extra_dim_size4", "ExtraDimSize4"),
        ("extra_dim_size5", "ExtraDimSize5"),
        ("extra_dim_size6", "ExtraDimSize6"),
        ("extra_dim_size7", "ExtraDimSize7"),
        ("extra_dim_size8", "ExtraDimSize8"),
        ("extra_dim_size9", "ExtraDimSize9"),
        doc="extra_dim_size",
        default_read_attrs=[
            "extra_dim_size3",
            "extra_dim_size4",
            "extra_dim_size5",
            "extra_dim_size6",
            "extra_dim_size7",
            "extra_dim_size8",
            "extra_dim_size9",
        ],
    )
    pos_index_dim = DDC_SignalWithRBV(
        ("pos_index_dim3", "PosIndexDim3"),
        ("pos_index_dim4", "PosIndexDim4"),
        ("pos_index_dim5", "PosIndexDim5"),
        ("pos_index_dim6", "PosIndexDim6"),
        ("pos_index_dim7", "PosIndexDim7"),
        ("pos_index_dim8", "PosIndexDim8"),
        ("pos_index_dim9", "PosIndexDim9"),
        doc="pos_index_dim",
        default_read_attrs=[
            "pos_index_dim3",
            "pos_index_dim4",
            "pos_index_dim5",
            "pos_index_dim6",
            "pos_index_dim7",
            "pos_index_dim8",
            "pos_index_dim9",
        ],
    )
    pos_index_dim = DDC_SignalWithRBV(
        ("pos_index_dim_x", "PosIndexDimX"),
        ("pos_index_dim_y", "PosIndexDimY"),
        ("pos_index_dim_n", "PosIndexDimN"),
        doc="pos_index_dim",
        default_read_attrs=["pos_index_dim_x", "pos_index_dim_y", "pos_index_dim_n"],
    )
    pos_name_dim = DDC_SignalWithRBV(
        ("pos_name_dim3", "PosNameDim3"),
        ("pos_name_dim4", "PosNameDim4"),
        ("pos_name_dim5", "PosNameDim5"),
        ("pos_name_dim6", "PosNameDim6"),
        ("pos_name_dim7", "PosNameDim7"),
        ("pos_name_dim8", "PosNameDim8"),
        ("pos_name_dim9", "PosNameDim9"),
        doc="pos_name_dim",
        default_read_attrs=[
            "pos_name_dim3",
            "pos_name_dim4",
            "pos_name_dim5",
            "pos_name_dim6",
            "pos_name_dim7",
            "pos_name_dim8",
            "pos_name_dim9",
        ],
    )
    pos_name_dim = DDC_SignalWithRBV(
        ("pos_name_dim_x", "PosNameDimX"),
        ("pos_name_dim_y", "PosNameDimY"),
        ("pos_name_dim_n", "PosNameDimN"),
        doc="pos_name_dim",
        default_read_attrs=["pos_name_dim_x", "pos_name_dim_y", "pos_name_dim_n"],
    )


class HDF5Plugin_V32(HDF5Plugin_V25, version=(3, 2)):
    blosc_compressor = Cpt(
        SignalWithRBV,
        "BloscCompressor",
        string=True,
        doc="0='blosclz' 1='lz4' 2='lz4hc' 3='snappy' 4='zlib' 5='zstd'",
    )
    blosc_level = Cpt(
        SignalWithRBV,
        "BloscLevel",
        string=True,
        doc="0='blosclz' 1='lz4' 2='lz4hc' 3='snappy' 4='zlib' 5='zstd'",
    )
    blosc_shuffle = Cpt(
        SignalWithRBV,
        "BloscShuffle",
        string=True,
        doc="0='None' 1='ByteShuffle' 2='BitShuffle'",
    )
    compression = Cpt(
        SignalWithRBV,
        "Compression",
        string=True,
        doc="0='None' 1='N-bit' 2='szip' 3='zlib' 4='blosc'",
    )
    io_speed = Cpt(
        EpicsSignal,
        "IOSpeed",
        string=True,
        doc="0='None' 1='N-bit' 2='szip' 3='zlib' 4='blosc'",
    )
    run_time = Cpt(
        EpicsSignal,
        "RunTime",
        string=True,
        doc="0='None' 1='N-bit' 2='szip' 3='zlib' 4='blosc'",
    )
    swmr_active = Cpt(
        EpicsSignalRO, "SWMRActive_RBV", string=True, doc="0='Off' 1='Active'"
    )
    swmr_cb_counter = Cpt(
        EpicsSignalRO, "SWMRCbCounter_RBV", string=True, doc="0='Off' 1='Active'"
    )
    swmr_supported = Cpt(
        EpicsSignalRO,
        "SWMRSupported_RBV",
        string=True,
        doc="0='Not Supported' 1='Supported'",
    )
    extra_dim_name = DDC_EpicsSignalRO(
        ("extra_dim_name3", "ExtraDimName3_RBV"),
        ("extra_dim_name4", "ExtraDimName4_RBV"),
        ("extra_dim_name5", "ExtraDimName5_RBV"),
        ("extra_dim_name6", "ExtraDimName6_RBV"),
        ("extra_dim_name7", "ExtraDimName7_RBV"),
        ("extra_dim_name8", "ExtraDimName8_RBV"),
        ("extra_dim_name9", "ExtraDimName9_RBV"),
        doc="extra_dim_name",
        default_read_attrs=[
            "extra_dim_name3",
            "extra_dim_name4",
            "extra_dim_name5",
            "extra_dim_name6",
            "extra_dim_name7",
            "extra_dim_name8",
            "extra_dim_name9",
        ],
    )
    extra_dim_name = DDC_EpicsSignalRO(
        ("extra_dim_name_x", "ExtraDimNameX_RBV"),
        ("extra_dim_name_y", "ExtraDimNameY_RBV"),
        ("extra_dim_name_n", "ExtraDimNameN_RBV"),
        doc="extra_dim_name",
        default_read_attrs=["extra_dim_name_x", "extra_dim_name_y", "extra_dim_name_n"],
    )


# --- NDStdArrays.template ---


# --- NDFileJPEG.template ---
class JPEGPlugin_V20(JPEGPlugin, FilePlugin_V20, version=(2, 0)):
    ...


class JPEGPlugin_V21(JPEGPlugin_V20, FilePlugin_V21, version=(2, 1)):
    ...


class JPEGPlugin_V22(JPEGPlugin_V21, FilePlugin_V22, version=(2, 2)):
    ...


# --- NDFileMagick.template ---
class MagickPlugin_V20(MagickPlugin, FilePlugin_V20, version=(2, 0)):
    ...


class MagickPlugin_V21(MagickPlugin_V20, FilePlugin_V21, version=(2, 1)):
    ...


class MagickPlugin_V22(MagickPlugin_V21, FilePlugin_V22, version=(2, 2)):
    ...


class MagickPlugin_V31(MagickPlugin_V22, version=(3, 1)):
    bit_depth = Cpt(
        SignalWithRBV, "BitDepth", string=True, doc="1='1' 8='8' 16='16' 32='32'"
    )


# --- NDFileNetCDF.template ---
class NetCDFPlugin_V20(NetCDFPlugin, FilePlugin_V20, version=(2, 0)):
    ...


class NetCDFPlugin_V21(NetCDFPlugin_V20, FilePlugin_V21, version=(2, 1)):
    ...


class NetCDFPlugin_V22(NetCDFPlugin_V21, FilePlugin_V22, version=(2, 2)):
    ...


# --- NDFileNexus.template ---
class NexusPlugin_V20(NexusPlugin, FilePlugin_V20, version=(2, 0)):
    ...


class NexusPlugin_V21(NexusPlugin_V20, FilePlugin_V21, version=(2, 1)):
    ...


class NexusPlugin_V22(NexusPlugin_V21, FilePlugin_V22, version=(2, 2)):
    ...


# --- NDOverlayN.template ---


class Overlay_V21(Overlay, version=(2, 1)):
    display_text = Cpt(SignalWithRBV, "DisplayText")
    font = Cpt(
        SignalWithRBV,
        "Font",
        string=True,
        doc="0='6x13' 1='6x13 Bold' 2='9x15' 3='9x15 Bold'",
    )
    shape = Cpt(
        SignalWithRBV, "Shape", string=True, doc="0='Cross' 1='Rectangle' 2='Text'"
    )
    time_stamp_format = Cpt(SignalWithRBV, "TimeStampFormat", string=True)
    width = DDC_SignalWithRBV(
        ("width_x", "WidthX"),
        ("width_y", "WidthY"),
        doc="width",
        default_read_attrs=["width_x", "width_y"],
    )
    width_link = DDC_EpicsSignal(
        ("width_xlink", "WidthXLink"),
        ("width_ylink", "WidthYLink"),
        doc="width_link",
        default_read_attrs=["width_xlink", "width_ylink"],
    )


class Overlay_V26(Overlay_V21, version=(2, 6)):
    shape = Cpt(
        SignalWithRBV,
        "Shape",
        string=True,
        doc="0='Cross' 1='Rectangle' 3='Ellipse' 2='Text'",
    )
    center = DDC_SignalWithRBV(
        ("center_x", "CenterX"),
        ("center_y", "CenterY"),
        doc="center",
        default_read_attrs=["center_x", "center_y"],
    )
    center_link = DDC_EpicsSignal(
        ("center_xlink", "CenterXLink"),
        ("center_ylink", "CenterYLink"),
        doc="center_link",
        default_read_attrs=["center_xlink", "center_ylink"],
    )
    position_x = DDC_SignalWithRBV(
        ("position_x", "PositionX"),
        ("position_y", "PositionY"),
        doc="position",
        default_read_attrs=["position_x", "position_y"],
    )
    set_xhopr = DDC_EpicsSignal(
        ("set_xhopr", "SetXHOPR"),
        ("set_yhopr", "SetYHOPR"),
        doc="set_hopr",
        default_read_attrs=["set_xhopr", "set_yhopr"],
    )
    width = DDC_SignalWithRBV(
        ("width_x", "WidthX"),
        ("width_y", "WidthY"),
        doc="width",
        default_read_attrs=["width_x", "width_y"],
    )


class Overlay_V31(Overlay_V26, version=(3, 1)):
    center = DDC_SignalWithRBV(
        ("center_x", "CenterX"),
        ("center_y", "CenterY"),
        doc="center",
        default_read_attrs=["center_x", "center_y"],
    )


# --- NDOverlay.template ---


# --- NDProcess.template ---


class ProcessPlugin_V33(ProcessPlugin, PluginBase_V20, version=(3, 3)):
    port_backup = Cpt(EpicsSignal, "PortBackup", string=True)
    read_background_tiffs_eq = Cpt(EpicsSignal, "ReadBackgroundTIFFSeq", string=True)
    read_flat_field_tiffs_eq = Cpt(EpicsSignal, "ReadFlatFieldTIFFSeq", string=True)


# --- NDROI.template ---


class ROIPlugin_V26(ROIPlugin, PluginBase_V20, version=(2, 6)):
    collapse_dims = Cpt(
        SignalWithRBV, "CollapseDims", string=True, doc="0='Disable' 1='Enable'"
    )


# --- NDROIStat.template ---


class ROIStatPlugin_V22(PluginBase, version=(2, 2)):
    reset_all = Cpt(EpicsSignal, "ResetAll", string=True, doc="")


class ROIStatPlugin_V23(ROIStatPlugin_V22, PluginBase_V20, version=(2, 3)):
    ts_acquiring = Cpt(
        EpicsSignal, "TSAcquiring", string=True, doc="0='Done' 1='Acquiring'"
    )
    ts_control = Cpt(
        EpicsSignal,
        "TSControl",
        string=True,
        doc="0='Erase/Start' 1='Start' 2='Stop' 3='Read'",
    )
    ts_current_point = Cpt(
        EpicsSignal,
        "TSCurrentPoint",
        string=True,
        doc="0='Erase/Start' 1='Start' 2='Stop' 3='Read'",
    )
    ts_num_points = Cpt(
        EpicsSignal,
        "TSNumPoints",
        string=True,
        doc="0='Erase/Start' 1='Start' 2='Stop' 3='Read'",
    )
    ts_read = Cpt(
        EpicsSignal,
        "TSRead",
        string=True,
        doc="0='Erase/Start' 1='Start' 2='Stop' 3='Read'",
    )


# --- NDStats.template ---


class StatsPlugin_V22(StatsPlugin, PluginBase_V20, version=(2, 2)):
    hist_entropy = Cpt(SignalWithRBV, "HistEntropy")
    max_value = Cpt(SignalWithRBV, "MaxValue")
    mean_value = Cpt(SignalWithRBV, "MeanValue")
    min_value = Cpt(SignalWithRBV, "MinValue")
    net = Cpt(SignalWithRBV, "Net")
    reset = Cpt(EpicsSignal, "Reset")
    sigma_value = Cpt(EpicsSignal, "SigmaValue")
    sigma_xy = Cpt(SignalWithRBV, "SigmaXY")
    total = Cpt(SignalWithRBV, "Total")
    centroid = DDC_SignalWithRBV(
        ("centroid_x", "CentroidX"),
        ("centroid_y", "CentroidY"),
        doc="centroid",
        default_read_attrs=["centroid_x", "centroid_y"],
    )
    max = DDC_SignalWithRBV(
        ("max_x", "MaxX"),
        ("max_y", "MaxY"),
        doc="max",
        default_read_attrs=["max_x", "max_y"],
    )
    min = DDC_SignalWithRBV(
        ("min_x", "MinX"),
        ("min_y", "MinY"),
        doc="min",
        default_read_attrs=["min_x", "min_y"],
    )
    reset = DDC_EpicsSignal(
        ("reset1", "Reset1"),
        ("reset2", "Reset2"),
        doc="reset",
        default_read_attrs=["reset1", "reset2"],
    )
    sigma = DDC_SignalWithRBV(
        ("sigma_x", "SigmaX"),
        ("sigma_y", "SigmaY"),
        doc="sigma",
        default_read_attrs=["sigma_x", "sigma_y"],
    )


class StatsPlugin_V25(StatsPlugin_V22, PluginBase_V20, version=(2, 5)):
    ts_timestamp = Cpt(EpicsSignal, "TSTimestamp")


class StatsPlugin_V26(StatsPlugin_V25, PluginBase_V20, version=(2, 6)):
    centroid_total = Cpt(SignalWithRBV, "CentroidTotal")
    eccentricity = Cpt(SignalWithRBV, "Eccentricity")
    hist_above = Cpt(SignalWithRBV, "HistAbove")
    hist_below = Cpt(SignalWithRBV, "HistBelow")
    orientation = Cpt(SignalWithRBV, "Orientation")
    reset = Cpt(EpicsSignal, "Reset")
    ts_centroid_total = Cpt(EpicsSignal, "TSCentroidTotal")
    ts_eccentricity = Cpt(EpicsSignal, "TSEccentricity")
    ts_orientation = Cpt(EpicsSignal, "TSOrientation")
    kurtosis = DDC_SignalWithRBV(
        ("kurtosis_x", "KurtosisX"),
        ("kurtosis_y", "KurtosisY"),
        doc="kurtosis",
        default_read_attrs=["kurtosis_x", "kurtosis_y"],
    )
    reset = DDC_EpicsSignal(
        ("reset1", "Reset1"),
        ("reset2", "Reset2"),
        doc="reset",
        default_read_attrs=["reset1", "reset2"],
    )
    skew = DDC_SignalWithRBV(
        ("skew_x", "SkewX"),
        ("skew_y", "SkewY"),
        doc="skew",
        default_read_attrs=["skew_x", "skew_y"],
    )
    ts_kurtosis = DDC_EpicsSignal(
        ("ts_kurtosis_x", "TSKurtosisX"),
        ("ts_kurtosis_y", "TSKurtosisY"),
        doc="ts_kurtosis",
        default_read_attrs=["ts_kurtosis_x", "ts_kurtosis_y"],
    )
    ts_skew = DDC_EpicsSignal(
        ("ts_skew_x", "TSSkewX"),
        ("ts_skew_y", "TSSkewY"),
        doc="ts_skew",
        default_read_attrs=["ts_skew_x", "ts_skew_y"],
    )


class StatsPlugin_V32(StatsPlugin_V26, PluginBase_V20, version=(3, 2)):
    histogram_x = Cpt(EpicsSignalRO, "HistogramX_RBV")


class StatsPlugin_V33(StatsPlugin_V32, PluginBase_V20, version=(3, 3)):
    ts_acquiring = None  # REMOVED
    ts_centroid_total = Cpt(EpicsSignal, "TSCentroidTotal")
    ts_control = None  # REMOVED
    ts_current_point = None  # REMOVED
    ts_eccentricity = Cpt(EpicsSignal, "TSEccentricity")
    ts_max_value = Cpt(EpicsSignal, "TSMaxValue")
    ts_mean_value = Cpt(EpicsSignal, "TSMeanValue")
    ts_min_value = Cpt(EpicsSignal, "TSMinValue")
    ts_net = Cpt(EpicsSignal, "TSNet")
    ts_num_points = None  # REMOVED
    ts_orientation = Cpt(EpicsSignal, "TSOrientation")
    ts_read = None  # REMOVED
    ts_sigma = Cpt(EpicsSignal, "TSSigma")
    ts_sigma_xy = Cpt(EpicsSignal, "TSSigmaXY")
    ts_timestamp = Cpt(EpicsSignal, "TSTimestamp")
    ts_total = Cpt(EpicsSignal, "TSTotal")
    ts_centroid = DDC_EpicsSignal(
        ("ts_centroid_x", "TSCentroidX"),
        ("ts_centroid_y", "TSCentroidY"),
        doc="ts_centroid",
        default_read_attrs=["ts_centroid_x", "ts_centroid_y"],
    )
    ts_kurtosis = DDC_EpicsSignal(
        ("ts_kurtosis_x", "TSKurtosisX"),
        ("ts_kurtosis_y", "TSKurtosisY"),
        doc="ts_kurtosis",
        default_read_attrs=["ts_kurtosis_x", "ts_kurtosis_y"],
    )
    ts_max = DDC_EpicsSignal(
        ("ts_max_x", "TSMaxX"),
        ("ts_max_y", "TSMaxY"),
        doc="ts_max",
        default_read_attrs=["ts_max_x", "ts_max_y"],
    )
    ts_min = DDC_EpicsSignal(
        ("ts_min_x", "TSMinX"),
        ("ts_min_y", "TSMinY"),
        doc="ts_min",
        default_read_attrs=["ts_min_x", "ts_min_y"],
    )
    ts_sigma_x = DDC_EpicsSignal(
        ("ts_sigma_x", "TSSigmaX"),
        ("ts_sigma_y", "TSSigmaY"),
        doc="ts_sigma",
        default_read_attrs=["ts_sigma_x", "ts_sigma_y"],
    )
    ts_skew = DDC_EpicsSignal(
        ("ts_skew_x", "TSSkewX"),
        ("ts_skew_y", "TSSkewY"),
        doc="ts_skew",
        default_read_attrs=["ts_skew_x", "ts_skew_y"],
    )


# --- NDFileTIFF.template ---
class TIFFPlugin_V20(TIFFPlugin, FilePlugin_V20, version=(2, 0)):
    ...


class TIFFPlugin_V21(TIFFPlugin_V20, FilePlugin_V21, version=(2, 1)):
    ...


class TIFFPlugin_V22(TIFFPlugin_V21, FilePlugin_V22, version=(2, 2)):
    ...


# --- NDTransform.template ---


class TransformPlugin_V21(TransformPlugin, PluginBase_V20, version=(2, 1)):
    name_ = None  # REMOVED
    origin_location = None  # REMOVED
    types = Cpt(
        EpicsSignal,
        "Type",
        string=True,
        doc="0='None' 1='Rot90' 2='Rot180' 3='Rot270' 4='Mirror' 5='Rot90Mirror' 6='Rot180Mirror' 7='Rot270Mirror'",
    )
    width = None  # REMOVED DDC
    t1_max_size = None  # REMOVED DDC
    t2_max_size = None  # REMOVED DDC
    t3_max_size = None  # REMOVED DDC
    t4_max_size = None  # REMOVED DDC


# --- NDPva.template ---


class PvaPlugin_V25(PluginBase, version=(2, 5)):
    pv_name = Cpt(EpicsSignalRO, "PvName_RBV")


# --- NDFFT.template ---


class FFTPlugin_V25(PluginBase, version=(2, 5)):
    fft_abs_value = Cpt(EpicsSignal, "FFTAbsValue")
    fft_direction = Cpt(
        SignalWithRBV,
        "FFTDirection",
        string=True,
        doc="0='Time to freq.' 1='Freq. to time'",
    )
    fft_freq_axis = Cpt(
        EpicsSignal,
        "FFTFreqAxis",
        string=True,
        doc="0='Time to freq.' 1='Freq. to time'",
    )
    fft_imaginary = Cpt(
        EpicsSignal,
        "FFTImaginary",
        string=True,
        doc="0='Time to freq.' 1='Freq. to time'",
    )
    fft_num_average = Cpt(
        SignalWithRBV,
        "FFTNumAverage",
        string=True,
        doc="0='Time to freq.' 1='Freq. to time'",
    )
    fft_num_averaged = Cpt(
        EpicsSignal,
        "FFTNumAveraged",
        string=True,
        doc="0='Time to freq.' 1='Freq. to time'",
    )
    fft_real = Cpt(
        EpicsSignal, "FFTReal", string=True, doc="0='Time to freq.' 1='Freq. to time'"
    )
    fft_reset_average = Cpt(
        EpicsSignal, "FFTResetAverage", string=True, doc="0='Done' 1='Reset'"
    )
    fft_suppress_dc = Cpt(
        SignalWithRBV, "FFTSuppressDC", string=True, doc="0='Disable' 1='Enable'"
    )
    fft_time_axis = Cpt(
        EpicsSignal, "FFTTimeAxis", string=True, doc="0='Disable' 1='Enable'"
    )
    fft_time_per_point = Cpt(
        SignalWithRBV, "FFTTimePerPoint", string=True, doc="0='Disable' 1='Enable'"
    )
    fft_time_per_point_link = Cpt(
        EpicsSignal, "FFTTimePerPointLink", string=True, doc="0='Disable' 1='Enable'"
    )
    fft_time_series = Cpt(
        EpicsSignal, "FFTTimeSeries", string=True, doc="0='Disable' 1='Enable'"
    )
    name_ = Cpt(EpicsSignal, "Name", string=True)


# --- NDScatter.template ---


class ScatterPlugin_V31(PluginBase, version=(3, 1)):
    scatter_method = Cpt(
        SignalWithRBV, "ScatterMethod", string=True, doc="0='Round robin'"
    )


class ScatterPlugin_V32(ScatterPlugin_V31, PluginBase_V20, version=(3, 2)):
    scatter_method = Cpt(
        SignalWithRBV, "ScatterMethod", string=True, doc="0='Round robin'"
    )


# --- NDPosPlugin.template ---


class PosPluginPlugin_V25(PluginBase, version=(2, 5)):
    delete = Cpt(EpicsSignal, "Delete", string=True, doc="")
    duplicate = Cpt(SignalWithRBV, "Duplicate", string=True, doc="")
    expected_id = Cpt(EpicsSignalRO, "ExpectedID_RBV", string=True, doc="")
    file_valid = Cpt(EpicsSignalRO, "FileValid_RBV", string=True, doc="0='No' 1='Yes'")
    filename = Cpt(SignalWithRBV, "Filename", string=True, doc="0='No' 1='Yes'")
    id_difference = Cpt(
        SignalWithRBV, "IDDifference", string=True, doc="0='No' 1='Yes'"
    )
    id_name = Cpt(SignalWithRBV, "IDName", string=True)
    id_start = Cpt(SignalWithRBV, "IDStart", string=True)
    index = Cpt(EpicsSignalRO, "Index_RBV", string=True)
    missing = Cpt(SignalWithRBV, "Missing", string=True)
    mode = Cpt(SignalWithRBV, "Mode", string=True, doc="0='Discard' 1='Keep'")
    position_ = Cpt(EpicsSignalRO, "Position_RBV", string=True)
    qty = Cpt(EpicsSignalRO, "Qty_RBV", string=True)
    reset = Cpt(EpicsSignal, "Reset", string=True, doc="")
    running = Cpt(SignalWithRBV, "Running", string=True, doc="")


# --- NDCircularBuff.template ---


class CircularBuffPlugin_V22(PluginBase, version=(2, 2)):
    actual_trigger_count = Cpt(EpicsSignalRO, "ActualTriggerCount_RBV")
    capture = Cpt(SignalWithRBV, "Capture")
    current_qty = Cpt(EpicsSignalRO, "CurrentQty_RBV")
    post_count = Cpt(SignalWithRBV, "PostCount")
    post_trigger_qty = Cpt(EpicsSignalRO, "PostTriggerQty_RBV")
    pre_count = Cpt(SignalWithRBV, "PreCount")
    preset_trigger_count = Cpt(SignalWithRBV, "PresetTriggerCount")
    status_message = Cpt(EpicsSignal, "StatusMessage", string=True)
    trigger_ = Cpt(SignalWithRBV, "Trigger", string=True)
    trigger_a = Cpt(SignalWithRBV, "TriggerA", string=True)
    trigger_a_val = Cpt(EpicsSignal, "TriggerAVal", string=True)
    trigger_b = Cpt(SignalWithRBV, "TriggerB", string=True)
    trigger_b_val = Cpt(EpicsSignal, "TriggerBVal", string=True)
    trigger_calc = Cpt(SignalWithRBV, "TriggerCalc", string=True)
    trigger_calc_val = Cpt(EpicsSignal, "TriggerCalcVal", string=True)


class CircularBuffPlugin_V34(CircularBuffPlugin_V22, PluginBase_V20, version=(3, 4)):
    flush_on_soft_trg = Cpt(
        SignalWithRBV,
        "FlushOnSoftTrg",
        string=True,
        doc="0='OnNewImage' 1='Immediately'",
    )


# --- NDAttributeN.template ---


class AttributeNPlugin_V22(PluginBase, version=(2, 2)):
    attr_name = Cpt(SignalWithRBV, "AttrName")
    ts_array_value = Cpt(EpicsSignal, "TSArrayValue")
    value_sum = Cpt(EpicsSignalRO, "ValueSum_RBV")
    value = Cpt(EpicsSignalRO, "Value_RBV")


# --- NDAttrPlot.template ---


class AttrPlotPlugin_V31(PluginBase, version=(3, 1)):
    npts = Cpt(EpicsSignal, "NPts")
    reset = Cpt(EpicsSignal, "Reset")


# --- NDTimeSeriesN.template ---


class TimeSeriesNPlugin_V25(PluginBase, version=(2, 5)):
    name_ = Cpt(EpicsSignal, "Name", string=True)
    time_series = Cpt(EpicsSignal, "TimeSeries", string=True)


# --- NDTimeSeries.template ---


class TimeSeriesPlugin_V25(PluginBase, version=(2, 5)):
    ts_acquire = Cpt(EpicsSignal, "TSAcquire")
    ts_acquire_mode = Cpt(
        SignalWithRBV,
        "TSAcquireMode",
        string=True,
        doc="0='Fixed length' 1='Circ. buffer'",
    )
    ts_acquiring = Cpt(
        EpicsSignal, "TSAcquiring", string=True, doc="0='Done' 1='Acquiring'"
    )
    ts_averaging_time = Cpt(
        SignalWithRBV, "TSAveragingTime", string=True, doc="0='Done' 1='Acquiring'"
    )
    ts_current_point = Cpt(
        EpicsSignal, "TSCurrentPoint", string=True, doc="0='Done' 1='Acquiring'"
    )
    ts_elapsed_time = Cpt(
        EpicsSignal, "TSElapsedTime", string=True, doc="0='Done' 1='Acquiring'"
    )
    ts_num_average = Cpt(
        EpicsSignal, "TSNumAverage", string=True, doc="0='Done' 1='Acquiring'"
    )
    ts_num_points = Cpt(
        EpicsSignal, "TSNumPoints", string=True, doc="0='Done' 1='Acquiring'"
    )
    ts_read = Cpt(EpicsSignal, "TSRead", string=True, doc="0='Done' 1='Read'")
    ts_time_axis = Cpt(EpicsSignal, "TSTimeAxis", string=True, doc="0='Done' 1='Read'")
    ts_time_per_point = Cpt(
        SignalWithRBV, "TSTimePerPoint", string=True, doc="0='Done' 1='Read'"
    )
    ts_time_per_point_link = Cpt(
        EpicsSignal, "TSTimePerPointLink", string=True, doc="0='Done' 1='Read'"
    )
    ts_timestamp = Cpt(EpicsSignal, "TSTimestamp", string=True, doc="0='Done' 1='Read'")


# --- NDCodec.template ---


class CodecPlugin_V34(PluginBase, version=(3, 4)):
    blosc_cl_evel = Cpt(SignalWithRBV, "BloscCLevel")
    blosc_compressor = Cpt(
        SignalWithRBV,
        "BloscCompressor",
        string=True,
        doc="0='BloscLZ' 1='LZ4' 2='LZ4HC' 3='SNAPPY' 4='ZLIB' 5='ZSTD'",
    )
    blosc_num_threads = Cpt(
        SignalWithRBV,
        "BloscNumThreads",
        string=True,
        doc="0='BloscLZ' 1='LZ4' 2='LZ4HC' 3='SNAPPY' 4='ZLIB' 5='ZSTD'",
    )
    blosc_shuffle = Cpt(
        SignalWithRBV, "BloscShuffle", string=True, doc="0='None' 1='Bit' 2='Byte'"
    )
    codec_error = Cpt(
        EpicsSignal, "CodecError", string=True, doc="0='None' 1='Bit' 2='Byte'"
    )
    codec_status = Cpt(
        EpicsSignal, "CodecStatus", string=True, doc="0='Success' 1='Warning' 2='Error'"
    )
    comp_factor = Cpt(
        EpicsSignalRO,
        "CompFactor_RBV",
        string=True,
        doc="0='Success' 1='Warning' 2='Error'",
    )
    compressor = Cpt(
        SignalWithRBV, "Compressor", string=True, doc="0='None' 1='JPEG' 2='Blosc'"
    )
    jpeg_quality = Cpt(
        SignalWithRBV, "JPEGQuality", string=True, doc="0='None' 1='JPEG' 2='Blosc'"
    )
    mode = Cpt(SignalWithRBV, "Mode", string=True, doc="0='Compress' 1='Decompress'")


# --- NDGather.template ---
