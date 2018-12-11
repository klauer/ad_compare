from ophyd import (
    Component as Cpt,
    FormattedComponent as FCpt,
    DynamicDeviceComponent as DDC,
    EpicsSignal,
    EpicsSignalRO,
    Device,
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
    default_read_attrs = kw.pop("default_read_attrs", [attr for attr, prefix in items])
    return DDC(ad_group(EpicsSignal, items), default_read_attrs=default_read_attrs, **kw)


def DDC_EpicsSignalRO(*items, **kw):
    default_read_attrs = kw.pop("default_read_attrs", [attr for attr, prefix in items])
    return DDC(ad_group(EpicsSignalRO, items), default_read_attrs=default_read_attrs, **kw)


def DDC_SignalWithRBV(*items, **kw):
    default_read_attrs = kw.pop("default_read_attrs", [attr for attr, prefix in items])
    return DDC(ad_group(SignalWithRBV, items), default_read_attrs=default_read_attrs, **kw)


class PluginBase_V20(PluginBase, version=(2, 0), version_of=PluginBase):
    epics_ts_sec = Cpt(EpicsSignalRO, "EpicsTSSec_RBV")
    epics_ts_nsec = Cpt(EpicsSignalRO, "EpicsTSNsec_RBV")


class PluginBase_V22(PluginBase_V20, version=(2, 2), version_of=PluginBase):
    ad_core_version = Cpt(EpicsSignalRO, "ADCoreVersion_RBV", string=True)
    array_callbacks = Cpt(
        SignalWithRBV, "ArrayCallbacks", string=True, doc="0='Disable' 1='Enable'"
    )
    array_size_int = Cpt(EpicsSignalRO, "ArraySize_RBV")
    color_mode = Cpt(
        SignalWithRBV,
        "ColorMode",
        string=True,
        doc="0=Mono 1=Bayer 2=RGB1 3=RGB2 4=RGB3 5=YUV444 6=YUV422 7=YUV421",
    )
    data_type = Cpt(
        SignalWithRBV,
        "DataType",
        string=True,
        doc="0=Int8 1=UInt8 2=Int16 3=UInt16 4=Int32 5=UInt32 6=Float32 7=Float64",
    )


class PluginBase_V26(PluginBase_V22, version=(2, 6), version_of=PluginBase):
    dimensions = Cpt(SignalWithRBV, "Dimensions")
    driver_version = Cpt(EpicsSignalRO, "DriverVersion_RBV", string=True)
    execution_time = Cpt(EpicsSignalRO, "ExecutionTime_RBV", string=True)
    ndimensions = Cpt(SignalWithRBV, "NDimensions", string=True)
    array_size = DDC_SignalWithRBV(
        ("array_size0", "ArraySize0"),
        ("array_size1", "ArraySize1"),
        ("array_size2", "ArraySize2"),
        ("array_size3", "ArraySize3"),
        ("array_size4", "ArraySize4"),
        ("array_size5", "ArraySize5"),
        ("array_size6", "ArraySize6"),
        ("array_size7", "ArraySize7"),
        ("array_size8", "ArraySize8"),
        ("array_size9", "ArraySize9"),
        doc="array_size",
    )
    dim_sa = DDC_SignalWithRBV(
        ("dim0_sa", "Dim0SA"),
        ("dim1_sa", "Dim1SA"),
        ("dim2_sa", "Dim2SA"),
        ("dim3_sa", "Dim3SA"),
        ("dim4_sa", "Dim4SA"),
        ("dim5_sa", "Dim5SA"),
        ("dim6_sa", "Dim6SA"),
        ("dim7_sa", "Dim7SA"),
        ("dim8_sa", "Dim8SA"),
        ("dim9_sa", "Dim9SA"),
        doc="dim_sa",
    )


class PluginBase_V31(PluginBase_V26, version=(3, 1), version_of=PluginBase):
    disordered_arrays = Cpt(SignalWithRBV, "DisorderedArrays")
    dropped_output_arrays = Cpt(SignalWithRBV, "DroppedOutputArrays")
    max_threads = Cpt(EpicsSignalRO, "MaxThreads_RBV")
    nd_attributes_macros = Cpt(EpicsSignal, "NDAttributesMacros")
    nd_attributes_status = Cpt(
        EpicsSignal,
        "NDAttributesStatus",
        string=True,
        doc="0='Attributes file OK' 1='File not found' 2='XML syntax error' 3='Macro substitution error'",
    )
    num_threads = Cpt(SignalWithRBV, "NumThreads")
    process_plugin = Cpt(EpicsSignal, "ProcessPlugin", string=True)
    sort_free = Cpt(EpicsSignal, "SortFree")
    sort_free_low = Cpt(EpicsSignal, "SortFreeLow")
    sort_mode = Cpt(SignalWithRBV, "SortMode", string=True, doc="0=Unsorted 1=Sorted")
    sort_size = Cpt(SignalWithRBV, "SortSize")
    sort_time = Cpt(SignalWithRBV, "SortTime")


class PluginBase_V33(PluginBase_V31, version=(3, 3), version_of=PluginBase):
    empty_free_list = Cpt(EpicsSignal, "EmptyFreeList", string=True)
    num_queued_arrays = Cpt(EpicsSignal, "NumQueuedArrays", string=True)
    pool_max_buffers = None  # REMOVED


class PluginBase_V34(PluginBase_V33, version=(3, 4), version_of=PluginBase):
    max_array_rate = Cpt(SignalWithRBV, "MaxArrayRate")
    max_array_rate_cout = Cpt(EpicsSignal, "MaxArrayRate_COUT")
    max_byte_rate = Cpt(SignalWithRBV, "MaxByteRate")
    min_callback_time = Cpt(SignalWithRBV, "MinCallbackTime")


class FilePlugin_V20(FilePlugin, PluginBase_V20, version=(2, 0), version_of=FilePlugin):
    ...


class FilePlugin_V21(FilePlugin_V20, version=(2, 1), version_of=FilePlugin):
    lazy_open = Cpt(SignalWithRBV, "LazyOpen", string=True, doc="0='No' 1='Yes'")


class FilePlugin_V22(FilePlugin_V21, PluginBase_V22, version=(2, 2), version_of=FilePlugin):
    create_directory = Cpt(SignalWithRBV, "CreateDirectory")
    file_number = Cpt(SignalWithRBV, "FileNumber")
    file_number_sync = None  # REMOVED
    file_number_write = None  # REMOVED
    temp_suffix = Cpt(SignalWithRBV, "TempSuffix", string=True)


class FilePlugin_V26(FilePlugin_V22, PluginBase_V26, version=(2, 6), version_of=FilePlugin):
    ...


class FilePlugin_V31(FilePlugin_V26, PluginBase_V31, version=(3, 1), version_of=FilePlugin):
    ...


class FilePlugin_V33(FilePlugin_V31, PluginBase_V33, version=(3, 3), version_of=FilePlugin):
    ...


class FilePlugin_V34(FilePlugin_V33, PluginBase_V34, version=(3, 4), version_of=FilePlugin):
    ...


class PvaPlugin(PluginBase_V22):
    'Serves as a base class for other versions'
    ...


class ROIStatPlugin(PluginBase_V22):
    'Serves as a base class for other versions'
    ...


class ROIStatNPlugin(Device):
    'Serves as a base class for other versions'
    ...


class AttributePlugin(PluginBase_V22, version=(2, 2)):
    'Serves as a base class for other versions'
    ...


class AttributeNPlugin(Device):
    'Serves as a base class for other versions'
    ...


class FFTPlugin(PluginBase_V22):
    'Serves as a base class for other versions'
    ...


class ScatterPlugin(PluginBase_V22):
    'Serves as a base class for other versions'
    ...


class PosPlugin(PluginBase_V22):
    'Serves as a base class for other versions'
    ...


class CircularBuffPlugin(PluginBase_V22):
    'Serves as a base class for other versions'
    ...


class AttrPlotPlugin(PluginBase_V22):
    'Serves as a base class for other versions'
    ...


class TimeSeriesNPlugin(Device):
    'Serves as a base class for other versions'
    ...


class TimeSeriesPlugin(PluginBase_V22):
    'Serves as a base class for other versions'
    ...


class CodecPlugin(PluginBase_V22):
    'Serves as a base class for other versions'
    ...


class GatherPlugin(PluginBase, version=(3, 1)):
    'Serves as a base class for other versions'
    ...


class GatherNPlugin(Device):
    'Serves as a base class for other versions'
    ...
